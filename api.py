from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running!"}

from fastapi import FastAPI
import requests
from requests.auth import HTTPBasicAuth

# Maak een FastAPI-app
app = FastAPI()

# WooCommerce API-sleutels (vervang deze met jouw echte sleutels)
consumer_key = "ck_a71a6e6549401c7cdc4d5b09ed140873d0fe9557"
consumer_secret = "cs_d22fd4b4ffecf9aa68ec074567bec900a8cb5452"

# WooCommerce API-base URL
base_url = "https://www.kuurne-brussel-kuurne.be/wp-json/wc/v3/reports"

@app.get("/get-sales")
def get_sales_data(start_date: str, end_date: str):
    """Haalt de verkoopsgegevens op tussen een start- en einddatum."""
    
    # API-endpoint met de juiste parameters
    url = f"{base_url}/sales?after={start_date}&before={end_date}"
    
    # API-aanroep met authenticatie
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    
    if response.status_code == 200:
        return response.json()  # JSON-response teruggeven
    else:
        return {"error": response.status_code, "message": response.text}

# Start de server met: uvicorn api:app --reload
