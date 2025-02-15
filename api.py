from fastapi import FastAPI, Query
import requests
from requests.auth import HTTPBasicAuth

app = FastAPI()

# WooCommerce API-sleutels
consumer_key = "ck_a71a6e6549401c7cdc4d5b09ed140873d0fe9557"
consumer_secret = "cs_d22fd4b4ffecf9aa68ec074567bec900a8cb5452"
base_url = "https://www.kuurne-brussel-kuurne.be/wp-json/wc/v3/reports"

@app.get("/")
def root():
    return {"message": "API is running!"}

@app.get("/get-sales")
def get_sales_data(
    start_date: str = Query(..., description="Startdatum in YYYY-MM-DD formaat"),
    end_date: str = Query(..., description="Einddatum in YYYY-MM-DD formaat")
):
    """Haalt de verkoopsgegevens op tussen een start- en einddatum."""

    # WooCommerce API endpoint - Opvragen van ALLE dagen in de opgegeven periode
    url = f"{base_url}/sales?after={start_date}&before={end_date}&orderby=date&order=asc"

    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    if response.status_code == 200:
        data = response.json()

        # Controleer of WooCommerce de data per dag groepeert
        if isinstance(data, list) and "totals" in data[0]:
            sales_by_day = data[0]["totals"]  # Alle dagen uit de data halen
            return {"sales_data": sales_by_day}  # Stuur de totale sales per dag terug

    return {"error": response.status_code, "message": response.text}
