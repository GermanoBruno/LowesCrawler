"""
	NOTAS DE DESENVOLVIMENTO

	Ao que parece, só pegar o get toda vez não vai funcionar. Talvez eu tenha que ir clicando em tudo mesmo, um por um...
	Aprender como abre link desse jeito e testar

	Abrindo e fechando o webdriver funciona... mas é bem demorado

	Feito: 	Peguei os dados principais
			Peguei todos os catalogos
			Exportei pra csv
		 	

	Todo: 	Arrumar a passada de paginas
			Identificar duplicatas(na leitura dos dados)
			Inserir a categoria, caso duplicata
			Pegar os dados (extras) da pagina de produto
"""

import pandas as pd
import numpy as np

from webScrape import *
from classes import *

def getMenu():
	print("Crawler do site Lowe's")
	df = None
	op = 0
	while not(op == 5):
		print("Operaçoes: ")
		print("1. Coletar os dados")
		print("2. Ver dataframe dos dados coletados")
		print("3. Remover duplicatas")
		print("4. Sobrescrever dados do csv")
		print("5. Sair do programa")
		op = input("\nQual a opcao desejada? ")
		if op == '1':
			print("Isso pode demorar, tem certeza que deseja continuar?")
			if(input("y/n\n").lower() == 'y'):
				fetchData()
				print("Dados coletados e csv criado")
			else:
				print("Retornando ao menu")
		elif op == '2':
			df = readData()
			print(df)
		elif op == '3':
			if(df.empty):
				print("Dataframe ainda não disponivel")
				print("Leia os dados primeiro")
			else:
				removeDuplicates(df)
				print("Duplicatas removidas")
		elif op == '4':
			if(df.empty):
				print("Dataframe ainda não disponivel")
				print("Leia os dados primeiro")
			else:
				rewriteData(df)
				print("Dados sobreescrevidos no csv")
		elif op == '5':
			print("Programa finalizado")
			return
		else:
			print("Operacao invalida")

def rewriteData(dataframe):
	dataframe.to_csv("geladeiras.csv")

def fetchData():
	catalog = Catalog()
	nameList, urlList = listCategoryUrl('https://www.lowes.com/c/Refrigerators-Appliances')

	for url, name in zip(urlList, nameList):
		getCategoryProducts(url, name, catalog)

	#geladeiras = getPageProducts(urlList, nameList)
	geladeiras = [i.toArray() for i in catalog.getProductList()]

	data = np.array(geladeiras)
	colunas = ['Brand', 'Title', 'Sku', 'Model', 'Url']

	df =pd.DataFrame(data, columns=colunas)
	df.to_csv("geladeiras.csv")
	return df

def readData():
	data = pd.read_csv("geladeiras.csv")
	return data

def removeDuplicates(dataframe):
	dataframe = dataframe.drop_duplicates('Sku', ignore_index=True)
	dataframe = dataframe.drop('Unnamed: 0', axis=1)
	return dataframe

getMenu()