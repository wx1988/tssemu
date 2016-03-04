
// get the product list, and show
constraints_list = null;

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
            if( j%3!=i) continue;
            //var tmp_str = "<div style='height:200px;'>";
            var tmp_str = "<div style='height:350px;'>";

            //tmp_str += "<div><a href='/view_product?id="+prod_list[j].source+"_"+prod_list[j].id+"'>";
            tmp_str += "<div><a href='#'>";
            var img_url = get_prod_img(prod_list[j]);
            tmp_str += "<div><img src='"+img_url+"' width='250px' /></div>";
            tmp_str += "<div>"+gen_prod_desc(prod_list[j].metadata)+"</div>";
            tmp_str += "</a></div>";

            // add the review information here    
            var star = Math.round( prod_list[j].mean_review );
            tmp_str += "<div>";
            tmp_str += "<img src='static/imgs/"+star+"star.png' width='50'/>";
            tmp_str += "("+prod_list[j].review_num+" reviews)";
            tmp_str += "</div>";

            tmp_str += "<div></div>";

            tmp_str += "Price: $"+get_min_price(prod_list[j]);
            tmp_str += "</div>";
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
    create_faceted_panel(prod_list);
}

window.onload = function(){
    // get the constriants parameter from the URL
    constraints_str = decodeURIComponent(urlParam('constraints'));
    constraints = JSON.parse( decodeURIComponent(urlParam('constraints')) );
    cur_constraints = constraints;

    // get all product and render them
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
function create_faceted_panel(products){
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
function sort_prod_by(tagname){
    // TODO, select option change
}

$('#sortbyselect').change(function(){ 
    var value = $(this).val();
    render_product_list(value);
});