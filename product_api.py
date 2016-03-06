"""

# Function group 1
Given a product id,
get the specification
get all the sellers and price

# Function group 2
Given a specification,
get all matching products
"""
import numpy as np
import os
import json

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.ram
prod_col = db.products
az_col = db.amazon
newegg_col = db.newegg
bb_col = db.bestbuy
cru_col = db.crucial_mem

from builddb.crucial.get_compatmem_by_machine import get_cm_list_mp

def get_prod_by_model(model):
    m = prod_col.find_one({'model':model})

    return m

def get_vote(vlist):
    tdic = {}
    for v in vlist:
        if not tdic.has_key(v):
            tdic[v] = 0
        tdic[v] += 1
    bk = tdic.keys()[0]
    for k in tdic.keys():
        if tdic[k] > tdic[bk]:
            bk = k
    return bk

def get_match_prod(sys_info):
    # find memory by memory model
    model_list = []
    for mem in sys_info['mem_list']:
        if mem.has_key('model'):
            model_list.append( mem['model'].strip() )
    model_list = list(set(model_list))

    exact_mem_res_list = []
    for model in model_list:
        res = get_prod_by_model(model)
        if res:
            exact_mem_res_list.append(res)

    # Suggestion based on the memory vendors
    # find memory by machine model
    mem_list_by_machine = get_cm_list_mp(
        sys_info['manufacturer'],
        sys_info['productname'])
    print 'from crucial recommendation', len(mem_list_by_machine)
    crucial_recommend_model_list = [ mem['model'] for mem in mem_list_by_machine]

    # find other compatible memory based on the voting
    search_spec = {}
    if len(sys_info['mem_list']) >0:
        search_spec = { 'metadata.freq':sys_info['mem_list'][0]['speed']}

    # type, reg, ecc, pin
    if len(mem_list_by_machine) == 0:
        # TODO, a bad thing
        raise Exception("TODO, crucial recommendation zero")
    else:
        # vote to get the right specification
        if not search_spec.has_key('metadata.freq'):
            search_spec['metadata.freq'] = get_vote([mem['metadata']['freq'] for mem in mem_list_by_machine if mem['metadata'].has_key('freq') ] )
        search_spec['metadata.type'] = get_vote([mem['metadata']['type'] for mem in mem_list_by_machine if mem['metadata'].has_key('type') ] )
        search_spec['metadata.reg'] = get_vote([mem['metadata']['reg'] for mem in mem_list_by_machine if mem['metadata'].has_key('reg') ] )
        search_spec['metadata.ecc'] = get_vote([mem['metadata']['ecc'] for mem in mem_list_by_machine if mem['metadata'].has_key('ecc') ])
        search_spec['metadata.pin'] = get_vote([mem['metadata']['pin'] for mem in mem_list_by_machine if mem['metadata'].has_key('pin') ])
    print search_spec

    spec_mem_list = [m for m in prod_col.find(search_spec)]
    for i in range(len(spec_mem_list)):
        # make json stringfy able
        spec_mem_list[i]['_id'] = str(spec_mem_list[i]['_id'])
        if spec_mem_list[i]['metadata'].has_key('_id'):
            spec_mem_list[i]['metadata']['_id'] = str(spec_mem_list[i]['metadata']['_id'])

        # special feature
        if spec_mem_list[i]['model'] in crucial_recommend_model_list:
            spec_mem_list[i]['feature'] = "crucial_recommend"
        if spec_mem_list[i]['model'] in model_list:
            spec_mem_list[i]['feature'] = "same_as_old"

    print len(spec_mem_list)

    # NOTE, return a bunch of information for next suggestion stage
    spec_mem_list = post_process(spec_mem_list)
    return spec_mem_list, search_spec

def get_prod_by_spec(spec_dic):
    spec_mem_list = [m for m in prod_col.find(spec_dic)]

    for i in range(len(spec_mem_list)):
        # make json stringfy able
        spec_mem_list[i]['_id'] = str(spec_mem_list[i]['_id'])
        if spec_mem_list[i]['metadata'].has_key('_id'):
            spec_mem_list[i]['metadata']['_id'] = str(spec_mem_list[i]['metadata']['_id'])

    # filter by price information
    def check_price(mem):
        good = False
        for web_info in mem['websites']:
            if web_info.has_key('price') and web_info['price']:
                return True
        return good

    new_res = []
    for mem in spec_mem_list:
        if not check_price(mem):
            continue
        new_res.append(mem)
    new_res = post_process(new_res)
    return new_res

def post_process(prod_list):
    prod_list = fill_review(prod_list)
    prod_list = fill_prod_url(prod_list)
    return prod_list

