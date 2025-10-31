from pathlib import Path

import pandas as pd
import seaborn as sns
from shared import INPUTS
from shiny import reactive
from shiny.express import input, ui
from shiny_validate import InputValidator, check

ui.page_opts(title="Estimation du DPE et de la consommation électrique")

ui.nav_spacer()  # Push the navbar items to the right
footer = ui.div(
        ui.input_action_button("submit", "Submit", class_="btn btn-primary"),
    class_="d-flex justify-content-end",
    )


with ui.nav_panel("Vos informations"):
    with ui.navset_card_underline(title="Vos Informations", footer=footer):
        with ui.nav_panel("Votre logement 1/2"):

            INPUTS["type_logement"]
            INPUTS["surface"]
            INPUTS["code_postal"]
            INPUTS["commune"]
            INPUTS["annee_construction"]

        with ui.nav_panel("Votre logement 2/2"):

            INPUTS["nb_nvx_chauffes"]
            INPUTS["hauteur_plafond"]
            INPUTS["isolation_toit"]
            INPUTS["logement_dessus"]
            INPUTS["isolation_plancher"]
            INPUTS["isolation_murs"]
            
        with ui.nav_panel("Vos installations énergétiques"):

            INPUTS["type_chauffage"]
            INPUTS["energie_chauffage"]
            INPUTS["climatisation"]
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
            "Des informations sont absentes, merci de finir de compléter le formulaire"
        else : 
            return

        df = pd.DataFrame([{k: input[k]() for k in INPUTS.keys()}])

        responses = app_dir / "responses.csv"
        if not responses.exists():
            df.to_csv(responses, mode="a", header=True)
        else:
            df.to_csv(responses, mode="a", header=False)

        ui.modal_show(ui.modal("Vos données ont bien prises en compte, Rendez-vous à la page des résultats!"))



with ui.nav_panel("Vos résultats"):
    "This is the second 'page'."

with ui.nav_panel("Cartographie"):
    "This is the  third 'page'."
