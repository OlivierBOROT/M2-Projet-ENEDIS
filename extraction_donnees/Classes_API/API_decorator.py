import time
import functools
import requests

def retry_request(max_retries=3, delay=1, backoff=2, exceptions=(requests.RequestException,)):
    """
    Décorateur pour répéter une requête HTTP en cas d'échec.

    Args:
        max_retries (int): Nombre maximum de tentatives.
        delay (float): Délai initial entre les tentatives (en secondes).
        backoff (float): Facteur multiplicatif du délai entre chaque tentative.
        exceptions (tuple): Exceptions qui déclenchent un retry.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        print(f"Échec après {attempt} tentatives : {e}")
                        raise
                    else:
                        print(f"Tentative {attempt} échouée ({e}).\n"
                              f"Nouvelle tentative dans {current_delay}s...")
                        time.sleep(current_delay)
                        current_delay *= backoff
        return wrapper
    return decorator
