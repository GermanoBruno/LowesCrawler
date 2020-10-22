# Lowe's Crawler
## Proposta
Script em python para coletar os dados dos refrigeradores do site Lowe's


## Funcionalidades
##### Coletar os dados gerais
Aqui o programa lê o catálogo do site para achar as categorias de produtos, e dentro dessas categorias, lê os dados visíveis dos produtos presentes. Após a leitura, é criado um .csv e é retornado um DataFrame com os dados.

##### Usar os dados do .csv em um DataFrame pandas
Lê o .csv e retorna um DataFrame com seus dados.

##### Remover as duplicatas do DataFrame utilizado
Remove as duplicatas de um DataFrame para evitar acessos multiplos a uma mesma página

##### Sobrescrever o .csv com os dados manipulados do DataFrame
Sobreescreve o .csv presente na pasta com um .csv criado a partir de um DataFrame manipulado no programa.

##### Coletar dados da pagina de produtos
Coleta as especificações de cada produto, encontrados na página de produto.

## Comentários
#### Tecnologias Usadas
* Python 3.8
* BeautifulSoup
* Selenium
* Pandas
* NumPy

#### Dados Coletados por Produto
* URL
* Marca
* Nome
* SKU (id unico no site)
* Modelo
* Categorias
* Tabela de especificações

#### Comentários Adicionais
O programa funciona como esperado, porém ainda há coisas a melhorar. Os dados demoram para ser lidos devido a limitação de precisar abrir o navegador para cada página. A leitura de dados também não tem sucesso em identificar duplicatas e agregar categoria nova em um item já existente. Pra essa funcionalidade eu retirei as duplicatas pelo pandas, mas as categorias não se acumulam.
Na pasta de Arquivos Suporte está o arquivo dos dados coletados por mim.