import pandas as pd
import numpy as np
import re
import unicodedata
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
from nltk.corpus import stopwords
import nltk

nltk.download("stopwords", quiet=True)
stop_words_fr = set(stopwords.words("french"))

# ===================================================
# Nettoyage du texte
# ===================================================
def nettoyer_label(label: str) -> str:
    label = str(label).lower()
    label = unicodedata.normalize("NFKC", label)
    label = re.sub(r"\d+", " ", label)
    label = re.sub(r"[^a-zàâçéèêëîïôûùüÿñæœ\s]", " ", label)
    label = re.sub(r"\s+", " ", label).strip()
    tokens = [t for t in label.split() if t not in stop_words_fr]
    return " ".join(tokens)

# ===================================================
# Fonction principale
# ===================================================
def proposer_classes_generales(value_counts: pd.Series, n_clusters=None, verbose=True):
    """
    Regroupe automatiquement les classes détaillées en grandes familles sémantiques.
    
    Args:
        value_counts : pd.Series (index = classes détaillées, values = effectifs)
        n_clusters : int ou None (auto)
        verbose : bool - affiche des logs
    
    Returns:
        DataFrame avec :
          - classe_originale
          - effectif
          - cluster_id
          - classe_large_proposee
    """
    labels = list(value_counts.index)
    counts = list(value_counts.values)

    if verbose:
        print(f"➡️ Analyse de {len(labels)} classes techniques...")

    # Nettoyage
    labels_clean = [nettoyer_label(x) for x in labels]

    # Embeddings
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embeddings = model.encode(labels_clean, show_progress_bar=False)

    # Nombre de clusters auto
    if n_clusters is None:
        n_clusters = max(5, min(25, len(labels) // 8))
        if verbose:
            print(f"🔢 Nombre de clusters déterminé automatiquement : {n_clusters}")

    # Clustering sémantique
    cluster = AgglomerativeClustering(
        n_clusters=n_clusters, metric="cosine", linkage="average"
    )
    cluster_ids = cluster.fit_predict(embeddings)

    df = pd.DataFrame({
        "classe_originale": labels,
        "effectif": counts,
        "cluster_id": cluster_ids,
    })

    # Génération des noms de familles
    familles = {}
    for cid in sorted(df["cluster_id"].unique()):
        sous_classes = df[df["cluster_id"] == cid]["classe_originale"].tolist()
        mots = [w for s in sous_classes for w in nettoyer_label(s).split()]
        if not mots:
            familles[cid] = f"famille_{cid}"
            continue
        top = pd.Series(mots).value_counts().index[:2].tolist()
        familles[cid] = " ".join(top)

    df["classe_large_proposee"] = df["cluster_id"].map(familles)

    if verbose:
        print("✅ Regroupement terminé.")
        print(f"Nombre de classes larges proposées : {len(familles)}")

    return df.sort_values("cluster_id").reset_index(drop=True)
