import pandas as pd
from typing import List, Union

def detect_outliers_via_bornes(
    df: pd.DataFrame,
    cols: List[str],
    bornes: List[List[Union[float, int]]],
    multiple_cols: bool = True
    ) -> pd.DataFrame:
    """
    Détecte les valeurs aberrantes dans un DataFrame en utilisant des bornes pour chaque colonne.

    Les valeurs situées en dehors des bornes spécifiées sont marquées comme outliers.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame contenant les colonnes à vérifier.
    cols : list[str]
        Liste des colonnes à vérifier.
    bornes : list[list[float, float]]
        Liste des bornes [min, max] pour chaque colonne.
        Si multiple_cols=True, la longueur de bornes doit correspondre à celle de cols.
    multiple_cols : bool, default True
        - True : crée une colonne de sortie pour chaque colonne (col_outlier).
        - False : crée une seule colonne "_outlier" indiquant au moins un outlier.

    Returns
    -------
    pd.DataFrame
        DataFrame avec les colonnes supplémentaires indiquant les outliers.

    Raises
    ------
    ValueError
        Si les bornes ne correspondent pas aux colonnes ou ne sont pas valides.
    """


    # Vérifications
    if multiple_cols and len(cols) != len(bornes):
        raise ValueError(
            "Le nombre de colonnes et de bornes doit être identique quand multiple_cols=True."
            )

    for i, b in enumerate(bornes):
        if not (isinstance(b, (list, tuple)) and len(b) == 2):
            raise ValueError(
                f"La borne pour la colonne '{cols[i]}' doit être un tuple ou une liste de 2 floats."
            )
        if not all(isinstance(x, (int, float)) for x in b):
            raise ValueError(
                f"Les bornes pour la colonne '{cols[i]}' doivent être des nombres."
            )


    # Création du DataFrame des outliers de manière vectorisée
    outlier_temp = pd.DataFrame({
        f"{col}_outlier": ~df[col].between(bornes[i][0], bornes[i][1])
        for i, col in enumerate(cols)
    }, index=df.index)

    if multiple_cols:
        # Ajouter toutes les colonnes _outlier
        df = pd.concat([df, outlier_temp], axis=1)
    else:
        # Une seule colonne _outlier globale
        df["_outlier"] = outlier_temp.any(axis=1)

    return df
