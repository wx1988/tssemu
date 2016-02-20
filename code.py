import web, json

urls=(
	# pages
	'/', 'index',
	'/view_product', 'view_product',
	'/list_product', 'list_product', 
	'/compare', 'compare_products', # compare two or three products


	# API
	'/search_product', 'search_product',
	)

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
# RESTFUL API
#############

class search_product:
	def GET(self):
		return json.dump({})


if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
