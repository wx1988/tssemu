import os
import re
import urllib2
import time

def get_prod_list(fname): 
    """
    Item=N82E16833127685&
    """
    item_list = []
    p = re.compile("Item=(\w+)&")
    tmp_str = open(fname).read()
    #for m in p.finadll( tmp_str):
    for m in re.findall("Item=(\w+)[&\"]", tmp_str):
        #print m.group(1)
        #print m
        item_list.append(m)
    return list(set(item_list))

def extract_md(itemid):
    """
    Use this API to extract the meta data information
    http://ecology-service.cs.tamu.edu/BigSemanticsService/metadata.json?url=http://www.newegg.com/Product/Product.aspx?Item=N82E16820148770
    """
    outpath = "metadata/%s.json"%(itemid)
    if os.path.isfile(outpath):
        return
    print 'downloading', itemid
    url = "http://ecology-service.cs.tamu.edu/BigSemanticsService/metadata.json?url=http://www.newegg.com/Product/Product.aspx?Item=%s"%(itemid)
    res = urllib2.urlopen(url).read()
    with open(outpath,'w') as f:
        print>>f, res

def batch_download():
    #folder = "download/desktop"
    #suffix = "txt
    folder = "download"
    suffix = "html"
    flist = os.listdir(folder)
    for fname in flist:
        print fname
        if not fname.endswith(suffix):
            continue
        prod_list = get_prod_list("%s/%s"%(folder, fname))
        print "list of prod", len(prod_list)
        for prod in prod_list:
            try:
                extract_md(prod)
                #time.sleep(1)
            except Exception as e:
                print e

if __name__ == "__main__":
    batch_download()
    #print get_prod_list("download/desktop1.html")
    #print get_prod_list("download/desktop2.html")
