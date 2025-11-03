# server/prediction.py
import re
import httpx
from shiny import reactive, ui, render

FASTAPI_URL = "http://127.0.0.1:8000/predict/"  # your FastAPI endpoint

def setup_prediction(input, output, session, dataset):

    # ==============
    # --- INPUTS ---
    # ==============

    def get_choices(col):
        data = dataset().copy()
        return data.loc[:, col].dropna().unique().tolist()

    # --- Inputs dynamically rendered ---
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

    def show_results_modal(results_text: str):
        """Return a modal UI showing the results text."""
        return ui.modal(
            ui.h3("✅ Résultats du questionnaire"),
            ui.pre(results_text, class_="bg-light p-3 rounded border"),
            easy_close=True,
            footer=ui.modal_button("Fermer"),
            size="l"
        )

    @reactive.effect
    @reactive.event(input.submit)
    async def _():
        """Handle form submission asynchronously."""
        payload = {
            # Votre logement (1/2)
            "type_batiment": input.type_batiment(),
            "surface_habitable_logement": input.surface_habitable_logement(),
            "nombre_niveau_logement": input.nombre_niveau_logement(),
            "periode_construction": input.periode_construction(),
            "code_postal_ban": input.code_postal_ban() if input.prediction_type() == "CONSO" else None,

            # Votre logement (2/2)
            "hauteur_sous_plafond": input.hauteur_sous_plafond(),
            "isolation_toiture": input.isolation_toiture(),
            "qualite_isolation_plancher_bas": input.qualite_isolation_plancher_bas(),
            "qualite_isolation_murs": input.qualite_isolation_murs(),

            # Vos installations énergétiques
            "type_installation_chauffage": input.type_installation_chauffage(),
            "type_energie_principale_chauffage": input.type_energie_principale_chauffage(),
            "type_installation_ecs": input.type_installation_ecs(),
            "type_generateur_n1_ecs_n1": input.type_generateur_n1_ecs_n1(),
            "type_generateur_chauffage_principal": input.type_generateur_chauffage_principal(),
        }


        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(FASTAPI_URL, json=payload)
                response.raise_for_status()
                result_json = response.json()
        except Exception as e:
            result_json = {"status": "error", "message": str(e)}

        modal = show_results_modal(result_json)
        ui.modal_show(modal)
