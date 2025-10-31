import pandas as pd

def detect_outliers_via_bornes(
        df: pd.DataFrame,
        cols: list[str],
        bornes: list[list[float]],
        multiple_cols=True
    ) -> pd.DataFrame:

    # Vérifications
    if multiple_cols and len(cols) != len(bornes):
        raise ValueError("Le nombre de colonnes et de bornes doit être identique quand multiple_cols=True.")
    for i, b in enumerate(bornes):
        if not (isinstance(b, (list, tuple)) and len(b) == 2):
            raise ValueError(f"La borne pour la colonne '{cols[i]}' doit être un tuple ou une liste de 2 floats.")
        if not all(isinstance(x, (int, float)) for x in b):
            raise ValueError(f"Les bornes pour la colonne '{cols[i]}' doivent être des nombres.")

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
