#coding: utf-8

class Refrigerator():
	def __init__(self, originalUrl, brand, title, sku, model):
			self.originalUrl = originalUrl
			self.brand = brand
			self.title = title
			self.sku = sku
			self.model = model
			self.categories = []

	def __str__(self):
		rep = ("Brand: " + self.brand + "\nName: " + self.title + "\nSku: "
			   + self.sku + "\nModel: " + self.model + "\nUrl: " + self.originalUrl)
		return rep

	def categoriesToString(self):
		# substituir as virgulas por ponto e virgulas para exibicao no CSV
		rep = str(self.categories).replace(',', ';')
		return rep

	def toArray(self):
		rep = [self.brand, self.title, self.sku, self.model, self.originalUrl, str(self.categories)]
		return rep

	def showCategories(self):
		print(self.categories)


	def appendCategory(self, category):
		self.categories.append(category)

	def getSku(self):
		return self.sku

	def getUrl(self):
		return self.originalUrl

class Catalog():
	def __init__(self):
		self.productList = []
		self.productSku = []

	def printCatalog(self):
		rep = ''
		for product in self.productList:
			print(product)
	
	def appendToCatalog(self, product):
		self.productList.append(product)
		self.productSku.append(product.getSku)

	def getProductList(self):
		return self.productList

	def searchSku(self, searching):
		for sku, product in zip(self.productSku, self.productList):
			if(sku == searching):
				return product
		return None