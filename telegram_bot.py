import requests
from bs4 import BeautifulSoup
import time

TOKEN = "COLE_SEU_TOKEN_AQUI"
CHAT_ID = "COLE_SEU_CHAT_ID_AQUI"

def enviar(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

def pegar_promos():
    url = "https://www.pelando.com.br"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    ofertas = soup.select("article")[:10]

    promos = []
    for o in ofertas:
        try:
            titulo = o.select_one("h2").get_text(strip=True)
            link = "https://www.pelando.com.br" + o.select_one("a")["href"]
            promos.append((titulo, link))
        except:
            pass
    return promos

def montar_msg(lista):
    msg = "🔥 PROMOÇÕES DO DIA 🔥\n\n"
    for i, (titulo, link) in enumerate(lista, 1):
        msg += f"{i}. {titulo}\n{link}\n\n"
    msg += "🤖 Automático"
    return msg

print("Buscando promoções...")
promos = pegar_promos()
mensagem = montar_msg(promos)
enviar(mensagem)
print("Enviado no Telegram!")
