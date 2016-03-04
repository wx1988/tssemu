
function render_plans(plans){
	// rendering different upgrading plans
	plans.sort(function(a,b){
		return b.score-a.score;
	});
	var all_plan_str = "";
	for(var i in plans){
		var id_str = plans[i].name;
		header_str = "";
		if(id_str[0] == 'k')
			header_str += "Keep Old Memory, ";
		else
			header_str += "Replace All Memory, ";
		header_str += "Target Size: "+ plans[i].target_size +", ";
		header_str += "Per Stick Size: " + plans[i].per_stick_size+", ";
		header_str += "Min Price: $" + get_min_price_of_all(plans[i].prod_list);
		var prod_str = render_products_list(plans[i].prod_list);
		var tmp_str = create_panel(id_str, header_str, prod_str);
		all_plan_str += tmp_str;
	}
	jQuery("#suggestions").html(all_plan_str);

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
    //suggestion_render_fullreplace(data.suggestions.full_replace);
    //suggestion_render_keepold(data.suggestions.keep_old);
    render_plans(data.suggestions);
}


function load_suggestion(){
    // get sys info from the URL
    var sysinfo = get_sysinfo();
    var data = {"sys_info": JSON.stringify(sysinfo)};
    jQuery.post(
        "http://rtds9.cse.tamu.edu:8080/suggest2",
        data,
        suggestion_render,
        "json");
}

function load_render(){
    load_suggestion();
    render_sysinfo();
}

jQuery(window).load(load_render);