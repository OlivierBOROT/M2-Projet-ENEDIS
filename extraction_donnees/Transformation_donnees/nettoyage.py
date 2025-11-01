import re
import unicodedata
from stop_words import STOP_WORDS_FR

def nettoyer(text: str) -> str:
    """
    Nettoie et normalise un texte en français.

    Étapes :
    1. Normalisation Unicode en NFKC et conversion en minuscules.
    2. Suppression des chiffres.
    3. Suppression des caractères spéciaux (ne conservant que lettres et espaces).
    4. Remplacement des espaces multiples par un seul espace.
    5. Suppression des stop words français.

    Args:
        text (str | None): Texte à nettoyer.

    Returns:
        str: Texte nettoyé.
    """


    if not isinstance(text, str):
        return ""

    # transformation
    text = unicodedata.normalize("NFKC", text.lower())
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"[^a-zàâçéèêëîïôûùüÿñæœ\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = [t for t in text.split() if t not in STOP_WORDS_FR]
    return " ".join(tokens)
