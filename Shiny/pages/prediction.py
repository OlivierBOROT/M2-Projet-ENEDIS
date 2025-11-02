from shiny import ui

def page():
    return ui.div(
        ui.h2("Questionnaire Logement et Installations Énergétiques"),
        
        ui.row(
            # Colonne 1 : Votre logement 1/2
            ui.column(
                4,  # largeur sur 12
                ui.h3("Votre logement 1/2"),
                ui.input_select("type_logement", "Type de logement:", 
                               ["maison","appartement"]),
                ui.input_numeric("surface", "Surface (m²):", 0),
                ui.input_text("code_postal", "Code postal:"),
                ui.input_text("commune", "Commune:"),
                ui.input_numeric("annee_construction", "Année de construction:", 0)
            ),
            
            # Colonne 2 : Votre logement 2/2
            ui.column(
                4,
                ui.h3("Votre logement 2/2"),
                ui.input_numeric("nombre_niveau_logement", "Nombre de niveaux chauffés:", 0),
                ui.input_numeric("hauteur_sous_plafond", "Hauteur sous plafond (m):", 0),
                ui.input_select("isolation_toiture", "Isolation du toit:", 
                                ["Bonne", "Moyenne", "Faible"]),
                ui.input_checkbox("logement_dessus", "Logement au-dessus ?"),
                ui.input_select("isolation_plancher", "Isolation du plancher:", 
                                ["Bonne", "Moyenne", "Faible"]),
                ui.input_select("isolation_murs", "Isolation des murs:", 
                                ["Bonne", "Moyenne", "Faible"])
            ),
            
            # Colonne 3 : Vos installations énergétiques
            ui.column(
                4,
                ui.h3("Vos installations énergétiques"),
                ui.input_select("type_chauffage", "Type de chauffage:", 
                                ["Central", "Individuel", "Pompe à chaleur", "Autre"]),
                ui.input_select("energie_chauffage", "Énergie de chauffage:", 
                                ["Électricité", "Gaz", "Fioul", "Bois", "Autre"]),
                ui.input_checkbox("climatisation", "Climatisation présente ?")
            )
        ),
        
        # Bouton pour soumettre le formulaire
        ui.input_action_button("submit", "Soumettre"),
        
        # Affichage des résultats
        ui.output_text_verbatim("result")
    )
