import time
from typing import Any
import requests
import pandas as pd

from variables_globales import DEBUG

from Classes_API.API import API
from Classes_API.API_decorator import retry_request

class API_TEMPERATURE(API):
    MAX_REQUESTS_PER_MIN = 60
    MIN_INTERVAL = 60 / MAX_REQUESTS_PER_MIN 
    URL = "https://tabular-api.data.gouv.fr/api/resources/"
    dic_dep_link = {
        "01": "f292971a-dd3c-4d76-9e52-c265e2f909a5",
        "03": "ebf1e37d-e88d-47eb-a5e9-2c5ff72ebd4d",
        "07": "638d69f1-a3fe-4e28-9787-c34dcb57e47c",
        "15": "332ca3c3-5e90-4c63-898e-a2976f39b923",
        "26": "470e2374-bee2-4613-83f6-94fe231213d2",
        "38": "15f5ffb2-527d-4315-9115-521c258f77d4",
        "42": "ee71a680-ec36-4a37-bf0f-ff18917ee42d",
        "43": "b1a7f768-a446-4c01-a462-34519de7567d",
        "63": "6f379930-c3c7-42ab-97c4-d052a8f655a2",
        "69": "d1b64ed7-d1c2-4bd3-8a29-c2d5501c8f94",
        "73": "eed1b6ab-bf91-4b3b-b2b1-dad212e6dc9a",
        "74": "054f9d2a-ae36-40ed-9359-f5cc8d3e38fc"
    }

    def __init__(self):
        self._last_cycle_time = 0.0
        self.params = {
            "columns": "",
            "page_size": 200
        }

    def _debug_log(self, func_name: str, message: str) -> None:
        """Affiche un message de debug formaté si DEBUG est actif."""
        if DEBUG:
            print(f"[DEBUG] {self.__class__.__name__}.{func_name}() → {message}")

    def _respect_rate_limit(self, duration: float) -> None:
        """
        Ajoute un délai pour respecter la limite ADEME.
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
    def _request(self, url: str, next_url: bool = False, **kwargs) -> requests.Response:
        params = None
        if not next_url: # si on n'a pas déjà les paramètres dans l'url
            params = dict(self.params)
            params.update(kwargs)

            if "columns" in params and isinstance(params["columns"], (list, tuple)):
                params["columns"] = ",".join(params["columns"])

        response = requests.get(url, params=params, timeout=60)
        # url = url
        # params = dict(params) | None
        self._debug_log("_request", f"params={params} | status={response.status_code}")
        response.raise_for_status()
        return response

    def _get_content(self, content: dict[str, Any]) -> dict[str, Any]:
        df = content.get("data", [])
        self._debug_log(
            "_get_content",
            f"total={content.get("total", "N/A")}"
            f" | dims={(len(df), len(df[0]) if df else 0)}"
            )

        return df

    def _get_next(self, content: dict[str, Any]) -> str | None:
        next_link = content.get("links", {}).get("next", None)
        self._debug_log("_get_next", f"next_link={next_link}")
        return next_link if next_link else None

    def _get_length(self, content: dict[str, Any]) -> int:
        """Retourne le nombre de lignes dans 'results'."""
        length = len(content.get("data", []))
        self._debug_log("_get_length", f"length={length}")
        return length

    def _get_total(self, content: dict[str, Any]) -> int:
        """Retourne le nombre total de lignes (content['total'])."""
        total = content.get("meta", {}).get("total", None)
        self._debug_log("_get_total", f"total={total}")
        return total

    def get_data(
            self,
            nrows: int | bool = False,
            print_progress: bool = False,
            **kwargs
        ) -> pd.DataFrame:

        data = pd.DataFrame() # dataframe de l'ensemble des données
        i = int # nombre de lignes extraites par département
        total = int # nombre total de lignes par département

        for dep_id, dep_url in self.dic_dep_link.items():
            temp_url = f"{self.URL}{dep_url}/data/"
            response = self._request(temp_url, **kwargs)
            content = response.json()

            temp_data = pd.DataFrame(self._get_content(content))
            next_link = self._get_next(content)


            if print_progress or nrows:
                i = 0
                if print_progress:
                    total = self._get_total(content)
                    print(f"Pour le département :{dep_id}, total à atteindre : {total}")

            while next_link:
                start_cycle = time.time()

                response = self._request(url = next_link, next_url = True)
                content = response.json()

                if self._get_length(content):
                    temp_chunk = pd.DataFrame(self._get_content(content))
                    temp_data = pd.concat([temp_data, temp_chunk], ignore_index=True)

                    if print_progress or nrows:
                        i += self._get_length(content)

                        if print_progress:
                            print(f"dep:{dep_id} : {i} / {total}")

                        if nrows and i >= nrows:
                            break
                next_link = self._get_next(content)

                cycle_duration = time.time() - start_cycle
                self._respect_rate_limit(cycle_duration)

            temp_data["dep_id"] = dep_id
            data = pd.concat([data, temp_data], ignore_index=True)

        self._debug_log("get_data",
                        f"total_records={len(data)} pour n_departements={len(self.dic_dep_link)}")
        return data
