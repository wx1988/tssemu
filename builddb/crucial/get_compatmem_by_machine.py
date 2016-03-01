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
import os
import re
import urllib2

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.ram
cru_m_col = db.crucial_machine

from tsse_common import crucial_cache_folder as cache_folder
from tsse_common import download_url
from tsse_common import href_reg

from compatible_mem.get_crucial_spec import get_spec

def get_mem_list(mem_list_str):
    """
    for a computer product, get all compatible memory
    """
    ## step 2
    #mem_list_str = download_url(prod_url)
    #mem_list_str = open("crawldata/dell5810mem.html").read()
    mem_reg = "(<div class=\"product-module-desc\"(\s|\S)*?</div>)"
    mem_url_list = []
    for m in re.findall(mem_reg, mem_list_str):
        print "i",type(m), m
        tmp_str = m[0]
        if tmp_str.lower().count("ddr") == 0:
            continue
        m = re.search(href_reg, tmp_str)
        if m:
            print m
            mem_url_list.append( m.group(1) )
    print mem_url_list
    return mem_url_list


def get_cm_list_mp(manufacture, product):
    manu_dic = {
        "ASUSTeK Computer Inc.":"ASUS", 
        "Dell Inc.": "Dell"}
    if manu_dic.has_key(manufacture):
        tmp_str = manu_dic[manufacture]
    else:
        tmp_str = manufacture
    tmp_str += " "+product
    return get_cm_list(tmp_str)

def get_cm_list(machine_model):
    """
    step 1. identify the machine by search
    """
    res = cru_m_col.find_one({"machine_model": machine_model})
    if res:
        return res['mem_info_list']

    ## step 1
    search_tpl = "http://www.crucial.com/SearchDisplay?searchTerm=%s&storeId=10151&catalogId=10151&sType=SimpleSearch&searchFor=Keyword&resultCatEntryType=2"
    search_url = search_tpl%(machine_model.replace(" ","+"))
    cache_path = "%s/search_%s.txt"%(cache_folder, machine_model)
    search_str = download_url(search_url, cache_path)

    # use regex to get all memory link
    prod_list_reg = "(<ul class=\"results(\s|\S)*?</ul>)"
    m = re.search(prod_list_reg, search_str)
    if not m:
        raise Exception("search failed")
    print m.groups()
    all_str = m.group(1)

    # find the first link
    m = re.search(href_reg, all_str)
    if not m:
        raise Exception("not found")
    prod_url = m.group(1)
    print prod_url# for the machine
    mem_list_str = download_url(prod_url)
    mem_url_list = get_mem_list(mem_list_str)
    # TODO, after crawl, store into database.
    mem_info_list = []
    for mem_url in mem_url_list:
        try:
            mem_info = get_spec(mem_url)
            mem_info_list.append( mem_info )
        except Exception as e:
            print e

    cru_m_col.insert({
        "machine_model":machine_model,
        "mem_info_list": mem_info_list
        })
    return mem_info_list

############
# test the function within this file
############
def test_get_cmlist():
    test_name = "Dell Inc. Precision Tower 5810"
    print get_cm_list(test_name)

def test_get_cm_list_mp():
    #test_m_name = "Dell Inc. "
    #test_p_name = "Precision Tower 5810"
    test_m_name = "Gigabyte Technology Co., Ltd."
    test_p_name = "To be filled by O.E.M."
    print get_cm_list_mp(test_m_name, test_p_name)    

if __name__ == "__main__":
    #test_get_cmlist()
    #get_mem_list()
    test_get_cm_list_mp()
