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
                ui.input_numeric("surface", "Surface (en m²):", 0),
                ui.input_text("code_postal", "Code postal:"),
                ui.input_text("commune", "Commune:"),
                ui.input_select("annee_construction", "Année de construction du logement",
                                          choices=["","Avant 1960","1961-1970","1971-1980","1981-1990","1991-2000","2001-2010","Après 2010"]),
            
            # Colonne 2 : Votre logement 2/2
            ui.column(
                4,
                ui.h3("Votre logement 2/2"),
                ui.input_numeric("nombre_niveau_logement", "Nombre de niveaux chauffés:", 0),
                ui.input_numeric("hauteur_sous_plafond", "Hauteur sous plafond (en m):", 0),
                ui.input_select("isolation_toiture", "Votre toiture a-telle été isolée, ou y a-t-il un logement au dessus du vôtre?", 
                                ["Oui", "Non"]),
                ui.input_select("isolation_plancher", "La qualité d'isolation de votre plancher:", 
                                ["très bonne","bonne", "moyenne", "insuffisante"]),
                ui.input_select("isolation_murs", "La qualité d'isolation de vos murs :", 
                                ["très bonne","bonne", "moyenne", "insuffisante"])
            ),
            
            # Colonne 3 : Vos installations énergétiques
            ui.column(
                4,
                ui.h3("Vos installations énergétiques"),
                ui.input_select("type_chauffage", "Votre type d'installation de chauffage:", 
                                ["collectif", "individuel", "Mixte"]),
                ui.input_select("energie_chauffage", "Votre principale énergie de chauffage :", 
                                ['Électricité', 'Gaz naturel', 'Réseau de Chauffage urbain', 'GPL',
                                 'Bois – Granulés (pellets) ou briquettes', 'Fioul domestique',
                                 'Bois – Bûches', 'Butane', 'Propane',
                                 'Bois – Plaquettes forestières', 'Bois – Plaquettes d’industrie',
                                 'Charbon',"Électricité d'origine renouvelable utilisée dans le bâtiment"]),
                ui.input_select("type_generateur_chauffage", "Votre principal générateur de chauffage :", 
                               ['Chaudière bois','Chaudière charbon','Chaudière électrique','Chaudière fioul','Chaudière gaz', 'Chaudière gpl/propane/butane', 
                                'convecteur bi-jonction','Convecteur électrique','réseau de chaleur', 
                                'PAC air/eau - Pompe à chaleur','PAC géothermique','pompe à chaleur hybride','Plancher ou plafond rayonnant électrique',
                                'Poêle / Cuisinière / Foyers / insert flamme verte','autre système / émetteurs'])
                ui.input_select("type_ecs", "Votre type d'installation de production d'eau chaude:", 
                                ["collectif", "individuel", "Mixte"]),
                 ui.input_select("type_generateur_ecs", "Votre principale installation pour la production d'eau chaude :", 
                               [ 'Accumulateur gaz', 'Ballon électrique','CET sur air',
                                'Chaudière bois','Chaudière charbon','chaudière condensation', 'Chaudière fioul','Chaudière gaz','Chaudière gpl/propane/butane',
                                'chauffe-eau électrique','Chauffe-eau gaz',
                                PAC / pompe à chaleur', 'Réseau de chaleur','autre système / émetteurs'])
            )
        ),
        
        # Bouton pour soumettre le formulaire
        ui.input_action_button("submit", "Soumettre"),
        
        # Affichage des résultats
        ui.output_text_verbatim("result")
    )
