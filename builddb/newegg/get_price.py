import os
import re
import json
import urllib2

from format_product_bigsem import format_complete_prod
from builddb.format_product_free import format_incomplete_prod
from tsse_common import newegg_html_cache_folder

newegg_cache_folder = newegg_html_cache_folder
debug = 0

def download_newegg(neweggid):
    cache_path = "%s/%s.html"%(newegg_cache_folder,neweggid)
    if os.path.isfile(cache_path):
        return open( cache_path ).read()

    the_url = "http://www.newegg.com/Product/Product.aspx?Item=%s"%(neweggid)
    tmp_str = urllib2.urlopen(the_url).read()
    with open(cache_path, "w") as f:
        print>>f, tmp_str
    return tmp_str

def extract_price(neweggid):
    if debug:
        print neweggid
    tmp_str = download_newegg(neweggid)
    #tmp_str = open("9SIA8H53HD8572.html").read()

    # TODO, get the price information
    try:
        biz_reg = "(Biz.Product\.GroupItemSwitcher\.init\(\{(\s|\S)*?\}\);)"
        m = re.search(biz_reg, tmp_str)
        all_str = m.group(1)
        if debug:
            print all_str
        lines = all_str.split("\n")

        if all_str.count("properties:null") > 0:
            #[{"info":{"item":"20-326-573","price":151.9,"vehicle":null},"map":[]}]
            tmp_line = lines[2].strip()
            tmp_line = tmp_line[tmp_line.index("["):-1]
            tmp_dic = json.loads(tmp_line)
            return tmp_dic[0]['info']['price']
        else:
            # TODO, each product of different specification is different id

            # selectedProperties
            tmp_line = lines[3].strip()
            tmp_line = tmp_line[tmp_line.index("["):]
            #print tmp_line
            select_list = json.loads(tmp_line)
            select_dic = {s['name']:s['value'] for s in select_list}

            # all mapping
            tmp_line = lines[2].strip()
            tmp_line = tmp_line[tmp_line.index("["):-1]
            all_map = json.loads(tmp_line)

            for info in all_map:
                propertymap = info['map']
                match = True
                for pm in propertymap:
                    if select_dic[ pm['name'] ] != pm['value']:
                        match = False
                if match:
                    return info['info']['price']
    except Exception as e:
        li_reg = "<li class=\"price-current\"(\s|\S)*?content=\"(\d+[.\d+])\">"
        m = re.search(li_reg, tmp_str)
        #print m
        #exit(1)
        #product_sale_price

    return None

def test_extract_price():
    print extract_price("9SIA8H53HD8572")
    print extract_price("N82E16820104537")
    print extract_price("N82E16820104535")

    #tmp_res = """[{"name":"523","description":"Capacity","style":"Swatch","hasPriceAdditionInfo":false,"data":[{"value":"73720","description":"64GB &#40;8 x 8GB&#41;","displayInfo":"64GB &#40;8 x 8GB&#41;"},{"value":"79369","description":"32GB &#40;4 x 8GB&#41;","displayInfo":"32GB &#40;4 x 8GB&#41;"},{"value":"39219","description":"16GB &#40;4 x 4GB&#41;","displayInfo":"16GB &#40;4 x 4GB&#41;"},{"value":"38973","description":"16GB &#40;2 x 8GB&#41;","displayInfo":"16GB &#40;2 x 8GB&#41;"},{"value":"23986","description":"8GB &#40;2 x 4GB&#41;","displayInfo":"8GB &#40;2 x 4GB&#41;"},{"value":"40080","description":"8GB","displayInfo":"8GB"},{"value":"21736","description":"4GB","displayInfo":"4GB"}]},{"name":"521","description":"Type","style":"DropDownList","hasPriceAdditionInfo":false,"data":[{"value":"492469","description":"288-Pin DDR4 SDRAM","displayInfo":""}]},{"name":"524","description":"Speed","style":"Swatch","hasPriceAdditionInfo":false,"data":[{"value":"492470","description":"DDR4 2133 &#40;PC4 17000&#41;","displayInfo":"DDR4 2133 &#40;PC4 17000&#41;"},{"value":"497969","description":"DDR4 2400 &#40;PC4 19200&#41;","displayInfo":"DDR4 2400 &#40;PC4 19200&#41;"},{"value":"501014","description":"DDR4 2666 &#40;PC4 21300&#41;","displayInfo":"DDR4 2666 &#40;PC4 21300&#41;"}]},{"name":"37715","description":"Color","style":"DropDownList","hasPriceAdditionInfo":false,"data":[{"value":"485839","description":"Black","displayInfo":""}]},{"name":"39680","description":"LED color","style":"DropDownList","hasPriceAdditionInfo":false,"data":[{"value":"533514","description":"N&#47;A","displayInfo":""}]}]"""
    #print json.loads(tmp_res)

if __name__ == "__main__":
    test_extract_price()
