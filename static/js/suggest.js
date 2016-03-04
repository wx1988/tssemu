////////////////
// global variables
////////////////
constraints = null;

////////////////
// functions
////////////////

function suggestion_render_keepold(ts2plans){
    // ts2plans, total size to options. 
    // return value, one part is the upgrading plan
    // another part is the products list under each plan

    // Create a clapsable tab for each
    var keep_old_str = "";
    for(var ts in ts2plans){
        products = ts2plans[ts];

        var id_str = "keepold"+ts;
        var header_str = "Keep Old Mem, Target Size:"+ ts;
        header_str += ", Min Price:$"+get_min_price_of_all(products);
        // TODO, order by review
        var prod_str = render_products_list(products);
        var tmp_str = create_panel(id_str, header_str, prod_str);

        keep_old_str += tmp_str;
    }
    jQuery("#keepold").html(keep_old_str);
}


function suggestion_render_fullreplace(ts2plans){

    var full_replace_str = "";
    for(var ts in ts2plans){
        products = ts2plans[ts];

        var id_str = "fullreplace"+ts;
        var header_str = "Replace All Memory, Target Size:"+ ts;
        header_str += ", Min Price:$"+get_min_price_of_all(products);
        var prod_str = render_products_list(products);

        var tmp_str = create_panel(id_str, header_str, prod_str);


        full_replace_str += tmp_str;
    }
    jQuery("#fullreplace").html(full_replace_str);
}

function suggestion_render(data){
    // load the data here
    if(data.status != 0){
        alert(data.data);
        return;
    }
    data = data.data;
    //
    constraints = data.match_spec;
    // render this part
    suggestion_render_fullreplace(data.suggestions.full_replace);
    suggestion_render_keepold(data.suggestions.keep_old);
}


function load_suggestion(){
    // get sys info from the URL
    var sysinfo = get_sysinfo();
    var data = {"sys_info": JSON.stringify(sysinfo)};
    jQuery.post(
        "http://rtds9.cse.tamu.edu:8080/suggest",
        data,
        suggestion_render,
        "json");
}

function load_render(){
    load_suggestion();
    render_sysinfo();
}

jQuery(window).load(load_render);
