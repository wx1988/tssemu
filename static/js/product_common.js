function get_prod_img(prod){
    if(prod.metadata.imgs == undefined)
        return '/static/imgs/no_image_available.png';
    if(prod.metadata.imgs.length == 0)
        return '/static/imgs/no_image_available.png';
    return prod.metadata.imgs[0];
}

function get_min_price(prod){
    var min_price = 100000;
    for(var i = 0;i < prod.websites.length;i++){
        if(prod.websites[i].price == null)
            continue;
        if(prod.websites[i].price < min_price)
            min_price = prod.websites[i].price;
    }
    if(min_price == 100000)
        return 'unknown';
    return min_price;
}

function render_memory_str(mem_metadata){
    // the metadata
    var tmp_str = "";
    // brand model
    tmp_str += mem_metadata.brand+', ';
    tmp_str += mem_metadata.model+', ';

    // specification, type, freq, pin, reg, ecc, cap
    tmp_str += mem_metadata.type+', ';
    tmp_str += mem_metadata.freq+"Mhz"+', ';
    tmp_str += mem_metadata.pin+"-Pin"+', ';
    if(mem_metadata.reg)
        tmp_str += "Registered"+', ';
    if(mem_metadata.ecc)
        tmp_str += "ECC"+', ';
    else
        tmp_str += "NonECC"+', ';
    tmp_str += mem_metadata.number + "x" +mem_metadata.capacity+"GB"+', ';

    // price
    tmp_str += "Unit price ($"+mem_metadata.price+")";
    return tmp_str;
}

function render_prod_source(prod){
    // sort the websites based on price
    var template = "<a href='{0}' target='_blank'><img src='{1}' height='20' /></a>";
    var source_list = prod.websites;
    source_list.sort(function(a,b){return a.price-b.price;});
    var html_str = "";
    var website2logo = {
        'crucial': "/static/imgs/sourcelogo/crucial_micron.jpg", 
        'amazon': "/static/imgs/sourcelogo/amazon.png", 
        'newegg': "/static/imgs/sourcelogo/newegg.png", 
        "bestbuy": "/static/imgs/sourcelogo/bestbuy.jpg"
    };
    for(var i = 0;i < source_list.length;i++){
        html_str += String.format(
            template, 
            source_list[i].url, 
            website2logo[source_list[i].website] );
    }
    return html_str;
}

function render_product_grid2(prod, plan_str){

    //var tmp_str = "<div style='height:200px;'>";
    var tmp_str = "<div style='height:350px;'>";

    //tmp_str += "<div><a href='/view_product?id="+prod_list[j].source+"_"+prod_list[j].id+"'>";
    tmp_str += "<div><a href='#'>";
    // image of the same height
    var img_url = get_prod_img(prod);
    tmp_str += "<div style='height:250px'><img src='"+img_url+"' width='250px' /></div>";

    tmp_str += "<div>"+gen_prod_desc(prod.metadata)+"</div>";
    tmp_str += "</a></div>";

    // add the review information here    
    var star = Math.round( prod.mean_review );

    // basic information part
    tmp_str += "<div>";
    tmp_str += "<img src='static/imgs/"+star+"star.png' width='50'/>";
    tmp_str += "("+prod.mean_review.toFixed(2)+", "+prod.review_num+" reviews)";
    tmp_str += "</div>";

    // price part
    // get the capacity to buy
    var ws = plan_str.split('_');
    var target_cap = parseInt(ws[1]);

    // divide by the capacity per product, ceil    
    var cur_cap = 0;
    sysinfo = get_sysinfo();
    for(var i=0;i < sysinfo.mem_list.length;i++){
        cur_cap += (sysinfo.mem_list[i].capacity / 1024);
    }

    var remain_cap = target_cap - cur_cap;
    var per_unit_cap = prod.metadata.capacity * prod.metadata.number;
    var unit_num = Math.ceil(remain_cap/per_unit_cap);

    tmp_str += "<div>";    
    tmp_str += "Price: $"+get_min_price(prod)*unit_num;
    tmp_str += "(Buy " + unit_num + " units)";
    // add different source of information, 14 px
    tmp_str += render_prod_source(prod);
    tmp_str += "</div>";

    tmp_str += "</div>";
    return tmp_str;
}

