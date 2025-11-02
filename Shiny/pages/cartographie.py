from shiny import App, ui
from shinywidgets import output_widget, render_widget  

def page():
    return ui.page_sidebar(
        # Sidebar on the right
        ui.sidebar(
            ui.h3(""),
            ui.h3("Inputs"),
            ui.input_radio_buttons(
                id="kpi_choice",
                label="Choix du KPI",
                choices=[
                    "moyenne du DPE",
                    "consommation moyenne",
                    "nombre de logements",
                    "zones à rénover"
                ],
                selected="moyenne du DPE"
            ),
            ui.input_radio_buttons(
                id="geo_level",
                label="Niveau géographique",
                choices=["par département", "par code_postal"],
                selected="par département"
            ),
            position="right",
            bg="#f8f9fa",
            style="padding: 20px; border-left: 2px solid #ddd; min-width: 300px;",
        ),

        # Main content
        ui.div(
            ui.h2("Cartographie"),
            ui.p("Visualisation cartographique des données."),

            # Card for the map
            ui.card(
                ui.h4("Carte"),
                ui.card_body(
                    ui.output_ui("render_map")
                ),
                class_="shadow mb-4; height: 600px;"
            ),

            # Row of download buttons with spacing
            ui.row(
                ui.column(
                    4,
                    ui.div(ui.download_button("download1", "Download 1"),
                           class_="d-grid mb-2")
                ),
                ui.column(
                    4, 
                    ui.div(ui.download_button("download2", "Download 2"),
                           class_="d-grid mb-2")
                ),
                ui.column(4,
                          ui.div(ui.download_button("download3", "Download 3"),
                                 class_="d-grid mb-2")
                ),
                style="margin-top: 30px;"
            ),
            style="padding-right: 20px; padding-left: 20px;"
        )
    )
