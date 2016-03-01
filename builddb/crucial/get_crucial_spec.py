"""
__author__ = "Xing Wang"
__copyright__ = "Copyright 2016, The TSSE MU Project"
__credits__ = ["Xing Wang"]
__license__ = "All right reserved"
__version__ = "0.1"
__maintainer__ = "Xing Wang"
__email__ = "xingwang@cse.tamu.edu"
__status__ = "Production"
"""
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.ram
cru_col = db.crucial_mem

import re, os
from tsse_common import download_url
from tsse_common import crucial_cache_folder as cache_folder

# TODO
from builddb.newegg.format_product_free import format_incomplete_prod

def get_spec(mem_url):
    """
    get the specification of each memory
    """
    mem_model = mem_url[mem_url.rindex("/")+1:]
    cache_path = "%s/mem_%s.txt"%(cache_folder, mem_model)
    res = download_url(mem_url, cache_path)

    # search specification
    tmp_dic = format_incomplete_prod(res)
    tmp_dic['url'] = mem_url
    tmp_dic['model'] = mem_url[mem_url.rindex("/")+1:]

    # the price information
    price_reg = "(class=\"priceList\"(\s|\S)*?</ul>)"
    m = re.search(price_reg, res)
    #print m.
    price_str = m.group(1)
    start = price_str.index("$")+1
    end = price_str.index("</", start)
    price_str = price_str[start:end].replace(',','')
    tmp_dic['price'] = float(price_str)
    if not cru_col.find_one({'model':tmp_dic['model']}):
        cru_col.insert(tmp_dic)
    return tmp_dic

############
# test the function within this file
############
def test_get_spec():
    """
    TODO, might move to another file
    """
    the_url = "http://www.crucial.com/usa/en/precision-5810/CT6338640"
    the_url = "http://www.crucial.com/usa/en/precision-5810/CT7169774"
    print get_spec(the_url)

if __name__ == "__main__":    
    test_get_spec()