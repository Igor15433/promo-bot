import requests
from bs4 import BeautifulSoup
import pywhatkit as kit
from datetime import datetime
import time
import os

# ===== CONFIG =====
GRUPO = "DCKDRGA61qa6y1sr9D5lpU"
LIMITE_PRECO = 1500
MAX_PROMOS = 10
ARQUIVO_ENVIADOS = "enviados.txt"

# ===== FUNÇÕES =====
def ja_enviados():
    if not os.path.exists(ARQUIVO_ENVIADOS):
        return set()
    with open(ARQUIVO_ENVIADOS, "r") as f:
        return set(l.strip() for l in f.readlines())

def salvar_enviado(link):
    with open(ARQUIVO_ENVIADOS, "a") as f:
        f.write(link + "\n")

def pegar_pelando():
    promos = []
    url = "https://www.pelando.com.br"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    ofertas = soup.select("article")[:20]

    for o in ofertas:
        try:
            titulo = o.select_one("h2").get_text(strip=True)
            link = "https://www.pelando.com.br" + o.select_one("a")["href"]
            preco_texto = o.get_text()

            preco = None
            for p in preco_texto.split():
                if "R$" in p:
                    preco = float(p.replace("R$", "").replace(".", "").replace(",", "."))
                    break

            if preco and preco <= LIMITE_PRECO:
                promos.append((titulo, preco, link))
        except:
            pass

    return promos

def pegar_promos():
    todas = []
    todas.extend(pegar_pelando())
    return todas

def montar_msg(lista):
    msg = "🔥 *PROMOÇÕES TOP DO DIA* 🔥\n\n"
    for i, (titulo, preco, link) in enumerate(lista, 1):
        msg += f"{i}️⃣ {titulo}\n"
        msg += f"💰 R$ {preco:.2f}\n"
        msg += f"🔗 {link}\n\n"
    msg += "🤖 Enviado automaticamente"
    return msg

# ===== EXECUÇÃO =====
print("Buscando promoções...")
promos = pegar_promos()
enviados = ja_enviados()

novas = []
for titulo, preco, link in promos:
    if link not in enviados:
        novas.append((titulo, preco, link))
    if len(novas) >= MAX_PROMOS:
        break

if not novas:
    print("Sem promoções novas.")
    exit()

mensagem = montar_msg(novas)
print("Preparando envio pro WhatsApp...")

agora = datetime.now()
hora = agora.hour
minuto = agora.minute + 2

kit.sendwhatmsg_to_group_instantly(GRUPO, mensagem, wait_time=15, tab_close=True)

for _, _, link in novas:
    salvar_enviado(link)

print("Promoções enviadas com sucesso!")