from shiny import App, ui
from shinywidgets import output_widget 

def page():
    return ui.page_sidebar(
        # ==================================
        # SIDEBAR : Inputs de Filtrage (NETTOYÉ)
        # ==================================
        ui.sidebar(
            ui.h3("Inputs de filtrage"),
            
            # --- FILTRES DPE & Période (G1/G2/G3) ---
            ui.h4("Filtres Période & Énergie (G1, G2, G3)"),
            ui.input_select(
                "select_periode_construction", 
                "Période de Construction :",
                choices=["Toutes", "Avant 1945", "1946-1970", "1971-1988", "Après 1988"],
                selected="Toutes",
            ),
            ui.input_select(
                "select_energie_chauffage", 
                "Énergie de Chauffage :",
                choices=["Toutes"], 
                selected="Toutes",
            ),
            
            ui.hr(), # Séparateur
            
            # --- FILTRES G4 (Courbe Surface) ---
            ui.h4("Filtre G4 (Type de Logement)"),
            ui.input_select(
                "select_type_batiment", 
                "Type de Bâtiment :",
                choices=["Toutes"], # Écrasé par le serveur
                selected="Toutes",
            ),
            
            open='closed'
        ),
        
        # ==================================
        # CONTENU PRINCIPAL : KPI et Graphiques
        # ==================================
        ui.card_body(
            # First row: 3 KPI cards (Vos KPI ici)
            ui.row(
                ui.column(4, ui.div(ui.h3("KPI 1"), ui.h1("123"), class_="card p-3 text-center shadow")),
                ui.column(4, ui.div(ui.h3("KPI 2"), ui.h1("456"), class_="card p-3 text-center shadow")),
                ui.column(4, ui.div(ui.h3("KPI 3"), ui.h1("789"), class_="card p-3 text-center shadow")),
            ),

            # Second row: Graphique 1 et Graphique 2
            ui.row(
                ui.column(6, output_widget("graph1")),
                ui.column(6, output_widget("graph2")),
            ),

            # Third row: Graphique 3 et Graphique 4
            ui.row(
                ui.column(6, output_widget("graph3")), 
                ui.column(6, output_widget("graph4")), 
            ),
        )
    )
