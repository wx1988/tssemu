import os
import urllib2

# folders
root_folder = "/home/xingwang/project/tsse"
crucial_cache_folder = "%s/compatible_mem/crawldata"%(root_folder)

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