import json
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.ram
az_col = db.amazon

from builddb.format_product_free import format_incomplete_prod, get_capacity, get_typefreq

def populate():
    memlist = json.load(open('memory.json'))
    for mem in memlist:
        #print mem
        #print type(mem)
        memdic = json.loads(mem)
        if not memdic.has_key('categories'):
            continue
        if not 'Memory' in memdic['categories'][0]:
            continue

        print memdic['categories']
        az_col.insert(memdic)

def update_metadata(asin):
    try:
        m = az_col.find_one({'asin':asin})
        prod_str = ""
        if m.has_key('title'):
            prod_str += m['title'] + ' '
        if m.has_key("description"):
            prod_str += m['description'] + ' '
        metadata = format_incomplete_prod(prod_str)
        az_col.update(
			{"asin":asin},
			{'$set':{"metadata":metadata}})
    except Exception as e:
        print asin, e

def update_metadata_all():
    asin_list = []
    for az in az_col.find():
        asin_list.append( az['asin'] )
    for asin in asin_list:
        update_metadata(asin)

if __name__ == "__main__":
    populate()
