import requests
from bs4 import BeautifulSoup
import csv
import re

# URL e headers
url = 'https://ge.globo.com/olimpiadas/noticia/2024/08/01/quantas-medalhas-o-brasil-tem-nas-olimpiadas-2024-veja-lista.ghtml'
headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}

# Fazendo a requisição
site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')

# Encontrando as listas de medalhistas
medalhistas = soup.find_all('ul', class_='content-unordered-list')

# Função para limpar e tratar os dados
def extrair_medalhas(medalhistas):
    dados = []
    for lista in medalhistas:
        for item in lista.find_all('li'):
            # Extraindo medalha e corrigindo formato
            medalha_raw = item.find('strong').text.strip()
            medalha = re.sub(r'Ouros', 'Ouro', re.sub(r'Pratas', 'Prata', re.sub(r'Bronzes', 'Bronze', medalha_raw.split()[1])))
            
            # Extraindo a string após o hífen
            conteudo = item.text.split('-')[1].strip()
            
            # Separando os atletas e esportes
            atletas = re.split(r',| e ', conteudo)  # Divide por vírgula ou " e "
            for atleta in atletas:
                # Expressão regular ajustada para número isolado
                match = re.search(r'(.+?) \((\b\d+\b)? ?(.+?)?\)', atleta)  # Captura nome, número isolado e esporte
                if match:
                    nome = match.group(1).strip()
                    quantidade = int(match.group(2)) if match.group(2) else 1
                    esporte = match.group(3).strip() if match.group(3) else 'Indefinido'
                    
                    # Adiciona múltiplas linhas conforme quantidade de medalhas
                    for _ in range(quantidade):
                        dados.append([nome, medalha, esporte, url])
                else:
                    # Tratamento para casos sem parênteses
                    if 'seleção feminina de futebol' in atleta:
                        dados.append(['Seleção Feminina de Futebol', medalha, 'Futebol', url])
                    elif 'seleção feminina de vôlei' in atleta:
                        dados.append(['Seleção Feminina de Vôlei', medalha, 'Vôlei', url])
                    elif 'equipe feminina de ginástica artística' in atleta:
                        dados.append(['Equipe Feminina de Ginástica Artística', medalha, 'Ginástica Artística', url])
                    elif 'equipe de judô' in atleta:
                        dados.append(['Equipe de Judô', medalha, 'Judô', url])
                    else:
                        dados.append([atleta.strip(), medalha, 'Indefinido', url])
    return dados

# Extraindo dados
dados_tratados = extrair_medalhas(medalhistas)

# Salvando no arquivo CSV com a coluna 'url'
with open('extracao_globo_esporte.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Nome do Atleta', 'Medalha', 'Esporte', 'URL'])
    writer.writerows(dados_tratados)

print("Dados salvos no arquivo 'extracao_globo_esporte.csv'.")
