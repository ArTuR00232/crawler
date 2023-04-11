import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime

def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time

# Define a URL base do site que será rastreado
plataform = "PC"
#base_url = "https://www.nuuvem.com/br-pt/catalog/platforms/pc/page/"
with open("Sitemap.xml",'r') as file:
    aqrv = file.read()
# Conecta-se ao banco de dados SQLite
conn = sqlite3.connect('documentos_html.db')
c = conn.cursor()

# Lê o arquivo xml
sitemap = BeautifulSoup (aqrv,'xml')
url = sitemap.find_all('loc')

# Cria a tabela para armazenar os documentos HTML, se ela não existir
c.execute('''CREATE TABLE IF NOT EXISTS documentos_html 
             (id INTEGER PRIMARY KEY, url TEXT, html TEXT, plataform TEXT, timestamp DATETIME)''')
# Função que busca e salva o HTML da página
def salvar_html(url):
    # Faz uma requisição GET para a URL
    response = requests.get(url)

    # Cria um objeto BeautifulSoup com o conteúdo da página
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extrai o HTML da página
    html = str(soup)

    # Salva o HTML no banco de dados
    c.execute("INSERT INTO documentos_html (url, html, plataform, timestamp) VALUES (?, ?, ?, ?)", (url, html, plataform, get_current_time()))
    conn.commit()

    # Retorna o HTML
    return html

# Função que rastreia as páginas do site
def rastrear_paginas(url):
    # Salva o HTML da página atual
    html = salvar_html(url)

    # Cria um objeto BeautifulSoup com o conteúdo da página
    soup = BeautifulSoup(html, 'html.parser')

    # Encontra todos os links na página
    links = soup.find_all("a", "product-card--wrapper")
    # Rastreia os links encontrados
    for link in links:
        # Extrai o URL do link
        link_url = link.get('href')

        if link_url is None:
            continue
        
        print(link_url)
        # Salva o HTML da página linkada
        salvar_html(link_url)

# Inicia o rastreamento na página inicial
x=0
while x < len(url):
    if(len(url[x].text) < 32):
        print(url[x].text)
        rastrear_paginas(url[x].text)
        #ff= 0
        
    elif (url[x].text[32] == 's' and url[x].text[33] == '/' or url[x].text[32] == 'r' and url[x].text[33] == '/' or url[x].text[32] == 'e' and url[x].text[33] == '/' or url[x].text[32] == 'h' and url[x].text[33] == '/' or url[x].text[32] == 'a' and url[x].text[33] == '/' or url[x].text[32] == 'o' and url[x].text[33] == '/' or url[x].text[32] == 'u' and url[x].text[33] == '/' or url[x].text[32] == 'r' and url[x].text[33] == '/'):
       # ff=0
       print(url[x].text[32])
    else:
        print(url[x].text) 
        rastrear_paginas(url[x].text)
       #ff=0
    x+=1      
#


# Fecha a conexão com o banco de dados
conn.close()
