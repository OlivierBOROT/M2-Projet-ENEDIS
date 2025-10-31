import pandas as pd

def get_line_index_of_outliers(df: pd.DataFrame, cols: list[str], as_dict: bool = False):
    """
    Retourne les index des lignes contenant au moins une valeur aberrante détectée
    dans les colonnes spécifiées.

    Paramètres
    ----------
    df : pd.DataFrame
        Le DataFrame contenant les colonnes d'indicateurs d'outliers.
    cols : list[str]
        Liste des colonnes (ex: ['lat_outlier', 'lon_outlier']).
    as_dict : bool, optional
        - False (défaut) : retourne une liste unique des index de lignes ayant au moins un outlier.
        - True : retourne un dictionnaire {colonne: [index des lignes outliers pour cette colonne]}.

    retour
    ------
    list[int] ou dict[str, list[int]]
    """
    if not cols or not all(col in df.columns for col in cols):
        raise ValueError("Aucune colonne d'outliers détectée dans le DataFrame.")

    if as_dict:
        return {
            col: df.index[df[col]].tolist()
            for col in cols
        }
    # union des index où au moins un outlier = True
    mask = df[cols].any(axis=1)
    return df.index[mask].tolist()
