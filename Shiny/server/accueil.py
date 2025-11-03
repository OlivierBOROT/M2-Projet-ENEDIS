import asyncio
from shiny import ui, reactive
from pathlib import Path

here = Path(__file__).parent.parent

def setup_accueil(session):
    accueil_readme_path = here / "content" / "accueil.md"
    with open(accueil_readme_path, "r", encoding="UTF-8") as f:
        readme = f.read()

    readme_chunks = readme.replace("\n", " \n ").split(" ")

    async def chunk_generator():
        # await asyncio.sleep(1.00)
        for chunk in readme_chunks:
            await asyncio.sleep(0.02)
            yield chunk + " "

    md = ui.MarkdownStream("accueil_readme")

    @reactive.effect
    async def _():
        await md.stream(chunk_generator())

    return md