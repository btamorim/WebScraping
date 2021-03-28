import urllib.request
#import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
import json
import time as tempo
#(Pegar conteúdo HTML a partir da URL)
url = "https://www.cartolafcbrasil.com.br/scouts/cartola-fc-2020/rodada-1"
times = {'Athlético-PR',
         'Atlético-MG',
         'Atlético-GO',
         'Bahia',
         'Botafogo',
         'Bragantino',
         'Ceará',
         'Corinthians',
         'Coritiba',
         'Flamengo',
         'Fluminense',
         'Fortaleza',
         'Goiás',
         'Grêmio',
         'Internacional',
         'Palmeiras',
         'Santos',
         'São Paulo',
         'Sport',
         'Vasco'
        }

def pontuacaoAtletas(timess, clube):

    driver.find_element_by_xpath(
        f"//select[@name='ctl00$cphMainContent$drpClubes']/option[text()='{timess}']").click()
    
    driver.find_element_by_name('ctl00$cphMainContent$btnFiltrar').click() 
    tempo.sleep(3)
    '''pegando dados da tabela'''
    element = driver.find_element_by_xpath(
            "//div[@id='ctl00_cphMainContent_uppScouts']//table")
    html_content = element.get_attribute('outerHTML')

    # Parse HTML (Parsear o conteúdo HTML) - BeaultifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    #  (Estruturar conteúdo em um Data Frame) - Pandas
    df_full = pd.read_html(str(table))[0]

    # FIltrar por coluna
    df = df_full[[ 'Nome', 'Clube', 'Preço','J', 'Média','Últ. Pont.', 'Variação']]
    df.columns = [ 'nome', 'clube', 'preco','J', 'media','ultima_pont', 'variacao']

    driver.implicitly_wait(10) 
    
    clubes = df.to_dict('records')
    for dado in clubes:
        dado['clube'] = clube

    # (Transformar os Dados em um Dicionário de dados próprio)
    return clubes


option = Options()
option.headless = True

driver = webdriver.Chrome('./chromedriver')

driver.get(url)
driver.implicitly_wait(10)  # in seconds

dados = []
for clube in times:
    print(clube)
    jogadores = pontuacaoAtletas(clube, clube)
    print("****************")
    print(jogadores)
    print("****************")
    dados.append(jogadores)


    
driver.quit()
# Dump and Save to JSON file (Converter e salvar em um arquivo JSON)
with open('ranking.json', 'w', encoding='utf-8') as jp:
    js = json.dumps(dados)
    jp.write(js)
