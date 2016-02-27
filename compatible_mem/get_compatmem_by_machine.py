import os
import re
import urllib2

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.ram
cru_col = db.crucial

test_name = "Dell Inc. Precision Tower 5810"
cache_folder = "crawldata"

href_reg = "href=\"((\s|\S)*?)\""
from builddb.newegg.format_product_free import format_incomplete_prod

def download_url(the_url,outpath=None):
    if outpath != None and os.path.isfile(outpath):
        return open(outpath).read()
    res = urllib2.urlopen(the_url).read()
    if outpath != None:
        with open(outpath,'w') as f:
            print>>f, res
    return res

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

    # the price information
    price_reg = "(class=\"priceList\"(\s|\S)*?</ul>)"
    m = re.search(price_reg, res)
    #print m.
    price_str = m.group(1)
    start = price_str.index("$")+1
    end = price_str.index("</", start)
    price_str = price_str[start:end].replace(',','')
    tmp_dic['price'] = float(price_str)
    return tmp_dic

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

def get_cm_list(machine_model):
    """
    step 1. identify the machine by search
    """
    res = cru_col.find_one({"machine_model": machine_model})
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

    cru_col.insert({
        "machine_model":machine_model,
        "mem_info_list": mem_info_list
        })
    return mem_info_list

def test_get_spec():
    the_url = "http://www.crucial.com/usa/en/precision-5810/CT6338640"
    the_url = "http://www.crucial.com/usa/en/precision-5810/CT7169774"
    print get_spec(the_url)

def test_get_cmlist():
    get_cm_list(test_name)

if __name__ == "__main__":
    test_get_cmlist()
    #get_mem_list()
    #test_get_spec()
