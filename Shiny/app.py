from shiny import App, ui
from pathlib import Path
from pages import (
    accueil_page, donnees_page, rapports_page,
    graphs_page, cartographie_page, prediction_page
)
from server_file import server

TITLE = "GreenTech Solutions - Projet Machine learning DPE - 2025"
HEADER_COLOR = "#165e7f"
TEXT_COLOR = "#CDCDCD"
TEXT_COLOR_HOVER = "#FFFFFF"

page_dependencies = ui.tags.head(
    ui.tags.link(rel='stylesheet', type='text/css', href='styles.css'),
    ui.tags.style(f"""
        .navbar-nav .nav-link,
        .navbar-brand,
        .dropdown-toggle {{
            color: {TEXT_COLOR} !important;
        }}
        .navbar-nav .nav-link:hover,
        .dropdown-menu a:hover {{
            font-weight: bold;
            color: {TEXT_COLOR_HOVER} !important;
        }}
        .dropdown-menu {{
            background-color: {HEADER_COLOR};
        }}
    """)
)

# ---- Titre au-dessus de la navbar
header_title = ui.div(
    ui.img(src="logo_appli.png", height="60px", style="margin-right:10px;"),
    ui.h2(
        TITLE,
          style=f"margin-top:10px; color:{TEXT_COLOR}; text-align:center;"
          ),
    style= f"display:flex; padding:15px; background-color:{HEADER_COLOR}; width:100%;",
)

# ---- Barre de navigation (sans titre intégré)
navbar = ui.page_navbar(
    ui.nav_panel("Accueil", accueil_page()),

    ui.nav_menu(
        "Contexte",
        ui.nav_panel("Données", donnees_page()),
        ui.nav_panel("Rapports", rapports_page())
    ),

    ui.nav_menu(
        "Visualisation",
        ui.nav_panel("Graphs", graphs_page()),
        ui.nav_panel("Cartographie", cartographie_page())
    ),

    ui.nav_panel("Prédiction", prediction_page()),
    id="page",
    bg=HEADER_COLOR,
    inverse=True,
    header=page_dependencies
)

footer = ui.div(
    ui.tags.div(
        # Copyright
        ui.tags.p("© 2025 PythonGroup Inc. All rights reserved.", style="margin: 5px;"),
        # GitHub link
        ui.tags.a("GitHub", href="https://github.com/OlivierBOROT/M2-Projet-ENEDIS", target="_blank", style="margin: 0 10px; color:#CDCDCD; text-decoration:none;"),
        # Google Drive link
        ui.tags.a("Données (GDrive)", href="https://drive.google.com/drive/folders/1p7akyWE66UCUMJyBxl0-if-7-RwIKDJE", target="_blank", style="margin: 0 10px; color:#CDCDCD; text-decoration:none;"),
        # YouTube link
        ui.tags.a("Youtube", href="https://www.youtube.com/watch?v=IxX_QHay02M", target="_blank", style="margin: 0 10px; color:#CDCDCD; text-decoration:none;"),
        ),
        # LinkedIn links
        ui.tags.div(
            ui.tags.a(
                "Olivier BOROT",
                href="https://www.linkedin.com/in/olivier-borot/",
                target="_blank",
                style="margin: 0 5px; color:#CDCDCD; text-decoration:none;"
            ),
            ui.tags.a(
                "Aya Mecheri",
                href="https://www.linkedin.com/in/aya-mecheri/",
                target="_blank",
                style="margin: 0 5px; color:#CDCDCD; text-decoration:none;"
            ),
            ui.tags.a(
                "Anne-Camille Vial",
                href="https://www.linkedin.com/in/anne-camille-vial-14629b66/",
                target="_blank",
                style="margin: 0 5px; color:#CDCDCD; text-decoration:none;"
            ),
            ui.tags.a(
                "Constantin Rey-Coquais",
                href="https://www.linkedin.com/in/constantin-rey-coquais-49a8a7250/",
                target="_blank",
                style="margin: 0 5px; color:#CDCDCD; text-decoration:none;"
            ),
            style="margin-top:5px;"
        ),
        style="display:flex; flex-direction:column; align-items:center;"
)

# ---- Combinaison du titre + navbar
app_ui = ui.page_fluid(
    header_title,
    navbar,
    footer
)

# ---- Création de l'application
www_dir = Path(__file__).parent / "www"
app = App(app_ui, server, static_assets=www_dir)
