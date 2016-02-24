import os
import json
from pymongo import MongoClient

# TODO, connect the db here. write the db configuration in a separate files. 
#from consts import MONGO_DB_HOST, MONGO_DB_USER, MONGO_DB_PASSWD

client = MongoClient('localhost', 27017)
db = client.ram
newegg_col = db.newegg

def import_ram():
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


if __name__ == "__main__":
	import_ram()