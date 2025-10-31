import re
import unicodedata
from variables_globales import STOP_WORDS_FR

def nettoyer(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize("NFKC", text.lower())
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"[^a-zàâçéèêëîïôûùüÿñæœ\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = [t for t in text.split() if t not in STOP_WORDS_FR]
    return " ".join(tokens)
