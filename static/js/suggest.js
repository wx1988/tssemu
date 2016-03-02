////////////////
// global variables
////////////////
constraints = null;

////////////////
// functions
////////////////
function get_sysinfo(){
    var name = 'sys_info';
    var results = urlParam(name);
    var sysinfo_str = decodeURIComponent(results);
    sysinfo_str = sysinfo_str.replace(/\+/g, " ");
    var sysinfo = JSON.parse( sysinfo_str );
    return sysinfo;
}

function render_sysinfo(){
    var sysinfo = get_sysinfo();
    // render this information part
    var machine_model = sysinfo.manufacturer+sysinfo.productname;

    var memory_limits = "Maximum Capacity:"+ sysinfo.maximum_capacity;
    memory_limits += ", Used/Total Slots: ";
    memory_limits += sysinfo.mem_list.length;
    memory_limits += "/";
    memory_limits += sysinfo.slots;

    var memory_list = "Current Memory List:<ul>";
    metadata_keys = ['model', 'type', 'speed', 'capacity', 'detail'];
    unit_list = ['', '', 'MHz', 'MB', ''];
    for( var i=0;i < sysinfo.mem_list.length;i++){
        tmp_str = "";
        for(var j=0;j < metadata_keys.length;j++){
            tmp_str += ", "+sysinfo.mem_list[i][metadata_keys[j]];
            tmp_str += unit_list[j];
        }
        memory_list += "<li>"+tmp_str.substring(1)+"</li>";
    }
    memory_list += "</ul>";

    var html_str = machine_model + "<br/>";
    html_str += memory_limits + "<br/>";
    html_str += memory_list;

var t = `<div class="panel-group">
    <div class="panel panel-default">
        <div class="panel-heading">
            <h4 class="panel-title">
                <a data-toggle="collapse" href="#{0}">
                    {1}
                </a>
            </h4>

            <div id="{0}" class="panel-collapse">
                <div class="panel-body">

                    {2}

                </div>
            </div>
        </div>
    </div>
</div>`;

    var id_str = "system_info"
    var header_str = "System Information";

    var tmp_str = String.format(t, id_str, header_str, html_str);

    jQuery('#sysinfo').html(tmp_str);
}


function render_products_list(products){
    // the products of interest under each plan
    var html_str = "<ul>";
    for(var i = 0;i < products.length;i++){
        html_str += "<li>";
        html_str += render_memory_str(products[i].metadata);
        html_str += "<br/>";
        html_str += "Buy "+products[i].buy_number+" unit"+', ';
        html_str += "Min price: $ "+products[i].min_price+" ";
        html_str += "</li>";
    }
    html_str += "</ul>";
    return html_str;
}

function get_min_price_of_all(products){
    var cur_min_price = 100000;
    for(var i=0;i < products.length;i++){
        if(products[i].min_price < cur_min_price)
            cur_min_price = products[i].min_price;
    }
    return cur_min_price;
}

function create_panel(id_str, header_str, content_str){
    var t = `<div class="panel-group">
    <div class="panel panel-default">
        <div class="panel-heading">
            <div class="row">
                <div class="col-sm-10">
                    <h4 class="panel-title">
                        <a data-toggle="collapse" href="#{0}">
                            {1}
                        </a>
                    </h4>
                </div>
                <div class="col-sm-2">
                    <a href='{3}'> View More >> </a>
                </div>
            </div>

            <div id="{0}" class="panel-collapse collapse">
                <div class="panel-body">

                    {2}

                </div>
            </div>
        </div>
    </div>
</div>`;

    var tmp_url = "/list_product?constraints=";
    tmp_url += encodeURIComponent( JSON.stringify(constraints));
    var res = String.format(t, id_str, header_str, content_str, tmp_url);
    return res;
}

function suggestion_render_keepold(ts2plans){
    // Create a clapsable tab for each
    var keep_old_str = "";
    for(var ts in ts2plans){
        products = ts2plans[ts];

        var id_str = "keepold"+ts;
        var header_str = "Keep Old Mem, Target Size:"+ ts;
        header_str += ", Min Price:$"+get_min_price_of_all(products);
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
