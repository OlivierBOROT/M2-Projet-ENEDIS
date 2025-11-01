import math
from typing import Callable, Optional, Tuple, Dict
import pandas as pd
import numpy as np

# Attention ! package non compris dans le requirements.txt car lourd et pas utilisé !
from sentence_transformers import SentenceTransformer

# scikit-learn
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import silhouette_score

from stop_words import DEBUG, STOP_WORDS_FR


def regrouper_termes_via_semantique(
    colonne: pd.Series,
    cleaner: Optional[Callable[[str], str]] = None,
    n_clusters: Optional[int] = None,
    method: str = "silhouette",
    min_k: int = 3,
    max_k: int = 30,
    batch_size: int = 10000,
    top_words: int = 3
) -> Tuple[pd.DataFrame, Dict[int, str], int]:
    """
    Regroupe des textes en clusters sémantiques et génère une classe_lisible synthétique.

    Étapes :
    1. Nettoyage des textes.
    2. Encodage des textes en embeddings via SentenceTransformer.
    3. Détermination du nombre optimal de clusters (optionnel) via différentes méthodes.
    4. Clustering avec MiniBatchKMeans.
    5. Extraction des mots-clés TF-IDF par cluster.
    6. Construction d'une classe_lisible synthétique par cluster.

    Parameters
    ----------
    colonne : pd.Series
        Série contenant les textes à regrouper.
    cleaner : Callable[[str], str] | None, optional
        Fonction de nettoyage à appliquer aux textes. Si None, aucun nettoyage.
    n_clusters : int | None, optional
        Nombre de clusters à créer. Si None, il sera déterminé automatiquement.
    method : str, default "silhouette"
        Méthode pour déterminer automatiquement n_clusters si n_clusters=None.
        Choix : 'silhouette', 'brooks-carruthers', 'sturges-huntsberger', 'scott', 'freedman-diaconis'.
    min_k : int, default 3
        Nombre minimal de clusters pour la méthode silhouette.
    max_k : int, default 30
        Nombre maximal de clusters pour la méthode silhouette.
    batch_size : int, default 10000
        Taille des batches pour l'encodage des embeddings.
    top_words : int, default 3
        Nombre de mots-clés les plus fréquents à utiliser pour construire la classe_lisible.

    Returns
    -------
    Tuple[pd.DataFrame, Dict[int, str], int]
        - DataFrame contenant les colonnes : texte, cluster, mots_cles, classe_lisible.
        - Dictionnaire {cluster_id: mots_cles TF-IDF principales}.
        - Nombre de clusters utilisés.
    """


    # --- Nettoyage des textes ---
    if cleaner:
        textes = colonne.apply(cleaner).dropna().reset_index(drop=True)
    else:
        textes = colonne.dropna().reset_index(drop=True)

    # --- Embeddings ---
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embeddings_list = []
    for i in range(0, len(textes), batch_size):
        batch = textes[i:i+batch_size].tolist()
        emb = model.encode(batch, show_progress_bar=False)
        embeddings_list.append(emb)
    embeddings = np.vstack(embeddings_list)

    # --- Choix du nombre de clusters ---
    if n_clusters is None:
        N = len(textes)
        longueurs = textes.str.len()
        xmax, xmin = longueurs.max(), longueurs.min()
        sigma = longueurs.std()
        IQR = np.percentile(longueurs, 75) - np.percentile(longueurs, 25)

        if method == "silhouette":
            sample_idx = np.random.choice(N, size=min(20000, N), replace=False)
            best_k, best_score = min_k, -1
            for k in range(min_k, max_k + 1):
                kmeans_temp = MiniBatchKMeans(n_clusters=k, random_state=42, batch_size=1000)
                labels_temp = kmeans_temp.fit_predict(embeddings[sample_idx])
                score = silhouette_score(embeddings[sample_idx], labels_temp)
                if score > best_score:
                    best_score, best_k = score, k
            n_clusters = best_k

        elif method == "brooks-carruthers":
            n_clusters = max(1, round(5 * math.log(N)))

        elif method == "sturges-huntsberger":
            n_clusters = max(1, round(1 + (10/3) * math.log(N)))

        elif method == "scott":
            n_clusters = max(1, round((xmax - xmin) / (3.5 * sigma * N**(-1/3))))

        elif method == "freedman-diaconis":
            n_clusters = max(1, round((xmax - xmin) / (2 * IQR * N**(-1/3))))

        else:
            raise ValueError("method doit être 'silhouette', 'brooks-carruthers', 'sturges-huntsberger', 'scott' ou 'freedman-diaconis'")

        # affichage
        if DEBUG:
            if method == "silhouette":
                print(f"Nombre optimal de clusters selon silhouette : {n_clusters} (score={best_score:.3f})")
            else:
                print(f"Nombre de clusters selon {method} : {n_clusters}")

    # --- Clustering complet ---
    kmeans = MiniBatchKMeans(n_clusters=n_clusters, random_state=42, batch_size=1000)
    labels = kmeans.fit_predict(embeddings)
    df = pd.DataFrame({"texte": textes, "cluster": labels})

    # --- TF-IDF pour mots clés ---
    vect = CountVectorizer(stop_words=STOP_WORDS_FR, ngram_range=(1, 2), max_features=30000)
    X_counts = vect.fit_transform(df["texte"])
    tfidf = TfidfTransformer().fit_transform(X_counts)
    features = np.array(vect.get_feature_names_out())

    mots_clusters = {}
    classe_lisible_dict = {}

    for cluster_id in range(n_clusters):
        idx = np.where(df["cluster"] == cluster_id)[0]
        if len(idx) == 0:
            continue

        cluster_tfidf = np.asarray(tfidf[idx].mean(axis=0)).ravel()
        top_indices = cluster_tfidf.argsort()[-30:][::-1]  # Pool de termes du cluster
        top_terms = features[top_indices]

        # Découper les bigrams et compter les mots
        word_count = {}
        for term in top_terms:
            for w in term.split():
                if w not in STOP_WORDS_FR:
                    word_count[w] = word_count.get(w, 0) + 1

        # Sélectionner les mots les plus fréquents
        top_words_sorted = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        selected_words = [w for w, _ in top_words_sorted[:top_words]]

        # Construire la classe lisible synthétique
        classe_lisible_dict[cluster_id] = " ".join(selected_words)
        mots_clusters[cluster_id] = ", ".join(top_terms[:3])  # référence TF-IDF

    df["mots_cles"] = df["cluster"].map(mots_clusters)
    df["classe_lisible"] = df["cluster"].map(classe_lisible_dict)

    return df, mots_clusters, n_clusters
