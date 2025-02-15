from fastapi import FastAPI, Query
import requests
import base64
from datetime import datetime

app = FastAPI()

# ✅ WooCommerce API-sleutels (vervang door jouw sleutels)
consumer_key = "ck_a71a6e6549401c7cdc4d5b09ed140873d0fe9557"
consumer_secret = "cs_d22fd4b4ffecf9aa68ec074567bec900a8cb5452"

# ✅ WooCommerce API-endpoint
base_url = "https://www.kuurne-brussel-kuurne.be/wp-json/wc-analytics/reports/products"

@app.get("/")
def root():
    return {"message": "API is running!"}

@app.get("/get-total-sales")
def get_total_sales():
    """Haalt het totale aantal verkochte producten op vanaf 1 december 2024 tot vandaag."""

    start_date = "2024-12-01"
    end_date = datetime.today().strftime("%Y-%m-%d")  # Automatische einddatum: vandaag

    total_items_sold = 0
    page = 1  

    credentials = f"{consumer_key}:{consumer_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Content-Type": "application/json"
    }

    while True:
        url = f"{base_url}?after={start_date}T00:00:00&before={end_date}T23:59:59&page={page}&per_page=100"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            products = response.json()
            
            if not products:
                break  # Stop als er geen producten meer zijn

            for product in products:
                total_items_sold += product.get("items_sold", 0)

            page += 1  

        else:
            return {"error": response.status_code, "message": response.text}

    return {
        "total_items_sold": total_items_sold
    }

@app.get("/get-sales")
def get_sales(
    start_date: str = Query(..., description="Startdatum in formaat YYYY-MM-DD"),
    end_date: str = Query(..., description="Einddatum in formaat YYYY-MM-DD")
):
    """Haalt verkochte producten op binnen een bepaalde datumrange."""

    credentials = f"{consumer_key}:{consumer_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Content-Type": "application/json"
    }

    url = f"{base_url}?after={start_date}T00:00:00&before={end_date}T23:59:59"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()

    return {"error": response.status_code, "message": response.text}
