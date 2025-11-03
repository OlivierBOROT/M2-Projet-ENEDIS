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
            # First row: 3 KPI cards (DYNAMIQUES)
            ui.row(
                # KPI 1: Nombre de Logements
                ui.column(4, ui.div(ui.h4("Nombre de Logements"), ui.output_ui("kpi1"), class_="card p-3 text-center shadow")),
                # KPI 2: Consommation Moyenne
                ui.column(4, ui.div(ui.h4("Conso Moyenne"), ui.output_ui("kpi2"), class_="card p-3 text-center shadow")),
                # KPI 3: Note DPE Moyenne
                ui.column(4, ui.div(ui.h4("Note DPE Moyenne"), ui.output_ui("kpi3"), class_="card p-3 text-center shadow")),
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
