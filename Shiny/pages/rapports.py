from shiny import ui

def page():
    return ui.page_fluid(
        ui.h2("Sélection du rapport"),
        ui.card(
            ui.card_header(
                ui.div(
                    ui.input_radio_buttons(
                        "rapport_select",
                        "Choisir un rapport",
                        choices={
                            "general": "Readme",
                            "technique": "Rapport technique",
                            "utilisateur": "Rapport utilisateur",
                            "machine_learning":"Rapport machine learning",
                        },
                        inline=True,
                    )
                )
            ),
            ui.output_ui("shiny_readme"),
            height="800px",
            class_="mt-3",
            full_screen=True,
        )
    )
