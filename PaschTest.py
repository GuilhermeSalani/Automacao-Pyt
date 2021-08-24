import requests #biblioteca que permite eu fazer requisicao
from bs4 import BeautifulSoup #biblioteca permite eu fazer uma busca dentro do html
import pandas as pd #biblioteca que cria tabela
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.options import Options

options = Options ()
options.add_argument('start-maximized')
#options.add_argument('--headless')
options.add_argument('disable-infobars')
options.add_argument('--incognito')
options.add_argument('--no-sandbox')

lista_celulares = [] #lista que vai receber as informacoes armazenadas dos celulares

Celular = ['Smartphone Samgung Galaxy A70', 'Smartphone Motorola One Vision', 'Smartphone Xiaomi Redmi Note 7'] #Array afim do for indicar o celular
for i in range (3): #0 #1 #2
    
    try:
        navegador = webdriver.Chrome(options=options) #iniciando o driver com as opcoes definidas em options
        navegador.get('https://www.mercadolivre.com.br/') #requisicao ao site
    except:
        print("Navegador fora do AR") #tratativa de erro apresentado no console caso a requisicao esteja com falha
        navegador.close()
        break
    sleep (2)

    try:
        barraDeBusca = navegador.find_element_by_name('as_word') #barra de pesquisa do site
        barraDeBusca.send_keys(Celular[i]) #texto que sera inserido dentro do busca
        lupaDeBusca = navegador.find_element_by_xpath('//button/div') #buscar do site
        lupaDeBusca.click() #clicando em buscar
        sleep (3) #tempo de espera para busca
        site = BeautifulSoup(navegador.page_source, 'html.parser') #variavel para receber o conteudo do site e converter para html e assim fazer buscas nesse conteudo, 
        #essa biblioteca vai basicamente transformar todo conteudo em um objeto, facilitando manipular os dados encontrados
        produtos = site.findAll('div', attrs={'andes-card andes-card--flat andes-card--default ui-search-result ui-search-result--core andes-card--padding-default'}) #div que agrupa os produtos encontrados 
        #todos os produtos da pagina possuem a div em comum. Caso queira somente o primeiro produto, basta mudar para site.find, o conteudo encontrado foi atribuido a uma variavel
        #assim ja que os produtos possuem um conjunto de tags em comum, eu vou consiguir ir filtrando minhas informacoes atraves dos mesmo atributos novamente em comum dentro dessa mesma div
    except:
        print("Não foi encontrado nenhum Celular com essa descrição") #caso a div nao esteja presente, a mesma ira retornar null, apresentado mensagem no console.
    
    for produto in produtos: #para produto dentro de produtos
        celular = produto.find('h2', attrs={'class':'ui-search-item__title'}) #nomes sao encontrados dentro de um h2 com mesmo atributo de classe, dentro da div listada acima
        real = produto.find('span', attrs={'class':'price-tag-fraction'}) #valor e encontrado dentro de um span com mesmo atributo de classe
        centavos = produto.find('span', attrs={'class':'price-tag-cents'}) #nota que os centavos estao dentro de outra classe, sendo assim tenho que repetir para buscar os cents
        link = produto.find('a', attrs={'class':'ui-search-link'}) #mesmo procedimento realizado anteriormente

        if (centavos): #tratativa nao ocorrer null pointer nos cents pois quando o valor e inteiro, o produto nao possui a classe tag cents
            lista_celulares.append([link['href'], celular.text, real.text +','+ centavos.text]) #armazenando os valores dentro da lista
        else:
            lista_celulares.append([link['href'], celular.text, real.text +','+ "00"]) #tratativa para quando o valor for inteiro e a variavel cents retornar null
    navegador.close() #ao final de cada busca, fechar o navegador

ArquivoExcel = pd.DataFrame(lista_celulares, columns=['Nome do Celular','Link','Preco']) #informado a lista ao data frame com as colunas desejadas, a bibli panda vai montar a tabela
ArquivoExcel.to_excel('TestePasch.xlsx', index=False) #montado o arquivo em excel, caso queira indice das colunas setar true

#Durante o teste, foi tentado inicialmente fazer a automatizacao  do processo com o framew junit + cucumber, porem alguma parte do codigo nao estava montando da lista em excel corretamente.

#Com o junit a ideia era armazenar os produtos no carrinho e montar a lista com os produtos encontrados. 
#Inicialmente percebi que os sites possuem uma obrigatoriedade de login para armazenar os produtos em carrinho, e assim sendo,
#a obrigatoriedade de realizar o login, porém pois a maioria dos sites possuem uma validacao de token, identificando que o acesso esta acontecendo por uma automatizacao, 
#Sendo assim ocorria o login nos sites escolhidos.
#Apos conseguir passar desse impecilho, foi tentado de diversas formas montar a lista em excel com os produtos armazenados em carrinho, 
#e por algum motivo nao estava conseguindo montar a lista, com as colunas corretas e as informacoes certas em cada coluna.

print("\nFinalizado Teste Paschoalotto, muito obrigado pela oportunidade")
print("\nGuilherme de Andrade Salani\n\n")
