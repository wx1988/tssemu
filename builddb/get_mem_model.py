import pickle

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.ram
newegg_col = db.newegg
bb_col = db.bestbuy
az_col = db.amazon
prod_col = db.products

def populate_mem_model_newegg():
	mlist = []
	for ni in newegg_col.find({"metadata.model":{"$exists":True}}):
		model = ni['metadata']['model']
		mlist.append(model)

		# insert into db
		p = prod_col.find_one({"model":model})
		if not p:
			# insert
			prod_col.insert({
				"model":model,
				"websites":[{"website":"newegg", "id":ni['neweggid']}]
				})
		else:
			# check whether the current product is inserted
			website_names = [w['website'] for w in p['websites']]
			if not "newegg" in website_names:
				tmp_websites = p['websites']
				tmp_websites.append({"website":"newegg", "id":ni['neweggid']})
				prod_col.update(
					{"model":model}, 
					{"$set": {"websites":tmp_websites}})		
	print len(mlist)
	return mlist

def populate_mem_model_bestbuy():
	mlist = []
	for ni in bb_col.find({"metadata.model":{"$exists":True}}):
		model = ni['metadata']['model']
		mlist.append( model )

		# insert into db
		p = prod_col.find_one({"model":model})
		if not p:
			# insert
			prod_col.insert({
				"model":model,
				"websites":[{"website":"bestbuy", "id":ni['skuid']}]
				})
		else:
			# check whether the current product is inserted
			website_names = [w['website'] for w in p['websites']]
			if not "bestbuy" in website_names:
				tmp_websites = p['websites']
				tmp_websites.append({"website":"bestbuy", "id":ni['skuid']})
				prod_col.update(
					{"model":model}, 
					{"$set": {"websites":tmp_websites}})

	print len(mlist)	
	return mlist

def get_all_mem_model():
	mlist = []
	for p in prod_col.find():
		mlist.append( p['model'] )
	return mlist


def search_amazon():
	"""
	only 187 products are search out
	"""
	mlist = get_all_mem_model()
	# for each model, use full text search	
	print len(mlist)
	m2asin = {}
	gc = 0
	for i,m in enumerate(mlist):
		if i % 100 == 0:
			print "done with ", i

		tmp_reg = ".*%s.*"%(m)
		o = az_col.find_one({"description":{"$regex":tmp_reg}})
		#print m, o		
		if o:
			gc += 1
			m2asin[m] = o['asin']
	print gc
	pickle.dump(m2asin, open("m2asin.pkl","w"))

def populate_amazon():
	m2asin = pickle.load(open("m2asin.pkl"))
	for model in m2asin.keys():
		p = prod_col.find_one({"model":model})

		website_names = [w['website'] for w in p['websites']]
		if not "amazon" in website_names:
			tmp_websites = p['websites']
			tmp_websites.append({"website":"amazon", "id":m2asin[model]})
			prod_col.update(
				{"model":model}, 
				{"$set": {"websites":tmp_websites}})

if __name__ == "__main__":	
	#get_mem_model_newegg()
	#get_mem_model_bestbuy()
	#search_amazon()
	populate_amazon()