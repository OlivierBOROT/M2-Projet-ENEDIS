from shiny import App, ui

def page():
    return  ui.page_sidebar(
        # Sidebar on the left
        ui.sidebar(
            ui.h3("Inputs"),
            ui.input_slider("slider1", "Slider Example", min=0, max=100, value=50),
            ui.input_text("text1", "Text Input", value="Type here"),
            ui.input_checkbox("check1", "Check me"),
            open='closed'
        ),
        # Main content on the right
        ui.card_body(
            # First row: 3 KPI cards
            ui.row(
                ui.column(
                    4,
                    ui.div(ui.h3("KPI 1"),
                    ui.h1("123"),
                    class_="card p-3 text-center shadow")
                ),
                ui.column(
                    4,
                    ui.div(ui.h3("KPI 2"),
                    ui.h1("456"),
                    class_="card p-3 text-center shadow")
                ),
                ui.column(
                    4,
                    ui.div(ui.h3("KPI 3"),
                    ui.h1("789"),
                    class_="card p-3 text-center shadow")
                ),
            ),

            # Second row: 2 graphs
            ui.row(
                ui.column(
                    6,
                    ui.output_plot("graph1")
                ),
                ui.column(
                    6,
                    ui.output_plot("graph2")
                ),
            ),

            # Third row: 2 graphs
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