function render_product_grid(prod){
    //var tmp_str = "<div style='height:200px;'>";
    var tmp_str = "<div style='height:350px;'>";

    //tmp_str += "<div><a href='/view_product?id="+prod_list[j].source+"_"+prod_list[j].id+"'>";
    tmp_str += "<div><a href='#'>";
    // image of the same height
    var img_url = get_prod_img(prod);
    tmp_str += "<div style='height:250px'><img src='"+img_url+"' width='250px' /></div>";

    tmp_str += "<div>"+gen_prod_desc(prod.metadata)+"</div>";
    tmp_str += "</a></div>";

    // add the review information here    
    var star = Math.round( prod.mean_review );

    // basic information part
    tmp_str += "<div>";
    tmp_str += "<img src='static/imgs/"+star+"star.png' width='50'/>";
    tmp_str += "("+prod.review_num+" reviews)";
    tmp_str += "</div>";

    // price part
    tmp_str += "<div>";
    tmp_str += "Price: $"+get_min_price(prod);
    // add different source of information, 14 px
    tmp_str += render_prod_source(prod);
    tmp_str += "</div>";

    tmp_str += "</div>";
    return tmp_str;
}


function gen_prod_desc(mem_metadata){
    // the metadata
    var tmp_str = "";
    // brand model
    tmp_str += mem_metadata.brand+', ';
    tmp_str += mem_metadata.model+', ';

    // specification, type, freq, pin, reg, ecc, cap
    tmp_str += mem_metadata.type+', ';
    tmp_str += mem_metadata.freq+"Mhz"+', ';
    tmp_str += mem_metadata.pin+"-Pin"+', ';
    if(mem_metadata.reg)
        tmp_str += "Registered"+', ';
    if(mem_metadata.ecc)
        tmp_str += "ECC"+', ';
    else
        tmp_str += "NonECC"+', ';
    tmp_str += mem_metadata.number + "x" +mem_metadata.capacity+"GB";
    return tmp_str;
}

function sort_product_by_review(prod_list){
    var tmp_prod_list = prod_list;
    tmp_prod_list.sort(function(a,b){
        var part1 = (b.mean_review - a.mean_review)*1000000;
        var part2 = (b.review_num - a.review_num)*1000;
        var part3 = get_min_price(a) - get_min_price(b);
        return part1 + part2 + part3;

    });
    return tmp_prod_list;
}

function sort_product_by_price_lh(prod_list){
    var tmp_prod_list = prod_list;
    tmp_prod_list.sort(function(a,b){
        return  get_min_price(a) - get_min_price(b);
    });
    return tmp_prod_list;
}

function sort_product_by_price_hl(prod_list){
    var tmp_prod_list = prod_list;
    tmp_prod_list.sort(function(a,b){
        return  get_min_price(b) - get_min_price(a);
    });
    return tmp_prod_list;
}

function sort_product_by_review2(prod_list){
    // TODO, the average review is not detailed enough
    var tmp_prod_list = prod_list;
    tmp_prod_list.sort(function(a,b){
        var part1 = (b.mean_review - a.mean_review)*1000000;
        var part2 = (b.review_num - a.review_num)*1000;
        var part3 = a.metadata.totalprice - b.metadata.totalprice;
        return part1 + part2 + part3;
    });
    return tmp_prod_list;
}

function sort_product_by_price_lh2(prod_list){
    var tmp_prod_list = prod_list;
    tmp_prod_list.sort(function(a,b){
        return  a.metadata.totalprice - b.metadata.totalprice;
    });
    return tmp_prod_list;
}

function sort_product_by_price_hl2(prod_list){
    var tmp_prod_list = prod_list;
    tmp_prod_list.sort(function(a,b){
        return  b.metadata.totalprice - a.metadata.totalprice;
    });
    return tmp_prod_list;
}
