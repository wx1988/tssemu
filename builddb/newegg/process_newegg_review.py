import os
import re

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.ram
newegg_review_col = db.newegg_review
newegg_col = db.newegg

def get_reviwes_by_id(neweggid):
    fpath = "neweggreview/%s.html"%(neweggid)
    #fpath = "neweggreview/9SIA4UB3RF0795.html"
    content = open(fpath).read()
    review_list = get_reviews(content)
    for r in review_list:
        r['neweggid'] = neweggid
    return review_list

def get_reviews(content):
    reviews_reg = "(<table class=\"grpReviews(\s|\S)*?</table>)"
    m = re.search(reviews_reg, content)
    if not m:
        return []
    reviews_str = m.group(1)
    #print reviews_str
    review_reg = "(<th class=\"reviewer(\s|\S)*?</tr>)"
    review_para_reg = "(<p>(\s|\S)*?</p>)"
    dt_reg = "(\d+/\d+/\d+ \d+:\d+:\d+ \S\S)"
    rating_reg = "Rating: (\d)/\d"
    con_list = []

    review_list = []
    for m in re.findall(review_reg, reviews_str):
        review_str = m[0]
        # find time and rating here
        print review_str
        review_dic = {}

        dt_m = re.search( dt_reg, review_str )
        #print dt_m.groups()
        review_dic['datetime'] = dt_m.group(1)

        rating_m = re.search( rating_reg, review_str )
        #print rating_m.groups()
        review_dic['rating'] = int(rating_m.group(1))

        for md in re.findall(review_para_reg, review_str):
            tmp_str = md[0]
            #print tmp_str
            if tmp_str.count("<em>Cons") > 0:
                review_dic['cons'] = tmp_str
            if tmp_str.count("<em>Pros") > 0:
                review_dic['pros'] = tmp_str
            if tmp_str.count("<em>Other Thoughts") > 0:
                review_dic['other'] = tmp_str

        if len( review_dic.keys() ) == 0:
            continue
        review_list.append(review_dic)

    return review_list


def test_get_reviews():
    print get_reviwes_by_id("9SIA0AJ3S75119")
    print get_reviwes_by_id("9SIA4UB3RF0795")
    """
    fpath = "neweggreview/9SIA0AJ3S75119.html"
    #fpath = "neweggreview/9SIA4UB3RF0795.html"
    content = open(fpath).read()
    print get_reviews(content)
    """

def populate_newegg_review():
    for fname in os.listdir("neweggreview"):
        if not fname.endswith("html"):
            continue
        neweggid = fname[:-5]
        review_list = get_reviwes_by_id(neweggid)
        for review in review_list:
            newegg_review_col.insert(review)

def fill_reivews():
    nid_list = []
    for newegg in newegg_col.find():
        if newegg.has_key('review'):
            continue
        nid_list.append( newegg['neweggid'] )

    for nid in nid_list:
        rid_list = []
        rscore_list = []
        for r in newegg_review_col.find({'neweggid':nid}):
            rid_list.append( str(r['_id']) )
            rscore_list.append( r['rating'] )
        if len(rid_list) == 0:
            continue
        review_dic = {
            'rid_list':rid_list,
            'rscore_list':rscore_list }
        newegg_col.update(
            {'neweggid':nid},
            {'$set':{'review':review_dic}})


if __name__ == "__main__":
    #test_get_reviews()
    #populate_newegg_review()
    fill_reivews()
