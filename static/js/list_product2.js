// get the product list, and show
constraints_list = null;
cur_plan = null;
prod_list = null;

function render_plan(plan_str){
    function render_current_memory(){
        var tmp_str = "";
        sysinfo = get_sysinfo();
        for(var i=0;i < sysinfo.mem_list.length;i++){
           tmp_str += (sysinfo.mem_list[i].capacity / 1024)+"G ";
        }
        return tmp_str;
    }
    
    var html_str = "Current Plan: ";
    if(plan_str[0] == 'k'){
        html_str += "Keep Old Memory ("+ render_current_memory() +")";
    }
    else{
        html_str += "Replace All Memory";
    }
    var ws = plan_str.split('_')
    html_str += ", Target Size: "+ws[1]+"G";
    html_str += ", Per Stick Size: "+ws[2]+"G";
    html_str = "<h4>" + html_str+"</h4>";
    jQuery("#plan").html(html_str);
}

function render_product_list(mode){
    if(mode == "rating"){
        prod_list = sort_product_by_review(prod_list);
    }else if(mode == "pricelh"){
        prod_list = sort_product_by_price_lh(prod_list);
    }else if(mode == "pricehl"){
        prod_list = sort_product_by_price_hl(prod_list);
    }else{
        console.log("unknow sort mode"+mode);
        prod_list = sort_product_by_review(prod_list);
    }
    
    for(var i=0; i< 3;i++){
        var col_str = "";
        for(var j=0;j < prod_list.length;j++){
            if( j%3!=i) 
                continue;

            tmp_str = render_product_grid(prod_list[j]);
            col_str += tmp_str;
        }
        var div_id = "prod_list_col_"+(i+1);
        jQuery('#'+div_id).html(col_str);
    }
}

function get_prod_cb(data){
    if(data.status != 0){
        alert(data.data);
        return;
    }

    prod_list = data.data;
    render_product_list("rating");    
    // TODO , create the faceted data panel here
    //create_faceted_panel(prod_list);
}

window.onload = function(){
    // get the constriants parameter from the URL
    constraints_str = decodeURIComponent(urlParam('constraints'));
    constraints = JSON.parse( decodeURIComponent(urlParam('constraints')) );
    cur_constraints = constraints;

    // TODO, rendering the current plan.    
    var plan_str = decodeURIComponent(urlParam('plan'));
    render_plan(plan_str);

    // get all product and render them
    // TODO, also pass the plan here
    jQuery.post(
        "/search_product",
        {"constraints":constraints_str},
        get_prod_cb,
        "json");

    rendering_faceted_tags(constraints);
}

////////////
// faceted data
////////////
faceted_info = null;
// global variabel of the faceted info
function whole_faceted_info_cb(data){    
    if(data.status != 0){
        alert(data.data);
    }

    // create_faceted_panel
    faceted_info = data.data;
    create_faceted_panel();

}

function get_whole_faceted_info(){
    jQuery.post(
        "/get_faceted_info", 
        {},
        whole_faceted_info_cb,
        "json");
}

function create_faceted_panel(){
    var products = prod_list;
    var t=`<div class="panel-heading">
            <h4 class="panel-title">
                <a data-toggle="collapse" href="#{2}">{0}</a>
            </h4>
            <div id="{2}" class="panel-collapse">
                <div class="panel-body">
                    {1}
                </div>
            </div>
        </div>`;

    // get all the meta field with more than one values
    keylist = ["brand", "capacity"];
    shownamelist = ["brand", "capacity"];

    var panels_str = "";
    for(var i=0;i < keylist.length;i++){
        var v2count = {}
        for(var j=0; j < products.length;j++){
            var p = products[j];
            if(p.metadata[keylist[i]] == undefined)
                continue;
            if(!v2count[p.metadata[keylist[i]]])
                v2count[p.metadata[keylist[i]]] = 0;
            v2count[p.metadata[keylist[i]]] += 1;
        }
        var checkbox_str = "";
        //console.log(v2count);
        for(v in v2count){
            var show_str = v +"("+v2count[v]+")";
            var tmp = "<input type='checkbox' name='"+keylist[i]+"'";
            tmp += " value='"+show_str+"' >"+show_str+"<br/>";
            checkbox_str += tmp;
        }
        var panel_str = String.format(
            t, shownamelist[i],
            checkbox_str, keylist[i])
        panels_str += panel_str;
    }
    jQuery("#faceted_panel").html(panels_str);

}


///////////////
//// feed back on selected faceted data
///////////////
function rendering_faceted_tags(constraints){
    var t=`<li>
        <span class="label label-default">
            {0}
            <button type="button" class="close"
                data-dismiss="li" name="{1}" value="{2}"
                onclick="close_facet_tags('{1}');">
                <span aria-hidden="true">&times;</span>
                <span class="sr-only">Close</span>
            </button>
        </span>
    </li>`;

    var tmp_str = "<ul>";
    for(var k in constraints){
        var v = constraints[k];

        var sv = v;
        if(k== 'metadata.ecc'){
            if(v == true)
                sv = "ECC";
            else
                sv = "NonECC"
        }

        if(k== 'metadata.reg'){
            if(v== true)
                sv = "Registered";
            else
                sv = "UnBuffered";
        }
        if(k == "metadata.pin") sv += '-Pin';

        var tmp_res = String.format(t, sv, k, v);
        tmp_str += tmp_res;
    }
    tmp_str += "</ul>";
    jQuery('#taglist').html(tmp_str);
}

function close_facet_tags(name){
    var tmp_constraints = {};
    for(var k in constraints){
        if(k == name)
            continue;
        tmp_constraints[k] = constraints[k];
    }
    var tmp_url = "/list_product?constraints=";
    tmp_url += encodeURIComponent( JSON.stringify( tmp_constraints ));

    window.location.href= tmp_url;
}


////////////
// sort product part
////////////
$('#sortbyselect').change(function(){ 
    var value = $(this).val();
    render_product_list(value);
});