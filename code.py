from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.ram
newegg_col = db.newegg

import os
import web, json

urls=(
    # pages
    '/', 'index',
    '/view_product', 'view_product',
    '/list_product', 'list_product',
    '/compare', 'compare_products', # compare two or three products

    # POST service
    '/suggest', 'suggest',

    # interactive cralwer
    '/getnextid', 'getnextid',
    '/receivedoc', 'receivedoc',

    # API
    '/search_product', 'search_product',
    '/prod_info', 'prod_info',
    )

############
# temporary receive doc
###########
class getnextid:
    def GET(self):
        for n in newegg_col.find():
            ni = n['neweggid']
            outpath = "neweggreview/%s.html"%(ni)
            if os.path.isfile(outpath):
                continue
            return json.dumps({'newegg_id':ni})
        return json.dumps({})


class receivedoc:
    def POST(self):
        d = web.input()
        content =  d['data']
        url = d['url']
        ni = url[url.rindex('=')+1:]
        outpath = "neweggreview/%s.html"%(ni)
        if os.path.isfile(outpath):
            return {'status':'exist'}
        with open(outpath,'w') as f:
            content = content.encode('ascii','ignore')
            print>>f, content
        return {'status':'good'}


#############
# HTML
#############

class index:
    def GET(self):
        render = web.template.render('templates/', base="base")
        return render.index()


class list_product:
    def GET(self):
        render = web.template.render('templates/', base="base")
        return render.list_product()


class view_product:
    def GET(self):
        render = web.template.render('templates/', base="base")
        return render.view_product()

class compare_products:
    def GET(self):
        render = web.template.render('templates/', base="base")
        return render.compare_products()

#############
# Post page
#############
class suggest:
    def GET(self):
        """
        get all compatible products,
        group them based on the upgrading
        """
        d = web.input()
        sys_info = json.loads( d['sys_info'] )
        print sys_info
        return sys_info


#############
# RESTFUL API
#############

class prod_info:
    def GET(self):
        from product_api import get_prod_info
        res = get_prod_info()
        res_dic = {'status':0, 'data':res}
        return json.dumps(res_dic)

class search_product:
    def GET(self):
        from product_api import get_match_prod
        tmp_res = get_match_prod()
        res = {'status':0, 'data':tmp_res}
        return json.dumps(res)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
