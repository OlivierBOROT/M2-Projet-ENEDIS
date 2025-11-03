import time
from typing import Any
import requests

from variables_globales import DEBUG
from Classes_API.API_decorator import retry_request
from Classes_API.API import API


class API_ADEME(API):
    """
    Classe pour interagir avec l'API DPE d'ADEME (Diagnostic de Performance Énergétique).

    Gère la limitation du nombre de requêtes, la pagination, et la récupération des données
    pour les bâtiments existants ou neufs selon les régions spécifiées.

    Hérite de la classe abstraite API
    """


    MAX_REQUESTS_PER_MIN = 600
    MIN_INTERVAL = 60 / MAX_REQUESTS_PER_MIN
    url_existant = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/lines"
    url_neuf = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe02neuf/lines"


    def __init__(self, region: int | list[int] = 84):
        """
        Initialisation de l'objet API_ADEME.

        Args:
            region (int | list[int]): Code(s) de région(s) pour filtrer les données.
        """


        self.region = region
        self._last_cycle_time = 0.0

        self.params = {
            "select": "",
            "size": 100,
            "qs": ""
        }


    def _debug_log(self, func_name: str, message: str) -> None:
        """
        Affiche un message de debug formaté si DEBUG est actif.

        Args:
            func_name (str): Nom de la fonction où le debug est appelé.
            message (str): Message à afficher.
        """


        if DEBUG:
            print(f"[DEBUG] {self.__class__.__name__}.{func_name}() → {message}")


    def _respect_rate_limit(self, duration: float) -> None:
        """
        Ajoute un délai pour respecter la limite de requêtes de l'API ADEME.

        Args:
            duration (float): Durée de la dernière requête.
        """


        elapsed_since_last = time.time() - self._last_cycle_time
        remaining = self.MIN_INTERVAL - elapsed_since_last - duration

        if remaining > 0:
            if DEBUG:
                print(f"[DEBUG] Sleeping {remaining:.3f}s to respect ADEME rate limit...")
            time.sleep(remaining)

        self._last_cycle_time = time.time()


    # retry_request à retrouver dans le fichier API_decorator
    @retry_request(max_retries=3, delay=1, backoff=2)
    def _request(self, url: str, next_url: bool = False, **kwargs) -> requests.Response:
        """
        Effectue une requête HTTP GET sur l'API ADEME.

        Args:
            url (str): URL de la requête.
            next_url (bool): Indique si l'URL contient déjà les paramètres pour la pagination.
            **kwargs: Paramètres supplémentaires pour la requête.

        Returns:
            requests.Response: Réponse HTTP de l'API.
        """


        params = None
        if not next_url: # si on n'a pas déjà les paramètres dans l'url
            params = dict(self.params)
            params.update(kwargs)

            if "select" in params and isinstance(params["select"], (list, tuple)):
                params["select"] = ",".join(params["select"])

            if isinstance(self.region, int):
                region_filter = f"code_region_ban:{self.region}"
            elif isinstance(self.region, list):
                # Elasticsearch OR pour plusieurs régions
                region_filter = " OR ".join(f"code_region_ban:{r}" for r in self.region)
                region_filter = f"({region_filter})"
            else:
                raise TypeError("region must be int or list[int]")

            qs = params["qs"]
            if region_filter not in qs:
                if qs.strip():
                    params["qs"] = f"{qs} AND {region_filter}"
                else:
                    params["qs"] = region_filter
        # requête :
        response = requests.get(url, params=params, timeout=60) # 60 secondes
        self._debug_log("_request", f"params={params} | status={response.status_code}")

        response.raise_for_status()
        return response


    def _get_content(self, content: dict[str, Any]) -> dict[str, Any]:
        """
        Extrait le contenu d'une réponse au format JSON.

        Args:
            content (dict[str, Any]): Contenu JSON de la réponse API.

        Returns:
            list[dict[str, Any]]: Liste des enregistrements.
        """


        df = content.get("results", [])
        self._debug_log(
            "_get_content",
            f"total={content.get("total", "N/A")}"
            f" | dims={(len(df), len(df[0]) if df else 0)}"
            )

        return df


    def _get_next(self, content: dict[str, Any]) -> str | None:
        """
        Récupère le lien vers la page suivante (pagination).

        Args:
            content (dict[str, Any]): Contenu JSON de la réponse API.

        Returns:
            str | None: URL suivante ou None si fin de pagination.
        """


        next_link = content.get("next", False)
        self._debug_log("_get_next", f"next_link={next_link}")
        return next_link if next_link else None


    def _get_length(self, content: dict[str, Any]) -> int:
        """
        Retourne le nombre de lignes dans 'results'.

        Args:
            content (dict[str, Any]): Contenu JSON de la réponse API.

        Returns:
            int: Nombre de lignes.
        """


        length = len(content.get("results", []))
        self._debug_log("_get_length", f"length={length}")
        return length


    def _get_total(self, content: dict[str, Any]) -> int:
        """
        Retourne le nombre total de lignes disponibles sur l'API pour la requête donnée.

        Args:
            content (dict[str, Any]): Contenu JSON de la réponse API.

        Returns:
            int: Nombre total de lignes.
        """


        total = content.get("total", 0)
        self._debug_log("_get_total", f"total={total}")
        return total


    def get_data(
        self,
        neuf: bool = False,
        nrows: int | bool = False,
        print_progress: bool = False,
        **kwargs
    ) -> dict[str, Any]:
        """
        Récupère les données de l'ADEME selon les paramètres.

        Args:
            neuf (bool): True pour les bâtiments neufs, False pour existants.
            nrows (int | bool): Nombre maximum de lignes à récupérer, False pour tout.
            print_progress (bool): Affiche la progression si True.
            **kwargs: Paramètres supplémentaires pour la requête API.

        Returns:
            list[dict[str, Any]]: Liste des enregistrements.
        """


        url =  self.url_neuf if neuf else self.url_existant

        response = self._request(url, **kwargs)
        content = response.json()

        data = self._get_content(content)
        next_link = self._get_next(content)


        if print_progress or nrows:
            i = 0
            if print_progress:
                total = self._get_total(content)
                print(f"total à atteindre : {total}")

        while next_link:
            start_cycle = time.time()

            response = self._request(url = next_link, next_url = True)
            content = response.json()

            batch = self._get_content(content)
            if batch:
                data += batch

                if print_progress or nrows:
                    i += self._get_length(content)

                    if print_progress:
                        print(f"{i} / {total}")

                    if nrows and i >= nrows:
                        return data[:nrows]

            next_link = self._get_next(content)

            cycle_duration = time.time() - start_cycle
            self._respect_rate_limit(cycle_duration)


        self._debug_log("get_data", f"total_records={len(data)}")
        return data
