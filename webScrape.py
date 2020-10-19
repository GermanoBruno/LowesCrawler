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
	# Função para abrir uma janela do navegador na url dada

	# Caminhos do sistema para os binarios do webdriver e do navegador
	binary = FirefoxBinary("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
	driver = webdriver.Firefox(firefox_binary=binary, executable_path=r"C:\\geckodriver.exe")
	print("Vai abrir: " + url)
	driver.get(url)
	return driver

# Recebe a url do catalogo, retorna lista das urls e nome das categorias
def listCategoryUrl(catalogUrl):
	# Função pra pegar a url das categorias, dado a url do catalogo
	driver = openBrowser(catalogUrl)

	# grid-16 é a classe da div de cada categoria
	categories = driver.find_elements_by_class_name('grid-16')

	listCategoryName = []
	listCategoryUrl = []

	for category in categories:
		categoryName = category.text
		# buscar o link de cada categoria
		categoryUrl = category.find_element_by_css_selector('a').get_attribute('href')

		listCategoryName.append(categoryName)
		listCategoryUrl.append(categoryUrl)

	# fechar o navegador
	driver.quit()
	#sessionCookies = driver.get_cookies()''
	return listCategoryName, listCategoryUrl

# recebe o numero da pagina, retorna o numero do offset
def setOffset(pageNum):

	return pageNum*36

# Recebe a url da categoria,o nome e o catalogo
# append no catalogo os produtos novos achados
def getCategoryProducts(categoryUrl, categoryName, catalog):
	driver = openBrowser(str(categoryUrl))
	soup = BeautifulSoup(str(driver.page_source), 'lxml')
	driver.close()
	productQtt = soup.find('div', class_='sc-1hnzoos-1 gEhtWF')
	if(productQtt != None):
		productQtt = productQtt.contents[0].split(' ')[0]
	else:
		return
	

	page = 0
	offset = setOffset(page)
	pageUrl = categoryUrl
	while(offset < int(productQtt)):
		getPageProducts__(pageUrl, categoryName, catalog)
		page = page+1
		offset = setOffset(page)
		pageUrl = pageUrl.split('?')[0] + "?offset=" + str(offset)

# Recebe lista com todas as urls de categoria e retorna todos os refrigeradores (das primeira paginas)
def getPageProducts(listCategoryUrl, categoryName):

	#listProductName = []
	refrigeratorList = Catalog()
	for site, categoriaAtual in zip(listCategoryUrl, categoryName):
		driver = openBrowser(str(site))
		#driver = openBrowser(str(site) + "?offset=" + str(offset))

		categoriaUsada = categoriaAtual

		#driver = openBrowser(str(listCategoryUrl[0]))
		#categoriaUsada = categoryName[0]

		soup = BeautifulSoup(str(driver.page_source), 'lxml')
		driver.close()
		'''
		child_element =  WebDriverWait(driver,10).until(
	    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/section/div/div[3]/div[2]/div/div[2]/div/div/div[47]/ul/li[7]/a"))
		)
		link = driver.find_element_by_xpath("/html/body/div[1]/div[2]/section/div/div[3]/div[2]/div/div[2]/div/div/div[47]/ul/li[7]/a")
		print(link)
		'''
		# sc-3tdioj-0 bbzAql pl-column é a classe da div de cada produto
		productList = soup.find_all('div', class_='sc-3tdioj-0 bbzAql pl-column')
		# sc-1b7wdu0-9 cjoVtZ é a classe do span da marca
		brandList = soup.find_all('span', class_='sc-1b7wdu0-9 cjoVtZ') 
		# sc-1b7wdu0-8 ePVQHM é a classe do article nome
		nameList = soup.find_all('article', class_='sc-1b7wdu0-8 ePVQHM')
		# tooltip-custom é a classe do span do SKU e do Model
		skuAndModel = soup.find_all('span', class_='tooltip-custom')
		productQtt = soup.find('div', class_='sc-1hnzoos-1 gEhtWF')

		totalProductQtt = productQtt.contents[0].split(' ')[0]
		print(totalProductQtt)
		#input('Só isso chapa')
		
		skuList = skuAndModel[0::2]
		modelList = skuAndModel[1::2]




		'''	print('sku: ' + str(len(skuList)))
		print('brand' + str(len(brandList)))
		print('name' + str(len(nameList)))
		print('model' + str(len(modelList)))
		print('product' + str(len(productList)))
		'''

		for (product, name, sku, brand, model) in zip(productList, nameList, skuList, brandList, modelList):
			urlFound = 'https://www.lowes.com' + product.find('a')['href']
			nameFound =  name.contents[1] or None
			brandFound = brand.contents[0]
			modelFound = model.contents[-1].split('#')[-1]
			skuFound = sku.contents[-1].split('#')[-1]
			'''print(urlFound)
			print(brandFound)
			print(nameFound)
			print(skuFound)
			print(modelFound)
			print('\n')'''
			
			newRefrigerator = Refrigerator(urlFound, brandFound, nameFound, skuFound, modelFound)
			#passar categoria aqui
			newRefrigerator.appendCategory(categoriaUsada)

			refrigeratorList.appendToCatalog(newRefrigerator)
			#ADICIONAR O OBJETO NA LISTA


	return refrigeratorList

# recebe uma pagina e sua categoria e coloca no catalogo os refrigeradores dela
def getPageProducts__(pageUrl, categoryName, catalog):

	driver = openBrowser(str(pageUrl))
	soup = BeautifulSoup(str(driver.page_source), 'lxml')
	driver.close()

	# sc-3tdioj-0 bbzAql pl-column é a classe da div de cada produto
	productList = soup.find_all('div', class_='sc-3tdioj-0 bbzAql pl-column')
	# sc-1b7wdu0-9 cjoVtZ é a classe do span da marca
	brandList = soup.find_all('span', class_='sc-1b7wdu0-9 cjoVtZ') 
	# sc-1b7wdu0-8 ePVQHM é a classe do article nome
	nameList = soup.find_all('article', class_='sc-1b7wdu0-8 ePVQHM')
	# tooltip-custom é a classe do span do SKU e do Model
	skuAndModel = soup.find_all('span', class_='tooltip-custom')
	
	skuList = skuAndModel[0::2]
	modelList = skuAndModel[1::2]

	for (product, name, sku, brand, model) in zip(productList, nameList, skuList, brandList, modelList):
		if(not catalog.searchSku(sku)):
			urlFound = 'https://www.lowes.com' + product.find('a')['href']
			nameFound =  name.contents[1] or None
			brandFound = brand.contents[0]
			modelFound = model.contents[-1].split('#')[-1]
			skuFound = sku.contents[-1].split('#')[-1]

			newRefrigerator = Refrigerator(urlFound, brandFound, nameFound, skuFound, modelFound)
			newRefrigerator.appendCategory(categoryName)

			catalog.appendToCatalog(newRefrigerator)
			#catalog.printCatalog()
			#input("colocou o primeiro")

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