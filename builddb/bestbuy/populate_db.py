import os
import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.ram
bb_col = db.bestbuy

from extract_spec import extract_spec as es_bb

def import_ram():
    ram_md_folder = "memory"
    for fname in os.listdir(ram_md_folder):
        if not fname.endswith("json"):
            continue
        obj = json.load(open("%s/%s"%(ram_md_folder,fname)))
        skuid = fname[:-5]
        if not bb_col.find_one({"skuid":skuid}):
            bb_col.insert({"skuid":skuid,"data":obj})

def extract_meta():
    ram_md_folder = "memory"
    for fname in os.listdir(ram_md_folder):
        if not fname.endswith("json"):
            continue
        skuid = fname[:-5]
        try:
            metadata = es_bb(skuid)
            bb_col.update(
                {"skuid":skuid},
                {"$set":{"metadata":metadata}})
        except Exception as e:
            print e

def try_search():
    pin_v = 240
    type_v = "DDR3"
    freq_v = 1333
    cap_v = 4

    """
    pin_v = 288
    type_v = "DDR4"
    freq_v = 2133
    cap_v = 4
    """

    res = bb_col.find({
        "metadata.pin":pin_v,
        "metadata.type":type_v,
        "metadata.freq":freq_v,
        "metadata.capacity":cap_v})

    for i in res:
        print i

def update_metadata(skuid):

    try:
        metadata = es_bb(skuid)
        bb_col.update(
            {"skuid":skuid},
            {"$set":{"metadata":metadata}})
    except Exception as e:
        print "bad", skuid

def update_metadata_all():
    skuid_list = []
    for bb in bb_col.find():
        skuid_list.append( bb['skuid'] )
    for skuid in skuid_list:
        update_metadata(skuid)

if __name__ == '__main__':
    #import_ram()
    #extract_meta()
    try_search()
