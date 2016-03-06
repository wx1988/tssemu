////////////
// faceted data panel generation
////////////
faceted_panel_template = `<div class="panel-heading">
    <h4 class="panel-title">
        <a data-toggle="collapse" href="#{2}">{0}</a>
    </h4>
    <div id="{2}" class="panel-collapse">
        <div class="panel-body">
            {1}
        </div>
    </div>
</div>`;

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
    // if prod_list == null, call this later timeout
    if(prod_list == null){
        setTimeout(create_faceted_panel,100);
        return;
    }

    //faceted_info
    // type, brand, capacity, speed, ecc, registered
    // optional, cas, voltage, 

    var products = prod_list;
    var t=faceted_panel_template;    

    // get all the meta field with more than one values
    simple_key_list = ['type', "brand", "freq", "ecc", "reg"];
    simple_showname_list = ['Type', "Manufacturer", "Speed", "ECC", "Registered/Buffered"];

    //keylist = ["brand", "capacity", ];
    //shownamelist = ["brand", "capacity"];
    keylist = simple_key_list;
    shownamelist = simple_showname_list;

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
            // TODO, if already in the constraints
            // show as checked. 
            if( constraints["metadata."+keylist[i]] != undefined){
                if( v.toString() == constraints["metadata."+keylist[i]].toString() )
                    tmp += " checked ";
            }
            tmp += " value='"+show_str+"' >"+show_str+"<br/>";

            checkbox_str += tmp;
        }
        var panel_str = String.format(
            t, shownamelist[i],
            checkbox_str, keylist[i])
        panels_str += panel_str;
    }

    // TODO, processing the kit capacity
    for(var j=0; j < products.length;j++){
        var p = products[j];
        if(p.metadata["capacity"] == undefined || p.metadata["number"] == undefined)
            continue;
        if(!v2count[p.metadata[keylist[i]]])
            v2count[p.metadata[keylist[i]]] = 0;
        v2count[p.metadata[keylist[i]]] += 1;
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
        if(k == "metadata.capacity") sv += 'G/stick';

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

    //plan, sys)_info
    plan_value = urlParam('plan');
    sys_info = urlParam('sys_info');
    var tmp_url = "/list_product2?constraints=";
    tmp_url += encodeURIComponent( JSON.stringify( tmp_constraints ));
    tmp_url += "&plan="+plan_value;
    tmp_url += "&sys_info="+sys_info;

    window.location.href= tmp_url;
}

///////////////
/// response on new faceted data selected
///////////////
