import pandas as pd
import plotly.express as px
from shiny import render, reactive, Session, ui 
from shinywidgets import render_widget

# ----------------------------------------------------
# Fonction de setup pour la page Graphs
# ----------------------------------------------------
# Signature mise à jour pour inclure logement_choices
def setup_graphs(input, output, session: Session, dataset, dpe_choices, energie_choices, logement_choices): 
    
    # ----------------------------------------------------
    # Calcul réactif : FILTRATION PAR PÉRIODE (Filtre N°1)
    # ----------------------------------------------------
    @reactive.calc
    def data_filtered_periode():
        """Filtre les données en fonction de l'input 'select_periode_construction'."""
        df = dataset()  
        
        # 1. Filtration par période de construction
        periode_selectionnee = input.select_periode_construction() 
        
        if periode_selectionnee and periode_selectionnee != "Toutes":
            df = df[df['periode_construction'] == periode_selectionnee]
            
        return df

    # ----------------------------------------------------
    # Calcul réactif : FILTRATION PAR ÉNERGIE (Filtre N°2)
    # ----------------------------------------------------
    @reactive.calc
    def data_filtered_energie():
        """Filtre les données en fonction de l'input 'select_energie_chauffage' (Dépend de la Période)."""
        df = data_filtered_periode() # Dépend du filtre Période
        
        # 1. Filtration par énergie
        energie_col = 'type_energie_principale_chauffage'
        energie_selectionnee = input.select_energie_chauffage()
        
        if energie_selectionnee and energie_selectionnee != "Toutes":
            df = df[df[energie_col] == energie_selectionnee]
            
        return df

    # ----------------------------------------------------
    # Calcul réactif : SOURCE DE DONNÉES FINALE (Intègre tous les filtres G1, G2, G3)
    # ----------------------------------------------------
    @reactive.calc
    def data_filtered_finale():
        """Source unique combinant les filtres Période et Énergie."""
        
        df = data_filtered_energie()  
        
        # On exclut les valeurs manquantes sur les colonnes clés (pour le traçage)
        df = df.dropna(subset=['etiquette_dpe', 'type_energie_principale_chauffage', 'surface_habitable_logement', 'type_batiment'])
        
        return df
        
    # ----------------------------------------------------
    # Calcul réactif : FILTRATION G4 (Type de Bâtiment)
    # ----------------------------------------------------
    @reactive.calc
    def data_filtered_g4():
        """Filtre la source finale par Type de Bâtiment (pour G4 uniquement)."""
        df = data_filtered_finale()
        
        type_batiment_selectionne = input.select_type_batiment()
        
        if type_batiment_selectionne and type_batiment_selectionne != "Toutes":
            df = df[df['type_batiment'] == type_batiment_selectionne]
        
        return df


    # ----------------------------------------------------
    # GRAPHIQUE 1, 2, 3 (Utilisent data_filtered_finale)
    # ----------------------------------------------------
    @output
    @render_widget
    def graph1():
        # Utilise la source de données finale (G1, G2, G3)
        df_local = data_filtered_finale() 
        if df_local.empty: return None 
        dpe_orders = ["A", "B", "C", "D", "E", "F", "G"]
        dpe_colors_map = {"A": "#008237", "B": "#62c733", "C": "#c7c733", "D": "#f7d300", "E": "#e98e29", "F": "#e34327", "G": "#c60e0d"}
        fig = px.histogram(df_local, x='etiquette_dpe', category_orders={"etiquette_dpe": dpe_orders}, color='etiquette_dpe', color_discrete_map=dpe_colors_map, title="Répartition des Étiquettes DPE (Filtrage Combiné)", template="plotly_white")
        fig.update_xaxes(title_text="Étiquette DPE")
        fig.update_yaxes(title_text="Nombre de Logements")
        return fig
    
    @output
    @render_widget
    def graph2():
        # Utilise la source de données finale (G1, G2, G3)
        df_local = data_filtered_finale() 
        if df_local.empty: return None 
        dpe_orders = ["A", "B", "C", "D", "E", "F", "G"]
        dpe_colors_map = {"A": "#008237", "B": "#62c733", "C": "#c7c733", "D": "#f7d300", "E": "#e98e29", "F": "#e34327", "G": "#c60e0d"}
        conso_col = 'conso_5_usages_ef' 
        try:
            df_clean = df_local.dropna(subset=[conso_col])
            df_agg = df_clean.groupby('etiquette_dpe')[[conso_col]].mean().reset_index()
            df_agg = df_agg.rename(columns={conso_col: 'consommation_moyenne'})
            if df_agg.empty: return None
            fig = px.bar(df_agg, x='etiquette_dpe', y='consommation_moyenne', category_orders={"etiquette_dpe": dpe_orders}, color='etiquette_dpe', color_discrete_map=dpe_colors_map, title="Consommation Énergétique Moyenne par DPE (Consommation Brute)", template="plotly_white")
            fig.update_xaxes(title_text="Étiquette DPE")
            fig.update_yaxes(title_text="Consommation Moyenne")
            return fig
        except KeyError: return None
        except Exception: return None
        
    @output
    @render_widget 
    def graph3():
        # Utilise la source de données finale (G1, G2, G3)
        df_local = data_filtered_finale() 
        if df_local.empty: return None 
        df_counts = df_local['etiquette_dpe'].value_counts().reset_index()
        df_counts.columns = ['etiquette_dpe', 'count']
        fig = px.pie(df_counts, names='etiquette_dpe', values='count',color='etiquette_dpe',category_orders={"etiquette_dpe": ["A", "B", "C", "D", "E", "F", "G"]},
            color_discrete_map={
                "A": "#008237", "B": "#62c733", "C": "#c7c733", "D": "#f7d300", "E": "#e98e29", "F": "#e34327", "G": "#c60e0d"},
            title="Répartition des Étiquettes DPE pour l'Énergie sélectionnée",hole=.3)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig

    # ----------------------------------------------------
    # GRAPHIQUE 4 : Courbe de la Surface Moyenne par Période de Construction et Type de Bâtiment
    # ----------------------------------------------------
    @output
    @render_widget 
    def graph4():
        # Utilise les données filtrées par Période/Énergie ET par Type de Bâtiment (Filtre G4)
        df = data_filtered_g4() 
        
        if df.empty:
            return None

        # Préparation de l'ordre des périodes (pour l'axe X)
        period_orders = [c for c in dpe_choices if c != "Toutes"]
        
        # 1. Agrégation: Calcul de la surface moyenne par Période
        df_grouped = (
            df
            .groupby('periode_construction')['surface_habitable_logement']
            .mean()
            .reset_index(name='surface_moyenne')
        )
        
        if df_grouped.empty:
            return None

        # 2. Création du graphique en COURBE
        fig = px.line(
            df_grouped,
            x='periode_construction', 
            y='surface_moyenne',
            # Nous utilisons color='type_batiment' uniquement si nous avions plusieurs types par période,
            # mais ici on veut une seule courbe pour le type filtré.
            # On utilise donc un style plus simple.
            title="Évolution de la Surface Moyenne par Période de Construction",
            labels={
                'periode_construction': 'Période de Construction', 
                'surface_moyenne': 'Surface Moyenne ($m^2$)'
            },
            template="plotly_white"
        )
        
        # Ajout des marqueurs sur la courbe
        fig.update_traces(mode='lines+markers') 
        # Assure l'ordre des catégories sur l'axe X
        fig.update_xaxes(categoryorder='array', categoryarray=period_orders)

        return fig

    # ----------------------------------------------------
    # LOGIQUE D'INITIALISATION : Mise à jour des menus déroulants
    # ----------------------------------------------------
    @session.on_flush
    def init_ui():
        """Met à jour les choix des menus déroulants avec les vraies modalités."""
        
        # Mise à jour du filtre Période de Construction
        ui.update_select(
            "select_periode_construction",
            choices=dpe_choices,
            selected="Toutes"
        )
        
        # Mise à jour du filtre Énergie de Chauffage
        ui.update_select(
            "select_energie_chauffage",
            choices=energie_choices,
            selected="Toutes"
        )
        
        # Mise à jour du filtre Type de Bâtiment (G4)
        ui.update_select(
            "select_type_batiment",
            choices=logement_choices,
            selected="Toutes"
        )
