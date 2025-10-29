from shiny import ui

INPUTS = {
    "type_logement": ui.input_select("type_logement", "Type de logement", choices=['Maison','Appartement']),
    "surface": ui.input_numeric("surface","Surface Habitable en m²", None,min=0, max=1000, step=0.1),
    "code_postal": ui.input_numeric("code_postal", "Code Postal", None, min=0, max=99000, step=1),
    "commune": ui.input_text("commune", "Commune"),
    "annee_construction": ui.input_select("annee_construction", "Année de construction du logement",
                                          choices=["","Avant 1960","1961-1970","1971-1980","1981-1990","1991-2000","2001-2010","Après 2010"]),
    "nb_nvx_chauffes": ui.input_numeric("nb_nvx_chauffes", "Nombre de niveau chauffés", None, min=1, max=3, step=1),
    "hauteur_plafond": ui.input_radio_buttons("hauteur_plafond", "Hauteur sous plafond (en m)", choices=[2,2.5,3,3.5,"Je ne sais pas"],selected=[],inline=True,),
    "isolation_toit":ui.input_select("isolation_toit","L'isolation de votre toit a-t-elle été refaite au cours des 20 dernières années?", choices=["Oui","Non","Je ne sais pas"]),
    "logement_dessus":ui.input_radio_buttons("logement_dessus", "Y a-t-il un logement au dessus du vôtre?",choices=["Oui","Non"],selected=[],inline=True,),
    "isolation_plancher":ui.input_select("isolation_plancher","Que trouve-t-on sous votre plancher?", choices=["Terre plein","Vide sanitaire/Sous sol non isolé","Vide sanitaire/Sous-sol isolé","Espace chauffé/Autre logement"]),
    "isolation_murs":ui.input_select("isolation_murs","Quand a été refaite l'isolation de vos murs pour la dernière fois?", choices=["Les murs n'ont pas été isolés","Il y a plus de 20 ans","Entre 20 et 10 ans","Il y a moins de 10 ans","Je ne sais pas"]),
    "type_chauffage":ui.input_radio_buttons("type_chauffage", "Votre installation de chauffage est-elle collective ou individuelle?", choices=["Chauffage Collectif","Chauffage Individuel"],selected=[],inline=True,),
    "energie_chauffage":ui.input_select("energie_chauffage","Votre énergie de chauffage principale", choices= ['Électricité', 'Gaz naturel', 'Réseau de Chauffage urbain', 'Bois – Granulés (pellets) ou briquettes', 'Fioul domestique', 'Bois – Bûches', 'Butane', 'Propane', 'Bois – Plaquettes forestières', 'Bois – Plaquettes d’industrie', 'Charbon', "Électricité d'origine renouvelable utilisée dans le bâtiment"]),
    "climatisation":ui.input_radio_buttons("climatisation","Avez-vous une installation de climatisation?", choices=["Oui", "Non"],selected=[],inline=True,),
}
