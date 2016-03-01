"""

# Function group 1
Given a product id, 
get the specification
get all the sellers and price

# Function group 2
Given a specification, 
get all matching products
"""

import os
import simplejson


def get_match_prod():
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
    return tmp_res

def get_prod_info():
    res = get_match_prod()
    return res[0]

def get_review():
    pass

if __name__ == "__main__":
    print get_match_prod()
