import requests
from bs4 import BeautifulSoup
import html

def fetch_jogos():
    url = "https://mantosdofutebol.com.br/guia-de-jogos-tv-hoje-ao-vivo/"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'  # garante codificação correta
    soup = BeautifulSoup(res.text, 'html.parser')

    jogos = []
    for h in soup.find_all(['h2', 'h3']):
        title = h.get_text(strip=True)
        if ' x ' in title or '–' in title:
            canal = "Canal não informado"
            next_p = h.find_next_sibling('p')
            if next_p and ('Canal:' in next_p.text or 'Canais:' in next_p.text):
                canal = next_p.get_text(strip=True)
                canal = canal.replace('Canais:', '').replace('Canal:', '').strip()
            # protege contra caracteres especiais no HTML
            title = html.escape(title)
            canal = html.escape(canal)
            jogos.append((title, canal))
    return jogos

def gerar_html(jogos):
    bloco = ""
    for jogo, canal in jogos:
        bloco += (
            '<div class="game">'
            f'<div class="info">{jogo}</div>'
            f'<div class="canal">Canal: {canal}</div>'
            '</div>\n'
        )
    return bloco

if __name__ == "__main__":
    with open("template.html", "r", encoding="utf-8") as f:
        template = f.read()

    html_final = template.replace("{{JOGOS_AQUI}}", gerar_html(fetch_jogos()))

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_final)
