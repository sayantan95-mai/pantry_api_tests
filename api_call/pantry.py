import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configuration
PANTRY_ID = "53748d1f-f12a-44f0-bc4b-7cc65a5fa7b9"
BASE_URL = f"https://getpantry.cloud/apiv1/pantry/{PANTRY_ID}"


def get_session():
    """
    Create this function because getting 429 error.
    Creates a requests Session that automatically retries on:
    - 429 (Too Many Requests)
    - 500, 502, 503, 504 (Server Errors)
    It waits 1s, 2s, 4s... automatically (Exponential Backoff).
    """
    session = requests.Session()

    # Define retry strategy
    retry_strategy = Retry(
        total=4,  # Maximum number of retries
        backoff_factor=1,  # Wait 1s, 2s, 4s, 8s...
        status_forcelist=[429, 500, 502, 503, 504],  # Retry on these errors
        allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "POST"]  # Retry on these methods
    )

    # Mount it to https://
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.headers.update({'Content-Type': 'application/json'})

    return session


# Create a global session instance to reuse
s = get_session()


# --- Public Functions (Clean & Simple) ---

def get_pantry_details():
    return s.get(BASE_URL)


def put_update_details(payload):
    return s.put(BASE_URL, data=payload)


def post_create_update(basket_name, payload):
    return s.post(f"{BASE_URL}/basket/{basket_name}", data=payload)


def get_content(basket_name):
    return s.get(f"{BASE_URL}/basket/{basket_name}")


def put_update_contents(basket_name, payload):
    return s.put(f"{BASE_URL}/basket/{basket_name}", data=payload)


def delete_basket(basket_name):
    return s.delete(f"{BASE_URL}/basket/{basket_name}")