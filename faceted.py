"""
get all faceted data
"""
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.ram
faceted = db.faceted
prod_col = db.products

def bulk_create():
	mn2vlist = {}
	single_meta_name_list = ['pin', 'freq', 'type','brand']
	# reg, ecc, only true and false
	# capacity * number
	for mn in single_meta_name_list:
		mn2vlist[mn] = []
	mn2vlist['reg'] = [True, False]
	mn2vlist['ecc'] = [True, False]
	mn2vlist['cn'] = []

	for p in prod_col.find():
		for mn in single_meta_name_list:
			if p['metadata'].has_key(mn):
				mn2vlist[mn].append( p['metadata'][mn] )
		if p['metadata'].has_key('capacity') and p['metadata'].has_key('number'):
			if p['metadata']['capacity'] == int(p['metadata']['capacity']):
				cn_str = "%d*%d"%(p['metadata']['number'], p['metadata']['capacity'])
				mn2vlist['cn'].append(cn_str)

	for mn in mn2vlist.keys():
		mn2vlist[mn] = list(set(mn2vlist[mn]))
	faceted.insert(mn2vlist)

def get_whole_faceted():
	faceted_info = faceted.find_one()
	del faceted_info['_id']
	return faceted_info

if __name__ == "__main__":
	bulk_create()