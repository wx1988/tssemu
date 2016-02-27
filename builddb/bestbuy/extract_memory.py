"""
name containing DDR and memory
"""

import os
import json

def extract_memory():
	prod_dir = "products"
	memory_dir = "memory"
	memory_list = []
	for fname in os.listdir(prod_dir):
		prod_path = "%s/%s"%(prod_dir, fname)
		prod_list = json.load( open(prod_path) )
		for prod in prod_list:
			out_path = "%s/%d.json"%(memory_dir, prod['sku'])
			if os.path.isfile(out_path):
				continue
			if prod.has_key('name'):
				name = prod['name']
				if name == None:
					continue
				name = name.lower()
				if name.count("memory") > 0 and name.count('ddr') > 0:
					json.dump(prod, open(out_path,'w'))
	
if __name__ == "__main__":
	extract_memory()
