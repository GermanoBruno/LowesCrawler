#coding: utf-8

#import requests as req
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

from classes import *

def openBrowser(url):
	##########
	# Param: an URL
	#
	# Returns: open webdriver on that URL
	##########


	# Função para abrir uma janela do navegador na url dada

	# Caminhos do sistema para os binarios do webdriver e do navegador
	binary = FirefoxBinary("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
	driver = webdriver.Firefox(firefox_binary=binary, executable_path=r"C:\\geckodriver.exe")
	
	# Debug Helper
	print("Vai abrir: " + url)

	driver.get(url)

	# poderia retornar o soup da pagina e fechar o browser, mas assim poderia
	# causar conflito com implementações futuras que precisem do webdriver aberto

	return driver

def listCategoryUrl(catalogUrl):
	##########
	# Param: an URL for the catalog of categories
	#
	# Returns: list of category names
	# 		   list of category urls
	##########


	# Nessa função, por ser a primeira que roda e só rodar uma vez,
	# usei as ferramentas de achar elementos do próprio webdriver.
	# Nunca tinha usado então quis testar e ver como se comportavam :)
	

	binary = FirefoxBinary("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
	driver = webdriver.Firefox(firefox_binary=binary, executable_path=r"C:\\geckodriver.exe")
	driver.get(catalogUrl)
	#driver = openBrowser(catalogUrl)

	# A classe especificada identifica as categorias no catalogo
	categories = driver.find_elements_by_class_name('grid-16')

	# inicializa as listas que serao utilizadas
	listCategoryName = []
	listCategoryUrl = []

	# itera em todas as categorias encontradas para achar o nome e o link
	for category in categories:
		categoryName = category.text
		# Buscar o link de cada categoria
		categoryUrl = category.find_element_by_css_selector('a').get_attribute('href')

		listCategoryName.append(categoryName)
		listCategoryUrl.append(categoryUrl)

	# Fecha o navegador
	driver.quit()

	return listCategoryName, listCategoryUrl

def setOffset(pageNum):
	##########
	# Param: the current page number
	#
	# Returns: the offset for the given page
	##########
	return pageNum*36

def getPageProducts(pageUrl, categoryName, catalog):
	##########
	# 	Params: an url for the product list page
	#			the name of the category of those products
	#			the Catalog object of the current execution of the program
	#
	# 	gets all the products on a given page and add their data to
	#	the catalog 
	##########

	driver = openBrowser(str(pageUrl))
	soup = BeautifulSoup(str(driver.page_source), 'lxml')
	driver.close()

	# A classe especificada é a identificadora da div contendo cada produto
	productList = soup.find_all('div', class_='sc-3tdioj-0 bbzAql pl-column')
	# A classe especificada é a identificadora do span contendo a marca
	brandList = soup.find_all('span', class_='sc-1b7wdu0-9 cjoVtZ') 
	# A classe especificada é a identificadora do article contendo o nome
	nameList = soup.find_all('article', class_='sc-1b7wdu0-8 ePVQHM')
	# A classe especificada é a identificadora do span contendo o SKU e o Model
	skuAndModel = soup.find_all('span', class_='tooltip-custom')
	
	# Separa a lista de SKU da de Modelos
	skuList = skuAndModel[0::2]
	modelList = skuAndModel[1::2]

	for (product, name, sku, brand, model) in zip(productList, nameList, skuList, brandList, modelList):
		repeatedProduct = catalog.searchSku(str(sku))
		if( repeatedProduct == None):
			urlFound = 'https://www.lowes.com' + product.find('a')['href']
			nameFound =  name.contents[1] or None
			brandFound = brand.contents[0]
			# Se certifica que pega o sku e o modelo no formato correto,
			# visto que há inconsistência nos dados do site
			modelFound = model.contents[-1].split('#')[-1]
			skuFound = sku.contents[-1].split('#')[-1]

			newRefrigerator = Refrigerator(urlFound, brandFound, nameFound, skuFound, modelFound)
			newRefrigerator.appendCategory(categoryName)

			catalog.appendToCatalog(newRefrigerator)
		else:
			print("Achou uma duplicata")
			if(categoryName not in catalog.getProductList()):
				repeatedProduct.appendCategory(categoryName)
				print("Adicionou a categoria nova")
				print(repeatedProduct.showCategories())
			else:
				print("a categoria ja esta inclusa")

def getCategoryProducts(categoryUrl, categoryName, catalog):
	##########
	# 	Params: an URL for a category
	#			the name for this category
	#			the Catalog object of the current execution of the program
	#
	#	gets all the products on a given category and adds them
	#	to the catalog object
	##########

	driver = openBrowser(str(categoryUrl))
	soup = BeautifulSoup(str(driver.page_source), 'lxml')
	driver.close()

	# A classe especificada identifica o o numero de produtos na categoria
	productQtt = soup.find('div', class_='sc-1hnzoos-1 gEhtWF')

	if(productQtt != None):
		# Separa o texto da quantidade de produtos e pega o numero
		productQtt = int(productQtt.contents[0].split(' ')[0])
	else:
		# Debug Helper
		print("Erro na leitura da pagina da categoria: (" + categoryName + ")")
		return
	
	page = 0
	offset = setOffset(page)
	pageUrl = categoryUrl

	# Tem uns sites que tem ?& na especificacao... 

	if (len(categoryUrl.split('?')) == 1):
		# se existir uma interrogacao na url, significa que existe um filtro nela
		# portanto a adicao da pagina e feita de uma maneira diferente
		while(offset < productQtt):
			getPageProducts(pageUrl, categoryName, catalog)
			page = page+1
			offset = setOffset(page)
			# Adiciona o offset, funcionando como um numero de pagina
			pageUrl = pageUrl.split('?')[0] + "?offset=" + str(offset)
	else:
		if (len(categoryUrl.split('&')) == 1):
			while(offset < productQtt):
				getPageProducts(pageUrl, categoryName, catalog)
				page = page+1
				offset = setOffset(page)
				# Adiciona o offset, funcionando como um numero de pagina
				pageUrl = pageUrl.split('&')[0] + "&offset=" + str(offset)
		else:
			# Para o caso (estranho, mas existente) de algum filtro ser aplicado com ?&
			while(offset < productQtt):
				getPageProducts(pageUrl, categoryName, catalog)
				page = page+1
				offset = setOffset(page)
				# Adiciona o offset, funcionando como um numero de pagina
				if(page > 1):
					# Se passou da primeira página, troca o offset pelo novo
					pageUrl = '&'.join(pageUrl.split('&')[:-1]) + "&offset=" + str(offset)
				else:
					# Se ainda está na primeira página, adiciona o offset na url
					pageUrl = pageUrl + "&offset=" + str(offset)

def getProductData(productUrl):
	##########
	# 	Params: an URL for a product
	#
	#	gets all the data on a given product and returns it
	#	as a dict
	##########

	driver = openBrowser(productUrl)

	try:
		# Procura o elemento specifications, para checar se nao houve
		# algum erro de carregamento na pagina
		specButton = driver.find_element_by_id('Specifications')
		specButton.click()
		soup = BeautifulSoup(str(driver.page_source), 'lxml')
		driver.close()
	except NoSuchElementException:
		print("Dados de ", productUrl, " nao disponiveis")
		driver.close()
		return None

	# Pega os dados da tabela
	table = soup.find('div', class_='styles__SpecificationWrapper-t8ysf8-2 fbGflN')
	tableRows = table.find_all('div', class_='tr')

	specsDict = {}
	# Processa os dados da tabela
	for row in tableRows:
		key = row.find('div', class_='key').contents[0]
		# Ignora o item especifico de warnings para evitar erro de leitura
		if(str(key) != 'CA Residents: Prop 65 Warning(s)'):
			#print(key)
			value = row.find('div', class_='value').contents[0]
			elementType = type(value)
			navString = "<class 'bs4.element.NavigableString'>"
			# Se o valor do item não é uma string, é uma tag.
			if(str(elementType) != navString):
				# Usa o alt da tag para pegar o valor 'yes' ou 'no'
				value = value['alt']
			specsDict[key] = value
	return specsDict
	