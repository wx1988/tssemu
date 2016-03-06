// get the product list, and show
// global variables
constraints = null;
cur_plan = null;
prod_list = null;
faceted_info = null;

window.onload = function(){
    // get the constriants parameter from the URL
    constraints_str = decodeURIComponent(urlParam('constraints'));
    constraints = JSON.parse( decodeURIComponent(urlParam('constraints')) );
    cur_constraints = constraints;

    // rendering the current plan.    
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

    get_whole_faceted_info();
}

/////////////
/// Upgrading plan
/////////////
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

/////////////
/// product list under current plan
/////////////
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
    jQuery("#total_number").html(prod_list.length+" items");
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

////////////
// UI event handler of sort product part
////////////
$('#sortbyselect').change(function(){ 
    var value = $(this).val();
    render_product_list(value);
});