canal_links = {
    "Premiere": "https://globoplay.globo.com/premiere/",
    "ESPN": "https://www.espn.com.br/watch/",
    "Amazon Prime": "https://www.primevideo.com/",
    "SporTV": "https://globoplay.globo.com/sportv/",
}

for jogo in jogos:
    canal = jogo['canal']
    canal_link = canal_links.get(canal, "#")

    jogos_html += f"""
    <div class="card p-3" data-league="{jogo['campeonato']}" data-canal="{canal}">
      <div class="card-title">{jogo['hora']} - {jogo['time1']} x {jogo['time2']}</div>
      <div>Campeonato: {jogo['campeonato']}</div>
      <div class="canal">Canal: <a href="{canal_link}" target="_blank">{canal}</a></div>
    </div>
    """
