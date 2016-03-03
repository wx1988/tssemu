from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.ram
az_review_col = db.amazon_review
az_col = db.amazon


import json
import gzip
import pickle
from sets import Set

def parse(path):
    g = gzip.open(path, 'r')
    for l in g: 
        yield json.dumps(eval(l))

def read_reviews():
    f = open("output.strict", 'w')
    review_path = "reviews_Electronics.json.gz"
    for l in parse(review_path):
        #f.write(l + '\n')
        print l
        break

def read_product():
    prod_path = "metadata.json.gz"
    flist = []
    c = 0
    tc = 0
    for l in parse(prod_path):
        tc += 1
        if tc % 10000 == 0:
            print 'total count', tc
        #title = l['title'].lower()
        title = l.lower()
        if 'ddr' in title and 'memory' in title:
            flist.append(l)
            c += 1
            if c % 100 == 0:
                print 'get', c
    json.dump(flist, open('memory.json','w'))

def get_memory_prod():
    m_str_list = json.load(open('memory.json','r'))
    m_list = [json.loads(m_str) for m_str in m_str_list]
    mid_set = Set()
    for m in m_list:
        #print m.keys()
        if not m.has_key('title'):
            continue
        title = m['title'].lower()
        if m.has_key('categories'):
            if not 'Memory' in m['categories'][0]:
                continue
        if 'ddr' in title and 'memory' in title:
            mid_set.add(m['asin'])
            #print m
    pickle.dump(mid_set, open('mid_list.pkl','w'))

def get_memory_reviews():
    mid_set = pickle.load(open('mid_list.pkl','r'))
    print len(mid_set)

    c = 0
    gc = 0
    rlist = []
    review_path = "reviews_Electronics.json.gz"
    for l in parse(review_path):
        #f.write(l + '\n')
        #print l
        rdic = json.loads(l)
        if rdic['asin'] in mid_set:
            gc += 1
            rlist.append(rdic)
        c += 1
        if c % 10000 == 0:
            print 'total count', c
        if gc % 100 == 0:
            print 'review count', gc
    pickle.dump(rlist, open('memory_review.pkl','w'))


def get_bad_reviews():
    rlist = pickle.load( open('memory_review.pkl','r'))
    brlist = []
    for r in rlist:
        if r['overall'] < 3:
            brlist.append(r)
    pickle.dump( brlist, open('bad_memory_review.pkl', 'w'))


def nltk_freq():
    from nltk import word_tokenize
    rlist = pickle.load( open("bad_memory_review.pkl",'r') )
    print len(rlist)
    wlist_list = []
    for r in rlist:
        wlist_list.append( word_tokenize( r['reviewText'] ) )

##########
# fill reviews
##########
def fill_reviews():
    # review into db    
    rlist = pickle.load( open('memory_review.pkl','r'))
    for r in rlist:
        az_review_col.insert(r)

def collect_reviews():
    asin_list = []
    for prod in az_col.find():
        if prod.has_key('review'):
            continue
        asin_list.append( prod['asin'] )

    for asin in asin_list:
        rid_list = []
        rscore_list = []
        for r in az_review_col.find({'asin':asin}):
            rid_list.append( str(r['_id']) )
            rscore_list.append( r['overall'] )
        review_dic = {'rid_list':rid_list, 'rscore_list':rscore_list}
        az_col.update(
            {'asin':asin},
            {'$set':{'review':review_dic}} )

if __name__ == "__main__":
    #read_product()
    #get_memory_prod()
    #get_memory_reviews()
    #get_bad_reviews()
    #nltk_freq()
    #fill_reviews()
    collect_reviews()
    
