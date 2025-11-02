import pandas as pd
import plotly.express as px
from shiny import render, reactive, Session, ui 
from shinywidgets import render_widget

# ----------------------------------------------------
# Fonction de setup pour la page Graphs
# ----------------------------------------------------
def setup_graphs(input, output, session: Session, dataset, dpe_choices): 
    
    # ----------------------------------------------------
    # Calcul réactif : Filtration des données DPE
    # ----------------------------------------------------
    @reactive.calc
    def data_filtered_dpe():
        """Filtre les données en fonction de l'input 'select_periode_construction'."""
        df = dataset()  
        
        # 1. Filtration par période de construction
        periode_selectionnee = input.select_periode_construction() 
        
        if periode_selectionnee and periode_selectionnee != "Toutes":
            df = df[df['periode_construction'] == periode_selectionnee]
            
        # On exclut les valeurs manquantes ou non renseignées pour l'étiquette DPE
        df = df.dropna(subset=['etiquette_dpe'])
        
        return df

    # ----------------------------------------------------
    # GRAPHIQUE 1 : Histogramme de répartition des étiquettes DPE (Plotly Interactif)
    # ----------------------------------------------------
    @output
    @render_widget
    def graph1():
        df_local = data_filtered_dpe()

        if df_local.empty:
            return None 
        
        # Définition de l'ordre canonique des étiquettes DPE
        dpe_orders = ["A", "B", "C", "D", "E", "F", "G"]
        
        # Création du graphique avec Plotly Express
        fig = px.histogram(
            df_local, 
            x='etiquette_dpe', 
            category_orders={"etiquette_dpe": dpe_orders}, 
            color='etiquette_dpe', 
            title="Répartition des Étiquettes DPE (Filtrage par Période de Construction)",
            template="plotly_white"
        )
        
        # Mise à jour des labels
        fig.update_xaxes(title_text="Étiquette DPE")
        fig.update_yaxes(title_text="Nombre de Logements")
        
        return fig
        
    # ----------------------------------------------------
    # GRAPHIQUE 2, 3, 4 et KPI (stubs)
    # ----------------------------------------------------
    @output
    @render.plot
    def graph2():
        return None 
        
    @output
    @render.plot
    def graph3():
        return None 
        
    @output
    @render.plot
    def graph4():
        return None 
        
    # ----------------------------------------------------
    # LOGIQUE D'INITIALISATION : Mise à jour du menu déroulant
    # ----------------------------------------------------
    @session.on_flush
    def init_ui():
        """Met à jour les choix du menu déroulant 'Période de Construction'
           avec les vraies modalités des données (non réactif)."""
        
        ui.update_select(
            "select_periode_construction",
            choices=dpe_choices,
            selected="Toutes"
        )