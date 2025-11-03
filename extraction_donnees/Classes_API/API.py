from abc import ABC, abstractmethod
from typing import Any
import requests

class API(ABC):
    """
    Classe abstraite de base pour toutes les classes d'API.

    Définit les méthodes minimales qu'une API doit implémenter :
    - _request : effectuer une requête HTTP.
    - _get_length : obtenir le nombre d'enregistrements d'une réponse.
    - _get_content : extraire les données utiles d'une réponse.
    - get_data : récupérer les données depuis l'API.
    """


    @abstractmethod
    def _request(self, url, **kwargs) -> requests.Response:
        """
        Effectue une requête HTTP GET vers l'API.

        Args:
            url (str): URL de la requête.
            **kwargs: Paramètres supplémentaires pour la requête.

        Returns:
            requests.Response: Réponse HTTP de l'API.
        """
        pass


    @abstractmethod
    def _get_length(self, content) -> int | None:
        """
        Retourne le nombre d'enregistrements dans le contenu d'une réponse.

        Args:
            content (Any): Contenu JSON ou équivalent de la réponse API.

        Returns:
            int | None: Nombre d'enregistrements, ou None si non applicable.
        """
        pass


    @abstractmethod
    def _get_content(self, content) -> dict[str, Any]:
        """
        Extrait et retourne les données utiles d'une réponse API.

        Args:
            content (Any): Contenu JSON ou équivalent de la réponse API.

        Returns:
            dict[str, Any]: Données extraites de la réponse.
        """
        pass

    @abstractmethod
    def get_data(self):
        """
        Méthode principale pour récupérer les données depuis l'API.

        Args:
            *args: Arguments positionnels spécifiques à l'API.
            **kwargs: Arguments nommés spécifiques à l'API.

        Returns:
            Any: Données récupérées depuis l'API (format dépend de l'implémentation).
        """
        pass
