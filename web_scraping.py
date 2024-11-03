from io import StringIO
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json

# pegando o conteúdo da url

url = "https://www1.folha.uol.com.br/esporte/olimpiadas-2024/medalhas/paralimpiada/"
placar_medalhas = {}

rankings = {
    'Medalhas de Ouro': {'field': "@data-scoreboard-olympics-sort-gold=''"},
    'Medalhas de Prata': {'field': "@data-scoreboard-olympics-sort-silver=''"},
    'Medalhas de Bronze': {'field': "@data-scoreboard-olympics-sort-bronze=''"},
    'Total de Medalhas': {'field': "@data-scoreboard-olympics-sort-total=''"},
}

def buildRank(type):

    field = rankings[type]['field']

    driver.find_element(By.XPATH, f"//button[{field}]").click()
    element = driver.find_element(By.XPATH, "//div[@class='c-scoreboard__table-limit']//table")
    html_content = element.get_attribute('outerHTML')

    # estruturando os dados html com beautifulsoup
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    # extraindo os dados em um data frame com pandas
    raw_data_frame = pd.read_html(StringIO(str(table)))[0]
    fixed_data_frame = raw_data_frame.dropna()
    # renomeando as colunas
    fixed_data_frame.columns = ['Posição', 'País', 'Medalhas de Ouro', 'Medalhas de Prata', 'Medalhas de Bronze', 'Total de Medalhas']

    # transformando os dados em um dicionário próprio
    return fixed_data_frame.to_dict('records')

option = Options()
option.headless = True
driver = webdriver.Chrome()

driver.get(url)
# garantindo que a página será carregada antes de tentar extrair o conteúdo
time.sleep(10)

for type in rankings:
    placar_medalhas[type] = buildRank(type)

# fechando a página após extrair os dados
driver.quit()

# salvando o dicionário próprio em um json
json = json.dumps(placar_medalhas,  ensure_ascii=False)
fp = open('placar_total.json', 'w')
with open('placar_total.json', 'w', encoding='utf-8') as fp:
    fp.write(json)
fp.close()