from pathlib import Path

import pandas as pd
from shared import INPUTS
from shiny import reactive
from shiny.express import input, ui
from shiny_validate import InputValidator, check

app_dir = Path(__file__).parent
ui.include_css(app_dir / "styles.css")

ui.page_opts(title="Estimation du DPE et de la consommation électrique")

with ui.card():
    ui.card_header("Votre logement 1/2")
    INPUTS["type_logement"]
    INPUTS["surface"]
    INPUTS["code_postal"]
    INPUTS["commune"]
    INPUTS["annee_construction"]

with ui.card():
    ui.card_header("Votre logement 2/2")
    INPUTS["nb_nvx_chauffes"]
    INPUTS["hauteur_plafond"]
    INPUTS["isolation_toit"]
    INPUTS["logement_dessus"]
    INPUTS["isolation_plancher"]
    INPUTS["isolation_murs"]
    
    

with ui.card():
    ui.card_header("Vos installations énergétiques")
    INPUTS["type_chauffage"]
    INPUTS["energie_chauffage"]
    INPUTS["climatisation"]
   

ui.div(
    ui.input_action_button("submit", "Submit", class_="btn btn-primary"),
    class_="d-flex justify-content-end",
)

# Unfortunate workaround to get InputValidator to work in Express
input_validator = None


@reactive.effect
def _():
    # Add validation rules for each input that requires validation
    global input_validator
    input_validator = InputValidator()
    input_validator.add_rule("type_logement", check.required())
    input_validator.add_rule("surface", check.required())
    input_validator.add_rule("code_postal", check.required())
    input_validator.add_rule("commune", check.required())
    input_validator.add_rule("annee_construction", check.required())
    input_validator.add_rule("nb_nvx_chauffes", check.required())
    input_validator.add_rule("hauteur_plafond", check.required())
    input_validator.add_rule("isolation_toit", check.required())
    input_validator.add_rule("logement_dessus", check.required())
    input_validator.add_rule("isolation_plancher", check.required())
    input_validator.add_rule("isolation_murs", check.required())
    input_validator.add_rule("type_chauffage", check.required())
    input_validator.add_rule("energie_chauffage", check.required())
    input_validator.add_rule("climatisation", check.required())


@reactive.effect
@reactive.event(input.submit)
def save_to_csv():
    input_validator.enable()
    if not input_validator.is_valid():
        return

    df = pd.DataFrame([{k: input[k]() for k in INPUTS.keys()}])

    responses = app_dir / "responses.csv"
    if not responses.exists():
        df.to_csv(responses, mode="a", header=True)
    else:
        df.to_csv(responses, mode="a", header=False)

    ui.modal_show(ui.modal("Form submitted, thank you!"))
