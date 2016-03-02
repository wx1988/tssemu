import copy
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.ram
prod_col = db.products

cru_col = db.crucial_mem
az_col = db.amazon
newegg_col = db.newegg
bb_col = db.bestbuy

db_info_list = [
    {'website':'crucial', 'col':cru_col, "mf":"model", "pf":"price", "idf":"model"},
    {'website':'amazon', 'col':az_col, "mf":"metadata.model", "pf":"price", "idf":"asin"},
    {'website':'newegg', 'col':newegg_col, "mf":"metadata.model", "pf":"metadata.price", "idf":"neweggid"},
    {'website':'bestbuy', 'col':bb_col, "mf":"metadata.model", "pf":"metadata.price","idf":"skuid"}
]

from builddb.crucial.get_crucial_spec import update_metadata_all as curcial_update
from builddb.newegg.populate_db import update_metadata_all as newegg_update
from builddb.bestbuy.populate_db import update_metadata_all as bestbuy_update
from builddb.amazon.populate_db import update_metadata_all as az_update


def do_all():
    curcial_update()


def consolidate_one(model):
    website_list = []
    match_prod_specs = []
    for db_info in db_info_list:
        print db_info
        m = db_info['col'].find_one( {db_info['mf']:model} )
        print m
        if not m:
            continue

        # product info part
        tmpdic = {
            'website':db_info['website'],
            'id':m[db_info['idf']] }
        if db_info['website'] in ['curcial','amazon']:
            tmpdic['price'] = m['price']
        else:
            if m['metadata'].has_key('price'):
                tmpdic['price'] = m['metadata']['price']
        website_list.append(tmpdic)

        # specification part
        if db_info['website'] == 'crucial':
            tmpdic = copy.copy(m)
            del m['_id']
            match_prod_specs.append(m)
        else:
            match_prod_specs.append(m['metadata'])

    # fill the website, id, and price
    prod_col.update(
        {"model":model},
        {"$set":{"websites":website_list}})
    merge_spec = {}
    for spec in match_prod_specs:
        merge_spec = dict(merge_spec.items()+spec.items())
    #print merge_spec
    # consolidate the specification across
    prod_col.update(
        {"model":model},
        {"$set":{"metadata":merge_spec}})


def consolidate():
    # get meta data except the price
    model_list = []
    for p in prod_col.find():
        model_list.append(p['model'])
        # find the model in each of the database

    for model in model_list:
        consolidate_one(model)
        #break

if __name__ == "__main__":
    #curcial_update()
    #newegg_update()
    #bestbuy_update()
    #az_update()
    #consolidate_one("CT12864AA800")
    #consolidate_one("F3-12800CL9T-6GBNQ")
    consolidate()

