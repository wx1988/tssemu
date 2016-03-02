import os
import json
import gzip
import pickle
import urllib2
from sets import Set

def parse(path):
    g = gzip.open(path, 'r')
    for l in g: 
        yield json.dumps(eval(l))

def iter_mem():
    mem_list = json.load( open('memory.json','r'))
    #print len(mem_list)
    #print mem_list[10001]
    for mem in mem_list:
    	mem = json.loads(mem)
        print mem
        url = "http://ecology-service.cs.tamu.edu/BigSemanticsService/metadata.json?url=http://www.amazon.com/dp/%s"%(mem['asin'])

        try:
            outpath = "bigsem/%s.json"%(mem['asin'])
            if os.path.isfile(outpath):
                continue
            res = urllib2.urlopen(url).read()
            with open(outpath,'w') as f:
                print>>f, res
        except Exception as e:
            print e

if __name__ == "__main__":
    iter_mem()
