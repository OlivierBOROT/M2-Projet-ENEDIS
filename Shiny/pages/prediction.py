from shiny import ui

def page():
    return ui.page_fluid(
        ui.h2("🏠 Questionnaire : Logement et Installations Énergétiques", class_="text-center mb-4"),

        ui.row(
            # Left card: Prediction
            ui.column(
                6,  # ensures column takes 6/12 of width
                ui.card(
                    ui.card_header("Prédiction"),
                    ui.layout_columns(
                        ui.input_select("prediction_type", "Type de prédiction :", ["DPE", "CONSO"]),
                        ui.output_ui("selected_model"),
                        col_widths=(6, 6),  # internal columns each take half of card
                        style="align-items:center; width:100%;"
                    ),
                    fill=True,
                    style="height: 100%;"
                )
            ),
            # Right card: Actions
            ui.column(
                6,  # ensures column takes 6/12 of width
                ui.card(
                    ui.card_header("Actions"),
                    ui.layout_columns(
                        ui.input_action_button("submit", "Prédire", class_="btn btn-primary"),
                        ui.input_action_button("dl_model",
                                               "Télécharger le modèle",
                                               class_="btn btn-secondary"),
                        col_widths=(6, 6),
                        style="justify-content: space-between; align-items: center; width:100%;"
                    ),
                    fill=True,
                    style="height: 100%;"
                )
            )
        ),
        ui.hr(),
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
