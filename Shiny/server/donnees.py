from shiny import App, Inputs, Outputs, Session, render, ui
import pandas as pd
import random
import asyncio
from io import BytesIO

from datetime import date

def setup_donnees(input, output, session, dataset):
    # PRESENTATION DES DONNEES

    # SCHEMAS EXPLICATIFS

    # TABLEAU : variation du nombre de lignes du header
    @output
    @render.data_frame
    def render_data_head():
        df = dataset().copy()
        n = input.nrows() or 10
        a_afficher = df.head(n)
        return render.DataGrid(a_afficher)

    # TABLEAU : DL header
    @render.download(
        filename = lambda: f"{date.today().isoformat()}-{random.randint(100, 999)}.csv"
    )
    async def save_head_data():
        await asyncio.sleep(0.25)
        df = dataset().copy()
        n = input.nrows() or 10
        a_afficher = df.head(n)

        # transformation en csv
        csv_buffer = BytesIO()
        a_afficher.to_csv(csv_buffer, index=False, encoding='utf-8')
        yield csv_buffer.getvalue()

    # TABLEAU : DL tout
    @render.download(
        filename = lambda: f"{date.today().isoformat()}-{random.randint(100, 999)}.csv"
    )
    async def save_all_data():
        await asyncio.sleep(0.25)
        df = dataset().copy()

        # transformation en csv
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False, encoding='utf-8')
        yield csv_buffer.getvalue()
