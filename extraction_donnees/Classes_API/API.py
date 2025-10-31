from abc import ABC, abstractmethod
from typing import Any
import requests

class API(ABC):
    @abstractmethod
    def _request(self, url, **kwargs) -> requests.Response:
        pass

    @abstractmethod
    def _get_length(self, content) -> int | None:
        pass

    @abstractmethod
    def _get_content(self, content) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_data(self):
        pass
