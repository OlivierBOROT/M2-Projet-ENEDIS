import requests
from shiny import reactive, render, ui
import markdown

rapports = {
    "technique": "https://raw.githubusercontent.com/posit-dev/py-shiny/refs/heads/main/README.md",
    "utilisateur": "",
    "general": "https://raw.githubusercontent.com/OlivierBOROT/M2-Projet-ENEDIS/refs/heads/extraction_donnees/Rapport%20Machine%20Learning.md"
}

cache = {}

def setup_rapports(input, output, session):

    @output
    @render.ui
    @reactive.event(input.rapport_select)
    def shiny_readme():
        choice = input.rapport_select()
        if choice not in rapports:
            return ui.HTML("<p>Choix invalide.</p>")

        if choice in cache:
            html = cache[choice]
            return ui.HTML(html)

        link = rapports[choice]
        if not link:
            html = "<p>Aucun rapport disponible.</p>"
            cache[choice] = html
            return ui.HTML(html)

        try:
            response = requests.get(link)
            response.raise_for_status()
            md_text = response.text
            html = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite'])
            cache[choice] = html
            return ui.HTML(html)
        except requests.RequestException as e:
            html = f"<p>Erreur lors du téléchargement : {e}</p>"
            cache[choice] = html
            return ui.HTML(html)
