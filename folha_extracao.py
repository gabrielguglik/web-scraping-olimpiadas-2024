from io import StringIO
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json

# Pegando o conteúdo da URL
url = "https://www1.folha.uol.com.br/esporte/olimpiadas-2024/medalhas/paralimpiada/"
placar_medalhas = {}

rankings = {
    'Medalhas de Ouro': {'field': "@data-scoreboard-olympics-sort-gold=''"},
    'Medalhas de Prata': {'field': "@data-scoreboard-olympics-sort-silver=''"},
    'Medalhas de Bronze': {'field': "@data-scoreboard-olympics-sort-bronze=''"},
    'Total de Medalhas': {'field': "@data-scoreboard-olympics-sort-total=''"},
}

# Função para construir o ranking
def buildRank(type):
    field = rankings[type]['field']

    driver.find_element(By.XPATH, f"//button[{field}]").click()
    element = driver.find_element(By.XPATH, "//div[@class='c-scoreboard__table-limit']//table")
    html_content = element.get_attribute('outerHTML')

    # Estruturando os dados HTML com BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    # Extraindo os dados em um DataFrame com pandas
    raw_data_frame = pd.read_html(StringIO(str(table)))[0]
    fixed_data_frame = raw_data_frame.dropna()
    
    # Renomeando as colunas
    fixed_data_frame.columns = ['Posição', 'País', 'Medalhas de Ouro', 'Medalhas de Prata', 'Medalhas de Bronze', 'Total de Medalhas']
    
    # Transformando os dados em um dicionário próprio
    return fixed_data_frame.to_dict('records')

# Configuração do Selenium
option = Options()
option.headless = True
driver = webdriver.Chrome()

driver.get(url)
# Garantindo que a página será carregada antes de tentar extrair o conteúdo
time.sleep(10)

# Construindo os dados
for type in rankings:
    placar_medalhas[type] = buildRank(type)

# Fechando a página após extrair os dados
driver.quit()

# Salvando os dados no formato JSON
json_data = json.dumps(placar_medalhas, ensure_ascii=False, indent=4)
with open('folha_extracao.json', 'w', encoding='utf-8') as fp:
    fp.write(json_data)

# Criando o DataFrame e adicionando a coluna 'url'
all_data = []
for type in placar_medalhas:
    all_data.extend(placar_medalhas[type])

# Criando o DataFrame
df = pd.DataFrame(all_data)

# Adicionando a coluna 'URL' com o conteúdo da variável url
df['URL'] = url

# Salvando o DataFrame em um arquivo CSV
df.to_csv('folha_extracao.csv', index=False, encoding='utf-8')

print("Dados salvos em folha_extracao.csv com a coluna URL adicionada.")
