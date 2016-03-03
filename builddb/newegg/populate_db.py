
import os
import re
import json
import urllib2
import time

from pymongo import MongoClient

from format_product_bigsem import format_complete_prod
from builddb.format_product_free import format_incomplete_prod

from tsse_common import newegg_ram_md_folder as ram_md_folder
from get_price import extract_price
# TODO, connect the db here. write the db configuration in a separate files.
#from consts import MONGO_DB_HOST, MONGO_DB_USER, MONGO_DB_PASSWD

client = MongoClient('localhost', 27017)
db = client.ram
newegg_col = db.newegg

def import_ram():
    """
    enumerate all files in metadata folder (metadata from bigsemantics)
    insert into mongo database
    """
    ram_md_folder = "metadata"
    for fname in os.listdir(ram_md_folder):
        if not fname.endswith("json"):
            continue
        obj = json.loads(open("%s/%s"%(ram_md_folder, fname),'r').read())

        neweggid = fname[:-5]
        if not newegg_col.find_one({"neweggid": neweggid}):
            newegg_col.insert({
                'neweggid':neweggid,
                'data': obj })

def check_ok(prod_info):
    """
    check whether the information is enough
    """    
    nece_list = ['type', 'freq', 'capacity']
    for k in nece_list:
        if not prod_info.has_key(k):
            print 'missing', k
            return False
    return True


def extract_metadata():
    """
    based on the metadata from bigsemantic, 
    also use regex to get accurate specification in unified representation
    """
    ram_md_folder = "metadata"
    for fname in os.listdir(ram_md_folder):
        if not fname.endswith("json"):
            continue
        neweggid = fname[:-5]
        prod_md_str = open("%s/%s"%(ram_md_folder, fname),'r').read()
        prod_md = json.loads(prod_md_str)
        try:
            p1 = format_complete_prod(prod_md)
            ok1 = check_ok(p1)
            if ok1:
                newegg_col.update(
                    {'neweggid':neweggid},
                    {"$set":{'metadata':p1}})
                continue
            p2 = format_incomplete_prod(prod_md_str)
            ok2 = check_ok(p2)
            if ok2:
                newegg_col.update(
                    {'neweggid':neweggid},
                    {"$set":{'metadata':p2}})
                continue
        except Exception as e:
            print e

def populate_price():
    """
    extract the price information from the webpage
    """
	neweggid_list = []
	for ni in newegg_col.find():
		neweggid_list.append(ni['neweggid'])
	for ni in neweggid_list:
		print ni
		try:
			price = extract_price(ni)
			newegg_col.update(
				{'neweggid':ni},
				{"$set":{"metadata.price":price}})
			time.sleep(2)
		except Exception as e:
			print e

############
# interface to populate database
############
def update_metadata(neweggid):
    prod_info = {}
    prod_md_str = open("%s/%s.json"%(ram_md_folder, neweggid),'r').read()
    prod_md = json.loads(prod_md_str)
    try:
        p1 = format_complete_prod(prod_md)
        ok1 = check_ok(p1)
        if ok1:
            prod_info = p1
        else:
            prod_info = format_incomplete_prod(prod_md_str)
    except Exception as e:
        print e
    prod_info['price'] = extract_price(neweggid)
    print prod_info
    newegg_col.update(
        {'neweggid':neweggid},
        {"$set":{'metadata':prod_info}})

def update_metadata_all():
    # get all newegg list
    for fname in os.listdir(ram_md_folder):
        if not fname.endswith("json"):
            continue
        neweggid = fname[:-5]
        update_metadata(neweggid)


if __name__ == "__main__":
    #import_ram()
    #extract_metadata()
    #try_search()
    #populate_price()
    update_metadata("N82E16820231225")
