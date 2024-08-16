import requests

BASE_URL = "https://api.scryfall.com"

def get_card_data(card_name: str) -> dict:
    response = requests.get(f"{BASE_URL}/cards/named", params={"fuzzy": card_name})
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()