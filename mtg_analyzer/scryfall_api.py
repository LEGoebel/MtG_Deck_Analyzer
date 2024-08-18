import requests
import json
import os

BASE_URL = "https://api.scryfall.com"
BASE_CACHE_FILEPATH = "data/card_cache.json"

def get_card_data(card_name: str) -> dict:
    #lade cache
    cache = load_cache()
    
    #prüfe, ob Daten im Cache vorhanden
    if card_name in cache:
        return cache[card_name]
    
    #falls nicht vorhanden rufe Daten ab und sichere sie im Cache
    response = requests.get(f"{BASE_URL}/cards/named", params={"fuzzy": card_name})
    if response.status_code == 200:
        card_data = response.json()
        
        #Daten im Cache speichern
        cache[card_name] = card_data
        save_cache(cache)
        return card_data
    else:
        response.raise_for_status()
        
def search_cards(query: str) -> list:
    response = requests.get(f"{BASE_URL}/cards/search", params={"q": query})
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        response.raise_for_status()
        
def save_cache(cache):
    with open(BASE_CACHE_FILEPATH, 'w') as f:
        json.dump(cache, f, indent = 4)
        
def load_cache():
    if os.path.exists(BASE_CACHE_FILEPATH):
        with open(BASE_CACHE_FILEPATH, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}  # Falls die Datei beschädigt ist oder kein gültiges JSON enthält
    else:
        # Erstellt den Cache-Ordner, falls er nicht existiert
        os.makedirs(os.path.dirname(BASE_CACHE_FILEPATH), exist_ok=True)
        return {}