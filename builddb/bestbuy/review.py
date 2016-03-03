"""
For each product in our db, get all related reviews
"""
import os
import json
import pickle

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.ram
bb_col = db.bestbuy
bb_review_col = db.bestbuy_review

def get_skuid():
	skuid_list = []
	for bb in bb_col.find():
		skuid_list.append( bb['skuid'] )
	pickle.dump(skuid_list, open('mem_skuid.pkl','w'))

def get_all_skuid():
	skuid_list = []
	for bb in bb_col.find():
		skuid_list.append(int(bb["skuid"]))
	return skuid_list

def import_reviews():
	all_sku = get_all_skuid()
	#print type(all_sku[0])
	all_sku = set( all_sku )


	flist = os.listdir("reviews")
	for fname in flist:
		if not fname.endswith("json"):
			continue
		print fname
		rlist = json.load( open("reviews/%s"%(fname)) ) 
		for r in rlist:
			#print type(r['sku'])
			#break
			if not r['sku'] in all_sku:
				continue
			bb_review_col.insert(r)
			
		#break

def aggregate_reviews():
	skuid_list = pickle.load( open('mem_skuid.pkl','r') )
	for skuid in skuid_list:		
		m = bb_col.find_one({'skuid':skuid})
		#if m.has_key('review'):
		#	continue
		rid_list = []
		rscore_list = []
		for r in bb_review_col.find({'sku':int(skuid)}):
			rid_list.append( str(r['_id']) )
			rscore_list.append( r['rating'] )
		if len(rid_list) == 0:
			continue
		review_dic = {'rid_list':rid_list, 'rscore_list':rscore_list}
		bb_col.update(
			{'skuid':skuid},
			{'$set':{'review':review_dic}})
		print skuid

	

if __name__ == "__main__":
	#get_skuid()	
	#import_reviews()
	aggregate_reviews()


