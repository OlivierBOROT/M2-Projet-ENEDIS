import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Callable

from variables_globales import DEBUG

def regrouper_colonne_en_classes(
    colonne: pd.Series,
    classes_existantes: list,
    cleaner: Callable[[str], str] | None,
):
    """
    Regroupe les textes d'une colonne autour des classes existantes fournies
    en utilisant TF-IDF + cosine similarity.
    """
    if DEBUG:
        print("Nettoyage des textes uniques...")
    # Valeurs uniques
    uniques = colonne.fillna("").unique()
    uniques = pd.Series(uniques)
    uniques = uniques[uniques.str.strip() != ""]
    uniques_nettoye  = uniques.copy()
    if cleaner:
        uniques_nettoye = uniques.apply(cleaner)

    if DEBUG:
        print(f"Encodage TF-IDF pour {len(uniques_nettoye)} valeurs uniques...")

    # Nettoyage des classes existantes
    classes_nettoye = pd.Series(classes_existantes)
    if cleaner:
        classes_nettoye = pd.Series(classes_existantes).apply(cleaner)

    # TF-IDF
    vect = TfidfVectorizer().fit(classes_nettoye)
    X_uniques = vect.transform(uniques_nettoye)
    Y_classes = vect.transform(classes_nettoye)

    if DEBUG:
        print("Calcul des similarités cosinus...")
    sim_matrix = cosine_similarity(X_uniques, Y_classes)
    assigned_indices = sim_matrix.argmax(axis=1)
    assigned_labels = [classes_existantes[i] for i in assigned_indices]

    # Mapping pour réappliquer au DataFrame complet
    mapping = dict(zip(uniques, assigned_labels))

    df = pd.DataFrame({"texte": colonne})
    df["classe_lisible"] = df["texte"].map(mapping)
    df["cluster"] = df["classe_lisible"].apply(
        lambda x: classes_existantes.index(x) if x in classes_existantes else -1
    )

    if DEBUG:
        print("fonction terminée.")
    return df
