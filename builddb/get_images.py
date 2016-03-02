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

def fill_images_one(model):
    im_list = []
    for db_info in db_info_list:
        if db_info['website'] == 'crucial':
            # no image crawled
            continue

        m = db_info['col'].find_one( {db_info['mf']:model} )
        if not m:
            continue
        try:
            if db_info['website'] == 'amazon':
                if m.has_key('imUrl'):
                    im_list.append(m['imUrl'])
        except Exception as e:
            print 'amazon', e

        try:
            if db_info['website'] == 'newegg':
                for im_info in m['data']['newegg_product']['main_images']:
                    im_list.append(im_info['location'])
        except Exception as e:
            print 'newegg', e

        try:
            if db_info['website'] == 'bestbuy':
                im_list.append(m['data']['image'])
        except Exception as e:
            print 'bestbuy', e

    prod_col.update(
        {'model':model},
        {'$set':{'metadata.imgs':im_list}})

def extract_images():
    """
    For each product, get the images
    """
    model_list = []
    for p in prod_col.find():
        model_list.append(p['model'])
    for model in model_list:
        fill_images_one(model)


if __name__ == '__main__':
    extract_images()
    #fill_images_one("B4U36AA-PE")
    #fill_images_one("F3-12800CL9T-6GBNQ")

