import os
import urllib2

# folders
root_folder = "/home/xingwang/project/tsse"
crucial_cache_folder = "%s/builddb/crucial/crawldata"%(root_folder)
newegg_folder = "%s/builddb/newegg"%(root_folder)
newegg_ram_md_folder = "%s/metadata"%(newegg_folder)
newegg_html_cache_folder = "%s/neweggcache"%(newegg_folder)
bb_memory_folder = "%s/builddb/bestbuy/memory"%(root_folder)

# regex
href_reg = "href=\"((\s|\S)*?)\""


def download_url(the_url,outpath=None):
    if outpath != None and os.path.isfile(outpath):
        return open(outpath).read()
    res = urllib2.urlopen(the_url).read()
    if outpath != None:
        with open(outpath,'w') as f:
            print>>f, res
    return res
