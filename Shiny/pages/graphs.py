from shiny import App, ui
from shinywidgets import output_widget 

def page():
    return ui.page_sidebar(
        # ==================================
        # SIDEBAR : Inputs de Filtrage
        # ==================================
        ui.sidebar(
            ui.h3("Inputs de filtrage"),
            
            # Inputs génériques
            ui.input_slider("slider1", "Slider Example", min=0, max=100, value=50),
            ui.input_text("text1", "Text Input", value="Type here"),
            ui.input_checkbox("check1", "Check me"),
            
            ui.hr(), # Séparateur
            ui.h4("Filtres DPE"),
            
            # 1. Input pour la période de construction (Mis à jour dynamiquement par le serveur)
            ui.input_select(
                "select_periode_construction", 
                "Période de Construction :",
                # La liste statique sera écrasée par le serveur
                choices=["Toutes", "Avant 1945", "1946-1970", "1971-1988", "Après 1988"],
                selected="Toutes",
            ),
            
            open='closed'
        ),
        
        # ==================================
        # CONTENU PRINCIPAL : KPI et Graphiques
        # ==================================
        ui.card_body(
            # First row: 3 KPI cards
            ui.row(
                ui.column(4, ui.div(ui.h3("KPI 1"), ui.h1("123"), class_="card p-3 text-center shadow")),
                ui.column(4, ui.div(ui.h3("KPI 2"), ui.h1("456"), class_="card p-3 text-center shadow")),
                ui.column(4, ui.div(ui.h3("KPI 3"), ui.h1("789"), class_="card p-3 text-center shadow")),
            ),

            # Second row: Graphique 1 (DPE) et Graphique 2
            ui.row(
                ui.column(
                    6,
                    output_widget("graph1")
                ),
                ui.column(
                    6,
                    ui.output_plot("graph2")
                ),
            ),

            # Third row: Graphique 3 et Graphique 4
            ui.row(
                ui.column(
                    6,
                    ui.output_plot("graph3")
                ),
                ui.column(
                    6,
                    ui.output_plot("graph4")
                ),
            ),
        )
    )