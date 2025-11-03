from shiny import ui

def page():
    return ui.page_fluid(
        ui.h2("🏠 Questionnaire : Logement et Installations Énergétiques", class_="text-center mb-4"),

        ui.layout_columns(
            # --- Prediction type and model selection ---
            ui.card(
                ui.card_header("Prédiction"),
                ui.layout_columns(
                    ui.input_select("prediction_type", "Type de prédiction :", ["DPE", "CONSO"]),
                    ui.input_select("selected_model", "Modèle :", choices=[], selected=None),
                    col_widths=(3, 3)  # adjust as needed
                ),
                fill=True,
            ),

            # Card with the submit button
            ui.card(
                ui.card_header("Soumettre le formulaire"),
                ui.layout_columns(
                    ui.div(
                        ui.input_action_button("submit", "Soumettre", class_="btn btn-primary"),
                        style="display:flex; justify-content:center; align-items:center; height:100%;"
                    ),
                ),
                fill=True,
            ),
            col_widths=(6, 6),
        ),

        # --- Inputs ---
        ui.layout_columns(
            ui.card(
                ui.card_header("Votre logement (1/2)"),
                ui.output_ui("type_batiment_ui"),
                ui.output_ui("surface_habitable_logement_ui"),
                ui.output_ui("nombre_niveau_logement_ui"),
                ui.output_ui("periode_construction_ui"),
                ui.output_ui("code_postal_ban_ui"),
                fill=True
            ),
            ui.card(
                ui.card_header("Votre logement (2/2)"),

                ui.output_ui("hauteur_sous_plafond_ui"),
                ui.output_ui("isolation_toiture_ui"),
                ui.output_ui("qualite_isolation_plancher_bas_ui"),
                ui.output_ui("qualite_isolation_murs_ui"),
                fill=True
            ),
            ui.card(
                ui.card_header("Vos installations énergétiques"),
                ui.output_ui("type_installation_chauffage_ui"),
                ui.output_ui("type_energie_principale_chauffage_ui"),
                ui.output_ui("type_installation_ecs_ui"),
                ui.output_ui("type_generateur_n1_ecs_n1_ui"),
                ui.output_ui("type_generateur_chauffage_principal_ui"),
                fill=True
            )
        ),
    )
