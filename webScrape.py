"""
	NOTAS DE DESENVOLVIMENTO

	Ao que parece, só pegar o get toda vez não vai funcionar. Talvez eu tenha que ir clicando em tudo mesmo, um por um...
	Aprender como abre link desse jeito e testar

	Abrindo e fechando o webdriver funciona... mas é bem demorado

	Feito: pegar os links das categorias de geladeiras
	Preciso: conseguir abrir direito elas
			 pegar os dados (primeiramente só os que eu consigo ver na pagina)

"""



import requests as req
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait

def document_initialised(driver):
	return drive.execute_script('return initialised')

# Caminhos do sistema para os binarios do webdriver e do navegador
binary = FirefoxBinary("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
driver = webdriver.Firefox(firefox_binary=binary, executable_path=r"C:\\geckodriver.exe")

def listCategoryUrl(catalogUrl):
	driver.get('https://www.lowes.com/c/Refrigerators-Appliances')
	categories = driver.find_elements_by_class_name('grid-16')

	listCategoryName = []
	listCategoryUrl = []

	for category in categories:
		categoryName = category.text
		categoryUrl = category.find_element_by_css_selector('a').get_attribute('href')

		listCategoryName.append(categoryName)
		listCategoryUrl.append(categoryUrl)
	driver.quit()
	#sessionCookies = driver.get_cookies()''
	return listCategoryName, listCategoryUrl
"""
def listProductUrls():

	listCategoryName = []
	listCategoryUrl = []	

"""

# Printar um dict com os links e nomes das categorias (só pra conferir) 
nameList, urlList = listCategoryUrl('https://www.lowes.com/c/Refrigerators-Appliances')
#print(dict(zip(nameList, urlList)))

#for url in urlList:
#print('https://www.lowes.com/pl/French-door-refrigerators-Refrigerators-Appliances/4294857963')
#print(urlList[0])
#driver.implicitly_wait(10)
#for url in urlList:
driver = webdriver.Firefox(firefox_binary=binary, executable_path=r"C:\\geckodriver.exe")
driver.get(str(urlList[0]))

### PAREI AQUI ###

# Tenta pegar a div com classe desse nome estranho, que é onde tão os itens de cada geladeira
# Não tá achando o elemento, então tem que ver isso ai
content = driver.find_element_by_class_name('sc-3tdioj-0 bbzAql pl-column')
print(content.text)
#print("passou uma")
driver.quit()

#driver.quit()


#print(content.text) 

'''
class Refrigerator():
	def __init__(self, originalUrl, title, sku):
			self.originalUrl = originalUrl
			self.title = title
			self.sku = sku

class Category():
	def __init__(self, name, url):
			self.name = name
			self.url = url
'''