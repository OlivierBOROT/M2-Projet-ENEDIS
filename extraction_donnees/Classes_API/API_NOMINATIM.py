import time
from typing import Any, List, Dict

import requests

from variables_globales import DEBUG
from Classes_API.API_decorator import retry_request
from Classes_API.API import API


class API_NOMINATIM(API):
    """
    Classe pour interagir avec l'API Nominatim d'OpenStreetMap.

    Permet de récupérer la latitude et la longitude d'une liste d'adresses françaises
    en respectant la limite de requêtes de Nominatim.
    """


    MAX_REQUESTS_PER_MIN = 60
    MIN_INTERVAL = 60 / MAX_REQUESTS_PER_MIN
    URL = "https://nominatim.openstreetmap.org/search"


    def __init__(self, email_adress: str = "olivier.dominique.borot@gmail.com"):
        """
        Initialise l'objet API_NOMINATIM.

        Args:
            email_address (str): Adresse email utilisée pour l'en-tête User-Agent.
        """


        self._last_cycle_time = 0.0
        self.params = {
            "q": "",
            "format": "json"
        }
        self.headers = {
    "User-Agent": f"DPE_project_university ({email_adress})"
        }


    def _debug_log(self, func_name: str, message: str) -> None:
        """
        Affiche un message de debug formaté si DEBUG est actif.

        Args:
            func_name (str): Nom de la fonction appelante.
            message (str): Message à afficher.
        """


        if DEBUG:
            print(f"[DEBUG] {self.__class__.__name__}.{func_name}() → {message}")


    def _respect_rate_limit(self, duration: float) -> None:
        """
        Ajoute un délai pour respecter la limite de requêtes de Nominatim.

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
    def _request(self, url:str = URL, **kwargs) -> requests.Response:
        """
        Effectue une requête HTTP GET sur l'API Nominatim.

        Args:
            url (str): URL de l'API.
            **kwargs: Paramètres supplémentaires pour la requête.

        Returns:
            requests.Response: Réponse HTTP de l'API.
        """


        params = dict(self.params)
        params.update(kwargs)

        response = requests.get(url, params=params, headers=self.headers, timeout=60)
        return response


    def _get_content(self, content: dict[str, Any]) -> dict[str, Any]:
        """
        Extrait la latitude et la longitude d'un résultat Nominatim.

        Args:
            content (dict[str, Any]): Résultat JSON d'une adresse.

        Returns:
            dict[str, Any]: Dictionnaire contenant 'lat' et 'lon'.
        """


        return {
            "lat": content.get("lat", None),
            "lon": content.get("lon", None)
        }


    def _get_length(self, content: dict[str, Any]) -> int:
        """
        Vérifie si un résultat contient des coordonnées valides.

        Args:
            content (dict[str, Any]): Résultat JSON d'une adresse.

        Returns:
            int: 1 si lat/lon sont présents, 0 sinon.
        """


        return 1 if content.get("lat") and content.get("lon") else 0


    def get_data(
        self,
        liste_adresses: list[str],
        url: str = URL,
        print_progress: bool = False,
        **kwargs
    ) -> list[dict[str, Any]]:
        """
        Récupère les coordonnées latitude/longitude pour une liste d'adresses.

        Args:
            liste_adresses (list[str]): Liste d'adresses françaises.
            url (str): URL de l'API Nominatim.
            print_progress (bool): Affiche la progression si True.
            **kwargs: Paramètres supplémentaires pour la requête API.

        Returns:
            list[dict[str, Any]]: Liste des dictionnaires contenant 'adresse', 'lat', 'lon'.
        """


        data: List[Dict[str, Any]] = [] # dictionnaire de l'ensemble des données
        i = 0

        if print_progress:
            total = len(liste_adresses)
            print(f"nombre d'adresses : {total}")

        for i, adresse in enumerate(liste_adresses):
            start_cycle = time.time()

            self.params["q"] = f"{adresse} France"
            response = self._request(url=url, **kwargs)

            if response.status_code != 200:
                self._debug_log("get_data", f"HTTP {response.status_code} pour {adresse}")
                continue

            results = response.json()
            if not results:
                self._debug_log("get_data", f"Aucun résultat pour {adresse}")
                continue
            content = results[0]

            if self._get_length(content):
                temp_data = {
                    "adresse" : adresse,
                    **self._get_content(content)
                }
                print(temp_data)
                data.append(temp_data)

            if print_progress:
                print(f"{i + 1} / {total}")

            cycle_duration = time.time() - start_cycle
            self._respect_rate_limit(cycle_duration)

        self._debug_log("get_data", f"total_records={len(data)}")
        return data
