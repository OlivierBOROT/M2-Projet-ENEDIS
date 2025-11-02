from shiny import ui

def page():
    return ui.page_fluid(
        ui.tags.style(
            """
            .card h1, .card h2, .card h3, .card h4, .card h5, .card h6 {
                text-align: center;
            }
            """
        ),
            ui.div(
            ui.h2("Bienvenue sur la page d'accueil"),
        ),
        ui.card(
            ui.output_markdown_stream(
                "accueil_readme",
                auto_scroll=False
                ),
            style="""
                height: auto;
                overflow: auto;
            """,
            class_="mt-3",
            full_screen=True,
        )
    )
