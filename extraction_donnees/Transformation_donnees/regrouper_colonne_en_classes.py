import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Callable, Optional, List


from variables_globales import DEBUG

def regrouper_colonne_en_classes(
    colonne: pd.Series,
    classes_existantes: List[str],
    cleaner: Optional[Callable[[str], str]] = None,
) -> pd.DataFrame:
    """
    Regroupe les textes d'une colonne autour des classes existantes en utilisant
    TF-IDF et la similarité cosinus.

    Chaque valeur unique de la colonne est comparée aux classes existantes,
    et assignée à la classe la plus similaire.

    Parameters
    ----------
    colonne : pd.Series
        Série contenant les textes à regrouper.
    classes_existantes : list[str]
        Liste des classes cibles existantes/voulues.
    cleaner : Callable[[str], str] | None, optional
        Fonction de nettoyage à appliquer sur les textes(ex: suppression de stop words, normalisation).
        Si None, aucun nettoyage n'est appliqué.

    Returns
    -------
    pd.DataFrame
        DataFrame contenant :
        - 'texte' : texte original
        - 'classe_lisible' : classe assignée
        - 'cluster' : indice de la classe dans `classes_existantes`
    """


    if DEBUG:
        print("Nettoyage des textes uniques...")

    # Valeurs uniques non vides
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

    # calcul de la matrice de similarité
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
