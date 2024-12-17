import requests
from bs4 import BeautifulSoup
import csv

# URL e headers
url = 'https://ge.globo.com/olimpiadas/noticia/2024/08/01/quantas-medalhas-o-brasil-tem-nas-olimpiadas-2024-veja-lista.ghtml'
headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}

# Fazendo a requisição
site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')

# Encontrando as listas de medalhistas
medalhistas = soup.find_all('ul', class_='content-unordered-list')

# Lista para armazenar os dados extraídos
dados = []

print(medalhistas)

# Função para corrigir nomes de esportes ou equipes
def corrigir_esporte(esporte):
    esporte = esporte.strip().lower()
    if 'seleção feminina de futebol' in esporte:
        return 'futebol'
    elif 'seleção feminina de vôlei' in esporte:
        return 'vôlei'
    elif 'equipe feminina de ginástica artística' in esporte:
        return 'ginástica artística'
    else:
        return esporte

# Função para corrigir a categoria da medalha
def corrigir_categoria(categoria):
    categoria = categoria.strip().lower()
    if 'ouro' in categoria:
        return 'Ouro'
    elif 'prata' in categoria:
        return 'Prata'
    elif 'bronze' in categoria:
        return 'Bronze'
    else:
        return categoria

# Processando cada item da lista
for medalha in medalhistas:
    for item in medalha.find_all('li'):
        # Extraindo a categoria da medalha (tag <strong>)
        categoria = item.find('strong').text.strip()

        # Corrigir categoria
        categoria_corrigida = corrigir_categoria(categoria)

        # Extraindo os atletas e os esportes
        atletas_e_esportes = item.text.replace(categoria, "").strip()

        # Separando os atletas e os esportes pela vírgula ou "e"
        atletas_esportes_list = [x.strip() for x in atletas_e_esportes.replace(' e ', ',').split(',')]

        for atleta_esporte in atletas_esportes_list:
            # Remover o "-" do nome do atleta e separar nome do esporte (se houver)
            atleta_esporte = atleta_esporte.lstrip('-').strip()
            
            if '(' in atleta_esporte:  # Existe um esporte associado ao atleta
                nome_atleta = atleta_esporte.split('(')[0].strip()
                esporte = atleta_esporte.split('(')[1].replace(')', '').strip()
            else:  # Se não houver parênteses, o atleta e o esporte são combinados
                nome_atleta = atleta_esporte.strip()
                esporte = "Desconhecido"  # Caso não tenha esporte explícito
                
            # Corrigir o nome do esporte
            esporte_corrigido = corrigir_esporte(esporte)
            
            # Adicionando uma linha para cada medalha (caso haja multiplicidade)
            if '(' in atleta_esporte and esporte.isdigit():
                qtd = int(esporte)
                for _ in range(qtd):
                    dados.append([nome_atleta, f"1 {categoria_corrigida}", esporte_corrigido])
            else:
                dados.append([nome_atleta, f"1 {categoria_corrigida}", esporte_corrigido])

# Salvando os dados em um arquivo CSV
with open('extracao_Globo_Esporte.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Nome Atleta', 'Categoria da Medalha', 'Esporte'])  # Cabeçalho
    writer.writerows(dados)

print("CSV gerado com sucesso!")
