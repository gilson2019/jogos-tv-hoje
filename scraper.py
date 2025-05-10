import requests
from bs4 import BeautifulSoup
import html

API_KEY = "live_9526028cb44c00533bc77bb654b2a6"

# Busca lista de todos os times e salva nome/brasão
def fetch_times():
    res = requests.get(
        "https://api.api-futebol.com.br/v1/times",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    times = res.json()
    # Cria um dicionário: nome -> escudo
    return {t["nome_popular"].lower(): t["escudo"] for t in times}

def fetch_jogos():
    url = "https://mantosdofutebol.com.br/guia-de-jogos-tv-hoje-ao-vivo/"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')

    escudos = fetch_times()

    jogos = []
    for h in soup.find_all(['h2', 'h3']):
        title = h.get_text(strip=True)
        if ' x ' in title or '–' in title:
            canal = "Canal não informado"
            next_p = h.find_next_sibling('p')
            if next_p and ('Canal:' in next_p.text or 'Canais:' in next_p.text):
                canal = next_p.get_text(strip=True)
                canal = canal.replace('Canais:', '').replace('Canal:', '').strip()

            # Extrair nomes dos times tentando dividir pelo separador
            separador = ' x ' if ' x ' in title else '–'
            time1, time2 = [t.strip().lower() for t in title.split(separador, 1)]

            # Obter brasões se existirem
            brasao1 = escudos.get(time1, '')
            brasao2 = escudos.get(time2, '')

            jogos.append((html.escape(title), html.escape(canal), brasao1, brasao2, time1.title(), time2.title()))
    return jogos

def gerar_html(jogos):
    bloco = ""
    for titulo, canal, escudo1, escudo2, time1, time2 in jogos:
        bloco += '<div class="game">'
        if escudo1:
            bloco += f'<img class="brasao" src="{escudo1}" alt="{time1}"> '
        bloco += f'{time1} <strong>vs</strong> '
        if escudo2:
            bloco += f'<img class="brasao" src="{escudo2}" alt="{time2}"> '
        bloco += f'{time2}'
        bloco += f'<div class="canal">Canal: {canal}</div>'
        bloco += '</div>\n'
    return bloco

if __name__ == "__main__":
    with open("template.html", "r", encoding="utf-8") as f:
        template = f.read()

    html_final = template.replace("{{JOGOS_AQUI}}", gerar_html(fetch_jogos()))

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_final)
