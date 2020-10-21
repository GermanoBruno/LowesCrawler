#coding: utf-8

"""
	NOTAS DE DESENVOLVIMENTO

	Ao que parece, só pegar o get toda vez não vai funcionar. Talvez eu tenha que ir clicando em tudo mesmo, um por um...
	Aprender como abre link desse jeito e testar

	Abrindo e fechando o webdriver funciona... mas é bem demorado

	Feito: 	pegar os links das categorias de geladeiras
			pegar os links das geladeiras individualmente
		 	pegar os dados (nome, sku e link)

	Todo: 	conseguir abrir direito elas
			aprender a "passar página"
			SKU tá vindo duplicado com o modelo (o modelo cai como o SKU do proximo item)
			evitar duplicatas
			pegar mais dados
			passar a categoria
			agregar categoria, caso seja duplicata

"""

import requests as req
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from classes import *

#driver = webdriver.Firefox(firefox_binary=binary, executable_path=r"C:\\geckodriver.exe")

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
		repeatedProduct = catalog.searchSku(sku)
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
			#input("Pode ir dormir, chapa")

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

# NAO IMPLEMENTADO AINDA
def getProductData(product):
	# Product é um Refrigerator

	driver = openBrowser(product.getUrl())
	soup = BeautifulSoup(str(driver.page_source), 'lxml')
	driver.implicitly_wait(10)
	driver.save_screenshot('ss.png')
	driver.close()

	price = soup.find('div', class_='sc-fznMnq biVOqy')

	print(price)


#catalog = Catalog()
#nameList, urlList = listCategoryUrl('https://www.lowes.com/c/Refrigerators-Appliances')

#getCategoryProducts(urlList[6], nameList[6], catalog)

#print(urlList)


#nameList, urlList = listCategoryUrl('https://www.lowes.com/c/Refrigerators-Appliances')
#for url, name in zip(urlList, nameList):#
#	getCategoryProducts(url, name, catalog)

#geladeiras = getPageProducts(urlList, nameList).getProductList()
#getProductData(geladeiras[0])


'''
for geladeira in geladeiras:
	print(geladeira)
	print('')
'''

# Printar um dict com os links e nomes das categorias (só pra conferir) 
#print(dict(zip(nameList, urlList)))

#for url in urlList:
#print('https://www.lowes.com/pl/French-door-refrigerators-Refrigerators-Appliances/4294857963')
#print(urlList[0])
#for url in urlList:
#driver = openBrowser(str(urlList[0]))




""" TENTANDO PEGAR A SETA
driver = openBrowser(str(urlList[0]))
driver.implicitly_wait(5)
soup = BeautifulSoup(str(driver.page_source), 'lxml')
driver.close()
arrowLink = soup.find(name='div', class_='k0dn21-0 jSQPlH')

print(arrowLink)
"""


#arrowLink = driver.find_element(By.CSS_SELECTOR, '[class ="k0dn21-0 jSQPlH"]')
#arrowLink = soup.find('div', class_='k0dn21-0 jSQPlH')
#print(arrowLink)
#arrowLink.contents = arrowLink.find(class_='sc-AxirZ hylFqS arrow false')
#print(arrowLink)


# seta pra proxima pagina
# PEGAR O HREF
# <a>, 
# SE DISPONIVEL
#class='sc-AxirZ hylFqS arrow false'
# aria-label= 'arrow right'
# SE INDISPONIVEL
#sc-AxirZ hylFqS arrow disabled
# aria-label= 'arrow right'

# seta anterior
# <a>, 
# SE DISPONIVEL
# aria-label= 'arrow left'
# class='sc-AxirZ hylFqS arrow false'
# SE INDISPONIVEL
# aria-label= 'arrow left'
# class='sc-AxirZ hylFqS arrow disabled'






#driver.implicitly_wait(5)
"""
soup = BeautifulSoup(str(driver.page_source), 'lxml')
productList = soup.find_all('div', class_='sc-3tdioj-0 bbzAql pl-column')
nameList = soup.find_all('article', class_='sc-1b7wdu0-8 ePVQHM')
skuList = soup.find_all('span', class_='tooltip-custom')
driver.close()"""

#for product in productList:
#	urlFound = product.find('a')
#	print(urlFound['href'])
#urlFound = productList[0].find('a')['href']

#urlFound = 'https://www.lowes.com' + str(urlFound)
#print(nameList[0].contents[1])
#print(skuList[0].contents[2])
#print(urlFound)

#driver = openBrowser(urlFound)
#soup = BeautifulSoup(str(driver.page_source), 'lxml')

#driver.close()
# sc-1b7wdu0-8 ePVQHM é a classe do article nome
# tooltip-custom é a classe do span do SKU


# Achar itens


#print(product)


#content = driver.find_elements_by_class_name('sc-3tdioj-0 bbzAql pl-column')


### PAREI AQUI ###

# Tenta pegar a div com classe desse nome estranho, que é onde tão os itens de cada geladeira
# Não tá achando o elemento, então tem que ver isso ai
#print(driver.page_source)
#print("passou uma")

#driver.quit()


#print(content.text) 

'''

class Category():
	def __init__(self, name, url):
			self.name = name
			self.url = url
'''