from shiny import ui
from pathlib import Path

here = Path(__file__).parent.parent
content_dir = here / "content"

with open(f"{content_dir}/donnees_ademe.md", encoding="UTF-8") as f:
    donnees_ademe_markdown = f.read()

with open(f"{content_dir}/donnees_datagouv.md", encoding="UTF-8") as f:
    donnees_datagouv_markdown = f.read()

with open(f"{content_dir}/donnees_openstreetmap.md", encoding="UTF-8") as f:
    donnees_openstreetmap_markdown = f.read()

def page():
    return ui.page_fluid(
        # =========================
        # --- Présentation globale
        # =========================
        ui.card(
            ui.h4("Présentation des données"),

            # Barre d'onglets
            ui.navset_tab(
                # Onglet ADEME
                ui.nav_panel(
                    "ADEME",
                    ui.div(
                        "Principale source de données",
                    ),
                    ui.markdown(donnees_ademe_markdown)
                ),

                # Onglet DATA.GOUV
                ui.nav_panel(
                    "DATA.GOUV",
                    ui.div(
                        "Source de données secondaire"
                    ),
                    ui.markdown(donnees_datagouv_markdown)
                ),

                # Onglet OPENSTREETMAP
                ui.nav_panel(
                    "OPENSTREETMAP",
                    ui.div(
                        "Source de données complémentaire"
                    ),
                    ui.markdown(donnees_openstreetmap_markdown)
                ),
            ),
        ),

        # =========================
        # --- Schémas explicatifs
        # =========================
        ui.card(
            ui.card(
                ui.h3("Schémas explicatifs des étapes d'extraction des données"),
                ui.img(src = "schemas/schema_de_l_ordre_de_l_ajout_des_donnees.png",
                       alt="schema_de_l_ordre_de_l_ajout_des_donnees"),
                       style="display: block; margin: auto; max-width: 80%; height: auto; border-radius: 10px;"

            ),
            ui.card(
                ui.h3("Schémas explicatifs des étapes de transformations des données"),
                ui.img(src = "schemas/schema_de_l_ordre_des_transformations_des_donnees.png",
                       alt="schema_de_l_ordre_des_transformations_des_donnees"),
                        style="display: block; margin: auto; max-width: 80%; height: auto; border-radius: 10px;"
            ),
        ),

        # =========================
        # --- Aperçu des données
        # =========================
        ui.card(
            ui.h2("Aperçu des données"),

            # Ligne 1 : slider
            ui.div(
                ui.input_slider("nrows", "Nombre de lignes à afficher", 1, 100, 10),
                style="margin-bottom: 10px;"
            ),

            # DataFrame
            ui.div(ui.output_data_frame("render_data_head")),

            # Boutons de téléchargement
            ui.div(
                ui.div(
                    ui.download_button("save_head_data", "Télécharger les données affichées"),
                    style="width: 50%; display: flex; justify-content: center; padding-right: 5px;"
                ),
                ui.div(
                    ui.download_button("save_all_data", "Télécharger toutes les données"),
                    style="width: 50%; display: flex; justify-content: center; padding-left: 5px;"
                ),
                style="display: flex; gap: 0;"
            ),
        ),
    )
