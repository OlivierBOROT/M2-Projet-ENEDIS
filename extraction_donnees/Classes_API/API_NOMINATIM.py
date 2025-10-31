import time
from typing import Any

import requests

from variables_globales import DEBUG
from Classes_API.API_decorator import retry_request
from Classes_API.API import API


class API_NOMINATIM(API):
    MAX_REQUESTS_PER_MIN = 60
    MIN_INTERVAL = 60 / MAX_REQUESTS_PER_MIN
    URL = "https://nominatim.openstreetmap.org/search"

    def __init__(self, email_adress: str = "olivier.dominique.borot@gmail.com"):
        self._last_cycle_time = 0.0
        self.params = {
            "q": "",
            "format": "json"
        }
        self.headers = {
    "User-Agent": f"DPE_project_university ({email_adress})"
        }

    def _debug_log(self, func_name: str, message: str) -> None:
        """Affiche un message de debug formaté si DEBUG est actif."""
        if DEBUG:
            print(f"[DEBUG] {self.__class__.__name__}.{func_name}() → {message}")

    def _respect_rate_limit(self, duration: float) -> None:
        """
        Ajoute un délai pour respecter la limite NOMINATIM.
        On compte le temps total de la requête (durée) dans le calcul.
        """
        elapsed_since_last = time.time() - self._last_cycle_time
        remaining = self.MIN_INTERVAL - elapsed_since_last - duration

        if remaining > 0:
            if DEBUG:
                print(f"[DEBUG] Sleeping {remaining:.3f}s to respect ADEME rate limit...")
            time.sleep(remaining)

        self._last_cycle_time = time.time()

    @retry_request(max_retries=3, delay=1, backoff=2)
    def _request(self, url:str = URL, **kwargs) -> requests.Response:
        params = dict(self.params)
        params.update(kwargs)

        response = requests.get(url, params=params, headers=self.headers, timeout=60)
        return response

    def _get_content(self, content: dict[str, Any]) -> dict[str, Any]:
        return {
            "lat": content.get("lat", None),
            "lon": content.get("lon", None)
        }

    def _get_length(self, content: dict[str, Any]) -> int:
        if content.get("lat") and content.get("lon"):
            return len(content)
        return 0

    def get_data(
        self,
        liste_adresses: list[str],
        url: str = URL,
        print_progress: bool = False,
        **kwargs
    ) -> list[dict[str, Any]]:

        data = [] # dictionnaire de l'ensemble des données
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
