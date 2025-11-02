from shiny import App, ui
from shinywidgets import output_widget, render_widget  

def page():
    return ui.page_sidebar(
        # Sidebar on the right
        ui.sidebar(
            ui.h3("Inputs"),
            position="right",
            bg="#f8f9fa",
            style="padding: 20px; border-left: 2px solid #ddd; min-width: 300px;",
            open='closed'
        ),

        # Main content
        ui.div(
            ui.h2("Cartographie"),
            ui.p("Visualisation cartographique des données."),

            # Card for the map
            ui.card(
                ui.h4("Carte"),
                ui.card_body(
                    output_widget("map")
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
