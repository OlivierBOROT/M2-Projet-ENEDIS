# server/prediction.py
import re
import httpx
import requests
from shiny import reactive, ui, render

FASTAPI_URL = "https://m2-enedis-project-api.onrender.com/"
FASTAPI_PREDICT_URL = FASTAPI_URL + "predict/"
FASTAPI_MODEL_LIST_URL = FASTAPI_URL + "model_list/"
FASTAPI_DOWNLOAD_MODEL_URL = FASTAPI_URL + "download_model/"

try:
    resp = requests.get(FASTAPI_MODEL_LIST_URL, timeout=10.0)
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") == "success":
        MODEL_LIST = data.get("models", [])
        print(MODEL_LIST)
    else:
        MODEL_LIST = []
except Exception as e:
    MODEL_LIST = []


def setup_prediction(input, output, session, dataset):

    # ==============
    # --- INPUTS ---
    # ==============

    def get_choices(col):
        data = dataset().copy()
        return data.loc[:, col].dropna().unique().tolist()

    @output
    @render.ui
    def selected_model():
        return ui.input_select(
            "model_name",
            "Choisir un modèle :",
            choices=MODEL_LIST,
            selected=MODEL_LIST[0],
        )

    @reactive.effect
    @reactive.event(input.dl_model)
    async def _download_model():
        model_name = input.model_name()
        if not model_name:
            return

        download_url = f"{FASTAPI_DOWNLOAD_MODEL_URL}{model_name}"

        modal = ui.modal(
            "Download Model",
            ui.div(
                ui.p("Generating download link..."),
                ui.HTML(f'<a href="{download_url}" target="_blank">Click here</a>')
            ),
            easy_close=True,
            footer=None,
            size="m"
        )
        ui.modal_show(modal)

        
    @output
    @render.ui
    def type_batiment_ui():
        return ui.input_select("type_batiment", "Type de logement :", get_choices('type_batiment'))

    @output
    @render.ui
    def surface_habitable_logement_ui():
        return ui.input_numeric("surface_habitable_logement", "Surface habitable (m²) :",
                                value = 20,
                                min = 1,
                                max = 9999
                                )

    @output
    @render.ui
    def periode_construction_ui():
        choices = get_choices('periode_construction')
        choices = sorted(choices, key=lambda p: int(re.search(r"\d{4}", p).group()))
        return ui.input_select("periode_construction", "Période de construction :", choices= choices)

    @output
    @render.ui
    def nombre_niveau_logement_ui():
        return ui.input_numeric("nombre_niveau_logement", "Nombre de niveaux chauffés :",
                                value = 1,
                                min = 1,
                                max = 9999)

    @output
    @render.ui
    def hauteur_sous_plafond_ui():
        return ui.input_numeric("hauteur_sous_plafond", "Hauteur sous plafond (m) :", 
                                value = 2,
                                min = 1,
                                max = 9999)

    @output
    @render.ui
    def isolation_toiture_ui():
        choices = ["Oui" if x == 1 else "Non" if x == 0 else x for x in get_choices('isolation_toiture')]        
        return ui.input_select("isolation_toiture", "Toiture isolée :", choices = choices)

    @output
    @render.ui
    def qualite_isolation_plancher_bas_ui():
        order = ["insuffisante", "moyenne", "bonne", "très bonne"]
        choices = sorted(get_choices('qualite_isolation_plancher_bas'), key=lambda x: order.index(x))
        return ui.input_select("qualite_isolation_plancher_bas", "Isolation du plancher :", choices = choices)

    @output
    @render.ui
    def qualite_isolation_murs_ui():
        order = ["insuffisante", "moyenne", "bonne", "très bonne"]
        choices = sorted(get_choices('qualite_isolation_murs'), key=lambda x: order.index(x))
        return ui.input_select("qualite_isolation_murs", "Isolation des murs :", choices = choices)

    @output
    @render.ui
    def type_installation_chauffage_ui():
        return ui.input_select("type_installation_chauffage", "Type de chauffage :", get_choices('type_installation_chauffage'))

    @output
    @render.ui
    def type_energie_principale_chauffage_ui():
        return ui.input_select("type_energie_principale_chauffage", "Énergie principale de chauffage :", get_choices('type_energie_principale_chauffage'))

    @output
    @render.ui
    def type_installation_ecs_ui():
        return ui.input_select("type_installation_ecs", "Production d'eau chaude :", get_choices('type_installation_ecs'))

    @output
    @render.ui
    def type_generateur_n1_ecs_n1_ui():
        return ui.input_select("type_generateur_n1_ecs_n1", "Générateur ECS principal :", get_choices('type_generateur_n1_ecs_n1'))

    @output
    @render.ui
    def type_generateur_chauffage_principal_ui():
        return ui.input_select("type_generateur_chauffage_principal", "Générateur chauffage principal :", get_choices('type_generateur_chauffage_principal'))

    # --- Conditional input ---
    @output
    @render.ui
    @reactive.event(input.prediction_type)
    def code_postal_ban_ui():
        if input.prediction_type() == "CONSO":
            return ui.input_text("code_postal_ban", "Code postal :", placeholder="ex: 69000")
        else:
            return None

    # ==================
    # --- FIN INPUTS ---
    # ==================

    def show_results_modal(result_json):
        # Map DPE numeric to letters
        DPE_MAPPING = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G"}

        # Determine status color
        status_color = "green" if result_json.get("status") == "success" else "red"

        if result_json.get("status") != "success":
            return ui.modal(
                "Prediction Error",
                ui.p(str(result_json.get("message", "Unknown error")), style=f"color: {status_color}; font-weight: bold;"),
                easy_close=True,
                footer=None
            )

        # Pretty display for successful prediction
        prediction_type = result_json.get("prediction_type")
        prediction_val = result_json.get("prediction")

        # Adapt value for DPE
        if prediction_type == "DPE":
            prediction_val = DPE_MAPPING.get(int(prediction_val), prediction_val)
        else:
            # Format numeric prediction for CONSO
            try:
                prediction_val = f"{float(prediction_val):,.2f}"
            except Exception:
                pass

        # Build list items dynamically, skipping None values
        info_items = [
            ("Prediction Type", prediction_type),
            ("Model Used", result_json.get("model_used")),
            ("Predicted Value", prediction_val)
        ]
        info_list = [ui.tags.li(f"{name}: {val}") for name, val in info_items if val is not None]

        return ui.modal(
            "Prediction Results",
            ui.div(
                ui.h4("Prediction Summary", style="margin-bottom: 10px;"),
                ui.tags.ul(*info_list, style="font-size: 16px; line-height: 1.5;")
            ),
            easy_close=True,
            footer=None,
            size="m"
        )

    @reactive.effect
    @reactive.event(input.submit)
    async def _():
        """Handle form submission asynchronously."""
        isolation_toiture_value = input.isolation_toiture()
        if isinstance(isolation_toiture_value, str):
            isolation_toiture_value = 1 if isolation_toiture_value.lower() == "oui" else 0
        payload = {
            # Votre logement (1/2)
            "type_batiment": input.type_batiment(),
            "surface_habitable_logement": input.surface_habitable_logement(),
            "nombre_niveau_logement": input.nombre_niveau_logement(),
            "periode_construction": input.periode_construction(),
            "code_postal_ban": input.code_postal_ban() if input.prediction_type() == "CONSO" else 0,

            # Votre logement (2/2)
            "hauteur_sous_plafond": input.hauteur_sous_plafond(),
            "isolation_toiture": isolation_toiture_value,
            "qualite_isolation_plancher_bas": input.qualite_isolation_plancher_bas(),
            "qualite_isolation_murs": input.qualite_isolation_murs(),

            # Vos installations énergétiques
            "type_installation_chauffage": input.type_installation_chauffage(),
            "type_energie_principale_chauffage": input.type_energie_principale_chauffage(),
            "type_installation_ecs": input.type_installation_ecs(),
            "type_generateur_n1_ecs_n1": input.type_generateur_n1_ecs_n1(),
            "type_generateur_chauffage_principal": input.type_generateur_chauffage_principal(),

            "model_name": input.model_name()
        }


        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    FASTAPI_PREDICT_URL,
                    json=payload,
                    params={
                    "prediction_type": input.prediction_type(),
                    "model_name": input.model_name(),
                    }
                    )
                response.raise_for_status()
                result_json = response.json()
        except Exception as e:
            result_json = {"status": "error", "message": str(e)}

        modal = show_results_modal(result_json)
        ui.modal_show(modal)
