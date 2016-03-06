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
    // TODO, sort by review, and add the
    products = sort_product_by_review(products);
    
    // the products of interest under each plan
    var html_str = "<ul>";
    for(var i = 0;i < products.length;i++){
        html_str += "<li>";
        html_str += render_memory_str(products[i].metadata);
        html_str += "<br/>";

        // TODO, add review summarization here
        var star = Math.round( products[i].mean_review );
        html_str += "<img src='static/imgs/"+star+"star.png' width='50'/>";
        html_str += "("+products[i].review_num+" reviews)<br/>";

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

function create_panel(id_str, header_str, content_str, plan){
    var t = `<div class="panel-group">
    <div class="panel panel-default">
        <div class="panel-heading">
            <div class="row">
                <div class="col-sm-10">
                    <h4 class="panel-title">
                        <a data-toggle="collapse" href="#{0}">{1}</a>
                    </h4>
                </div>
                <div class="col-sm-2">
                    <a href='{3}'> View More >> </a>
                </div>
            </div>
            <div id="{0}" class="panel-collapse collapse">
                <div class="panel-body">{2}</div>
            </div>
        </div>
    </div>
</div>`;

    var tmp_url = "/list_product2?";
    
    // part 1
    tmp_url += "sys_info="+urlParam("sys_info");

    // part 2
    var tmp_constraints = constraints;
    if(plan != undefined){
        tmp_url += "&plan="+plan;
        // get the perstick capacity here
        var ws = plan.split('_')
        tmp_constraints['metadata.capacity'] = parseInt(ws[2]);    
    }

    // part 3
    tmp_url += "&constraints=";
    tmp_url += encodeURIComponent( JSON.stringify(tmp_constraints));    
    
    var res = String.format(t, id_str, header_str, content_str, tmp_url);
    return res;
}