def fill_prod_url(prod_list):
    for i,prod in enumerate(prod_list):
        for j, web_info in enumerate(prod['websites']):
            print web_info
            if web_info['website'] == "newegg":
                prod_list[i]['websites'][j]['url'] = "http://www.newegg.com/Product/Product.aspx?Item="+web_info['id']
            if web_info['website'] == "amazon":
                prod_list[i]['websites'][j]["url"] = "http://amazon.com/dp/"+web_info['id']
            if web_info['website'] == "bestbuy":
                prod_list[i]['websites'][j]["url"] = "http://www.bestbuy.com/site/t/%s.p?skuId=%s"%(str(web_info['id']), str(web_info['id']))
            if web_info['website'] == "crucial":
                # find the memory in curcial database based on model
                c = cru_col.find_one({'model':prod['model']})
                if c:
                    prod_list[i]['websites'][j]["url"] = c['url']
    return prod_list                

def fill_review(prod_list):
    """
    Summary of review here
    """
    source_col_list = [az_col ,newegg_col , bb_col]
    for prod in prod_list:
        modelname = prod['model']
        rscore_list = []
        for sc in source_col_list:
            p = sc.find_one({"metadata.model":modelname})
            if p and p.has_key('review'):
                rscore_list.extend( p['review']['rscore_list'] )
        prod['review_num'] = len(rscore_list)
        if len(rscore_list) == 0:
            prod['mean_review'] = 0
        else:
            prod['mean_review'] = np.mean(rscore_list)
    return prod_list



def test_get_match_prod():
    #sys_info = {u'mem_list': [{u'capacity': 4096, u'model': u'HMA451R7MFR8N-TF ', u'type': u'Other', u'detail': u'Synchronous', u'speed': 2133}, {u'capacity': 4096, u'model': u'HMA451R7MFR8N-TF ', u'type': u'Other', u'detail': u'Synchronous', u'speed': 2133}, {u'capacity': 4096, u'model': u'HMA451R7MFR8N-TF ', u'type': u'Other', u'detail': u'Synchronous', u'speed': 2133}, {u'capacity': 4096, u'model': u'HMA451R7MFR8N-TF ', u'type': u'Other ', u'detail': u'Synchronous', u'speed': 2133}], u'manufacturer': u' Dell Inc.', u'slots': 8, u'maximum_capacity': 256, u'productname': u' Precision Tower 5810'}
    sys_info = {"mem_list": [{"type": "DDR3", "model": "HMT451R7AFR8C-RD  ", "capacity": 4096, "detail": "Registered ", "speed": 1866}, {"type": "DDR3", "model": "HMT451R7AFR8C-RD  ", "capacity": 4096, "detail": "Registered ", "speed": 1866}], "slots": 8, "productname": " Precision T3610", "maximum_capacity": 128, "manufacturer": " Dell Inc."}
    print get_match_prod(sys_info)

if __name__ == "__main__":
    #print get_match_prod()
    test_get_match_prod()

"""
    tmp_res = [
{
'model':'CT4K4G4RFS8213',
'brand':'Crucial',
'imgs':[
    'http://pisces.bbystatic.com/image2/BestBuy_US/images/mp/products/1312/1312976/1312976564/1312976564_1000x1000_sd.jpg;canvasHeight=500;canvasWidth=500',
    'http://images17.newegg.com/is/image/newegg/20-148-841-TS?$S640$'],
'rate':0,
'unit':'4*4',

'sellerlist':[
    {
        'source':'Amazon',
        'id':'B00KUSMTW4',
        'sellerid':'2529211011',
        'sellername':'Crucial',
        'price':153.03,
        'left':'5'
        },
    {
        'source':'Newegg',
        'id':'9SIA24G28N3012',
        'sellerid':'antonline-com',
        'sellername':'antonline-com',
        'price':148.2,
        'left':'-1'
        },
    {
        'source':'BestBuy',
        'id':'1312976564',
        'sellerid':'6006839520005',
        'price':152.3,
        'left':'-1'
    }
]


},

{
'model':'KVR21R15S8K4/16',
'brand':'Kingston',
'rate':0,
'imgs':[],
'unit':'4*4',

'sellerlist':[
    {
    'source':'Newegg',
    'id':'N82E16820242104',
    'sellerid':'newegg',
    'price':133.4,
    },
    {
        'source':'Amazon',
        'id':'B00X60MU68',
        'sellerid':'11351297011',
        'sellername':'Kingston Technology',
        'price':142.84,
        }
]
},

{
'model':'HMA451R7MFR8N-TF',
'brand':'hynix',
'imgs':['http://ecx.images-amazon.com/images/I/717CGJn1%2BhL._SX522_.jpg'],
'rate':0,
'unit':'1*4',

'sellerlist':[
    {
    'source':'Amazon',
    'id':'B00SK7NMD2',
    'sellerid':'8318979011',
    'sellername':'GoldenRAM',
    'price':29.95,
    'left':1,
    }
]

},

]
"""
