# para esse script é necessário anteriormente criar um banco de dados MySQL com as colunas “id”, “valor” e “data” em formato string.
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
from datetime import date
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="senha_do_banco")
cur = conn.cursor()
cur.execute("USE nome_do_banco")
string = "AALR3 ABCB4 ABEV3 ADHM3 " # Inserir códigos dos ativos separados por espaço entre aspas
lista = string.split(" ")

def store(title, content, data):
    cur.execute('INSERT INTO betas (id, valor, data) VALUES '
        '("%s", "%s", "%s")', (title, content, data))
    conn.commit()

def EncontraInformacoes(codigo):
    try:
        html=urlopen(f"https://br.financas.yahoo.com/quote/{codigo}.SA?p={codigo}.SA&.tsrc=fin-srch")
        bs = BeautifulSoup(html, "html.parser")
        title = codigo
        data = date.today()
        content = bs.find("td", {"data-test": "BETA_5Y-value"}).find("span").get_text()
        store(title, content, data)
        print(codigo, content, data)
    except:
        pass
try:
    for codigo in lista:
        EncontraInformacoes(codigo)
finally:
    cur.close()
    conn.close()
