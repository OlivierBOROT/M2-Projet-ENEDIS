from ipyleaflet import GeoJSON, Map, Marker  
from shiny import App, ui
from shinywidgets import output_widget, render_widget  

def setup_carto(input, output, session):
    @render_widget  
    def map():
        map = Map(center=(50.6252978589571, 0.34580993652344), zoom=3) 
        return map
