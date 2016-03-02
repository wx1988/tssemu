function get_prod_img(prod){
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
