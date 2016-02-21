import os
import simplejson

def get_match_prod():
    tmp_res = [
{
'source':'Newegg',
'id':'9SIA24G28N3012',
'seller':'antonline-com',
'price':148.2,
'img':'http://images17.newegg.com/is/image/newegg/20-148-841-TS?$S640$',
},
{
'source':'Newegg',
'id':'N82E16820242104',
'seller':'newegg',
'price':133.4,
},

{
'source':'Amazon',
'id':'B00SK7NMD2',
'seller':'8318979011',
'price':29.95,
'attention':'only 1 used',
'img':'http://ecx.images-amazon.com/images/I/717CGJn1%2BhL._SX522_.jpg',
},

{
'source':'BestBuy',
'id':'1312976564',
'seller':'6006839520005',
'price':152.3,
'img':'http://pisces.bbystatic.com/image2/BestBuy_US/images/mp/products/1312/1312976/1312976564/1312976564_1000x1000_sd.jpg;canvasHeight=500;canvasWidth=500'
}

]
    return tmp_res

def get_review():
    pass

if __name__ == "__main__":
    print get_match_prod()
