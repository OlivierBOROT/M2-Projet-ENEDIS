import folium
import pandas as pd
import branca.colormap as cm
from shiny import render, reactive
from shinywidgets import render_widget
from pathlib import Path
import json
from io import BytesIO
from datetime import date
import random
import asyncio
import tempfile

here = Path(__file__).parent.parent
DEPARTEMENTS_GEOJSON_PATH = here / "data" / "departments_region84.geojson"
CODES_POSTAUX_GEOJSON_PATH = here / "data" / "codes_postaux_aura.geojson"

# Load GeoJSON files
with open(DEPARTEMENTS_GEOJSON_PATH, "r", encoding="utf-8") as f:
    departements_gdf = json.load(f)

with open(CODES_POSTAUX_GEOJSON_PATH, "r", encoding="utf-8") as f:
    codes_postaux_gdf = json.load(f)

DPE_COLORS = {
    "A": "#1a9850",  # green
    "B": "#66bd63",
    "C": "#a6d96a",
    "D": "#d9ef8b",
    "E": "#fee08b",
    "F": "#fdae61",
    "G": "#d73027"   # red
}

MAPS_DIR = here / Path("maps")
MAPS_DIR.mkdir(exist_ok=True)

def setup_carto(input, output, session, dataset):
    current_map = reactive.Value("")

    @render.ui
    def render_map():
        df = dataset().copy()
        kpi_choice = input.kpi_choice()
        geo_level = input.geo_level()

        # Choose geo level
        if geo_level == "par département":
            geojson_data = departements_gdf
            geojson_code_field = "code"
            group_col = "code_departement_ban"
            # zero-pad department codes to 2 digits
            df[group_col] = df[group_col].apply(lambda x: str(x).zfill(2))
        else:
            geojson_data = codes_postaux_gdf
            geojson_code_field = "ID"
            group_col = "code_postal_ban"
            df[group_col] = df[group_col].astype(str)

        use_categorical = False
        # Aggregate KPI
        if kpi_choice == "moyenne du DPE":
            map_data = df.groupby(group_col)["etiquette_dpe"].agg(
                lambda x: x.mode()[0] if not x.mode().empty else None
            ).reset_index()
            value_dict = map_data.set_index(group_col)["etiquette_dpe"].to_dict()
            use_categorical = True
        else:
            if kpi_choice == "consommation moyenne":
                map_data = df.groupby(group_col, dropna=False).agg(
                    value=("conso_5_usages_ef", "mean")
                ).reset_index()
            elif kpi_choice == "nombre de logements":
                map_data = df.groupby(group_col, dropna=False).agg(
                    value=("etiquette_dpe", "count")
                ).reset_index()
            elif kpi_choice == "zones à rénover":
                map_data = df[df["etiquette_dpe"].isin(["F", "G"])].groupby(group_col).agg(
                    value=("etiquette_dpe", "count")
                ).reset_index()
            else:
                map_data = pd.DataFrame({group_col: [], "value": []})

            # Map from code to KPI value
            value_dict = map_data.set_index(group_col)["value"].to_dict()

        # Create colormap
        colormap = None
        if not use_categorical and map_data["value"].notna().any():
            min_val, max_val = map_data["value"].min(), map_data["value"].max()
            colormap = cm.LinearColormap(["yellow", "orange", "red"], vmin=min_val, vmax=max_val)

        # Create Folium map
        m = folium.Map(location=[45.7, 4.9], zoom_start=7, control_scale=True)

        # Style function for GeoJSON
        def style_function(feature):
            region_code = feature["properties"].get(geojson_code_field)
            val = value_dict.get(region_code)
            if use_categorical:
                fill_color = DPE_COLORS.get(val, "#ffffff")
            else:
                fill_color = colormap(val) if val is not None else "#ffffff"
            return {
                "fillColor": fill_color,
                "color": "black",
                "weight": 1,
                "fillOpacity": 0.7
            }

        # Add GeoJSON with tooltip
        folium.GeoJson(
            geojson_data,
            style_function=style_function,
            tooltip=folium.GeoJsonTooltip(
                fields=[geojson_code_field],
                aliases=["Code"],
            ),
        ).add_to(m)

        if not use_categorical and colormap is not None:
            colormap.caption = kpi_choice
            colormap.add_to(m)

        # Add a background tile layer before saving
        folium.TileLayer(
            tiles="OpenStreetMap",  # or another provider
            name="Background",
            attr="Map data © OpenStreetMap contributors",
            control=True
        ).add_to(m)

        # Optional: add LayerControl if you want
        folium.LayerControl().add_to(m)

        # Save to a temporary file and store path reactively
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp_file:
            m.save(tmp_file.name)
            current_map.set(tmp_file.name)  # store temp path

        return m

    @render.download(
    filename=lambda: f"{date.today().isoformat()}-{random.randint(100, 999)}.html"
    )
    async def download_map():
        temp_map_path = current_map.get()
        if not temp_map_path:
            yield b""
            return

        with open(temp_map_path, "rb") as f:
            yield f.read()
