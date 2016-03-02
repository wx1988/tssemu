import os
import pickle
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import *
from collections import Counter

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def split_raw():
    rlist = pickle.load( open("bad_memory_review.pkl",'r') )
    for r in rlist:
        #wlist_list.append( word_tokenize( r['reviewText'] ) )
        out_path = "data/raw/%s-%s.txt"%(r['asin'], r['reviewerID'])
        if os.path.isfile( out_path ):
            continue
        with open(out_path,'w') as f:
            print>>f, r['reviewText']


def nltk_freq():
    rlist = pickle.load( open("bad_memory_review.pkl",'r') )
    print len(rlist)
    wlist_list = []
    tmp_str = ""

    stemmer = PorterStemmer()
    for r in rlist:
        #wlist_list.append( word_tokenize( r['reviewText'] ) )
        out_path = "data/stem/%s-%s.pkl"%(r['asin'], r['reviewerID'])
        if os.path.isfile( out_path ):
            continue

        #print r.keys()
        tmp_str = r['reviewText']

        #print tmp_str
        tmp_str = tmp_str.lower()
        tokens = word_tokenize( tmp_str )
        filtered = [w for w in tokens if not w in stopwords.words('english')]
        #print filtered
        stemmed = stem_tokens(filtered, stemmer)
        #print stemmed
        pickle.dump(stemmed, open(out_path,'w'))

def counter():
    stem_dir = "data/stem"
    flist = os.listdir(stem_dir)
    wwlist = []
    for fname in flist:
        if not fname.endswith("pkl"):
            continue
        fpath = "%s/%s"%(stem_dir, fname)
        wlist = pickle.load(open(fpath,'r'))
        wwlist.extend( wlist )
    count = Counter(wwlist)
    print count.most_common(300)
    print len(count.keys())

if __name__ == "__main__":
    #nltk_freq()
    #counter()
    split_raw()
