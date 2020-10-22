#coding: utf-8

import pandas as pd
import numpy as np

from webScrape import *

def getMenu():
	print("Crawler do site Lowe's")
	df = None
	op = 0
	while (op != 6):
		print("Operaçoes: ")
		print("1. Coletar os dados gerais")
		print("2. Ver dataframe dos dados coletados")
		print("3. Remover duplicatas")
		print("4. Sobrescrever dados do csv")
		print("5. Coletar dados especificos dos produtos")
		print("6. Sair do programa")
		op = input("\nQual a opcao desejada? ")
		if op == '1':
			if(input("Isso pode demorar, tem certeza que deseja continuar? (y/n)\n").lower() == 'y'):
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
			if(df.empty):
				print("Dataframe ainda não disponivel")
				print("Leia os dados primeiro")
			else:
				df = fetchProductData(df)
		elif op == '6':
			print("Programa finalizado")
			#return
		else:
			print("Operacao invalida")

def rewriteData(dataframe):

	dataframe.to_csv("geladeiras.csv")

def fetchData():
	catalog = Catalog()
	nameList, urlList = listCategoryUrl('https://www.lowes.com/c/Refrigerators-Appliances')

	for url, name in zip(urlList, nameList):
		getCategoryProducts(url, name, catalog)

	geladeiras = [i.toArray() for i in productList]

	data = np.array(geladeiras)
	colunas = ['Brand', 'Title', 'Sku', 'Model', 'Url', 'Categories']

	df =pd.DataFrame(data, columns=colunas)
	df.to_csv("geladeiras.csv")
	return df

def readData():
	data = pd.read_csv("geladeirasTotal.csv")
	return data


def fetchProductData(dataframe):
	specsColumn = []
	i = 0
	print('tamanho total:', len(dataframe))
	for productUrl in dataframe['Url']:
		i= i+1
		print('item atual', i)
		spec = getProductData(productUrl)
		specsColumn.append(spec)
	if(len(dataframe) == len(specsColumn)):
		dataframe['Specifications'] = specsColumn
	else:
		print('Specs não identificados')
	return dataframe



def removeDuplicates(dataframe):
	dataframe = dataframe.drop_duplicates('Sku', ignore_index=True)
	dataframe = dataframe.drop('Unnamed: 0', axis=1)
	return dataframe

getMenu()

# Caminho esperado
#fetchData()
#df = readData()
#df =removeDuplicates(df)
#df = fetchProductData(df)
#rewriteData(df)
#df = readData()