import requests
from bs4 import BeautifulSoup
import pandas as pd
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

lista_celulares = []

Celular = ['Smartphone Samgung Galaxy A70', 'Smartphone Motorola One Vision', 'Smartphone Xiaomi Redmi Note 7']

for i in range (3):
    
    try:
        navegador = webdriver.Chrome(options=options)
        navegador.get('https://www.mercadolivre.com.br/')
    except:
        print("Navegador fora do AR")
        navegador.close()
        break
    sleep (2)

    try:
        barraDeBusca = navegador.find_element_by_name('as_word')
        barraDeBusca.send_keys(Celular[i])
        lupaDeBusca = navegador.find_element_by_xpath('//button/div')
        lupaDeBusca.click()
        sleep (3)
        site = BeautifulSoup(navegador.page_source, 'html.parser')
        produtos = site.findAll('div', attrs={'andes-card andes-card--flat andes-card--default ui-search-result ui-search-result--core andes-card--padding-default'})
    except:
        print("Não foi encontrado nenhum Celular com essa descrição")
    
    for produto in produtos:
        celular = produto.find('h2', attrs={'class':'ui-search-item__title'})
        real = produto.find('span', attrs={'class':'price-tag-fraction'})
        centavos = produto.find('span', attrs={'class':'price-tag-cents'})
        link = produto.find('a', attrs={'class':'ui-search-link'})

        if (centavos):
            lista_celulares.append([link['href'], celular.text, real.text +','+ centavos.text])
        else:
            lista_celulares.append([link['href'], celular.text, real.text +','+ "00"])
    navegador.close()

ArquivoExcel = pd.DataFrame(lista_celulares, columns=['Nome do Celular','Link','Preco'])
ArquivoExcel.to_excel('TestePasch.xlsx', index=False)
print("\nFinalizado Teste Paschoalotto, muito obrigado pela oportunidade")
print("\nGuilherme de Andrade Salani\n\n")