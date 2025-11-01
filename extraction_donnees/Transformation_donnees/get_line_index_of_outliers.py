import pandas as pd
from typing import List, Dict, Union

def get_line_index_of_outliers(
        df: pd.DataFrame,
        cols: list[str],
        as_dict: bool = False
    )-> Union[List[int], Dict[str, List[int]]]:

    """
    Retourne les index des lignes contenant au moins une valeur aberrante
    détectée dans les colonnes spécifiées.

    Parameters
    ----------
    df : pd.DataFrame
        Le DataFrame contenant les colonnes d'indicateurs d'outliers (booléens).
    cols : list[str]
        Liste des colonnes à vérifier (ex: ['lat_outlier', 'lon_outlier']).
    as_dict : bool, optional
        - False (par défaut) : retourne une liste unique des index de lignes ayant au moins un outlier.
        - True : retourne un dictionnaire {colonne: [index des lignes outliers pour cette colonne]}.

    Returns
    -------
    list[int] ou dict[str, list[int]]
        Index des lignes contenant des valeurs aberrantes.

    Raises
    ------
    ValueError
        Si aucune des colonnes spécifiées n'existe dans le DataFrame.
    """

    if not cols:
        raise ValueError("La liste de colonnes est vide.")
    if not all(col in df.columns for col in cols):
        missing = [col for col in cols if col not in df.columns]
        raise ValueError(f"Colonnes manquantes dans le DataFrame : {missing}")

    if as_dict:
        return {col: df.index[df[col]].tolist() for col in cols}

    # union des index où au moins un outlier = True
    mask = df[cols].any(axis=1)
    return df.index[mask].tolist()
