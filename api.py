from fastapi import FastAPI
import requests
import base64
from datetime import datetime

app = FastAPI()

# ✅ Zet hier je WooCommerce API-sleutels neer
consumer_key = "ck_a71a6e6549401c7cdc4d5b09ed140873d0fe9557"
consumer_secret = "cs_d22fd4b4ffecf9aa68ec074567bec900a8cb5452"

base_url = "https://www.kuurne-brussel-kuurne.be/wp-json/wc-analytics/reports/products"

@app.get("/")
def root():
    return {"message": "API is running!"}

@app.get("/get-total-sales")
def get_total_sales():
    """Haalt alle verkochte producten op vanaf 1 december 2024 tot vandaag."""

    start_date = "2024-12-01"
    end_date = datetime.today().strftime("%Y-%m-%d")  # Automatische einddatum: vandaag

    url = f"{base_url}?date_min={start_date}&date_max={end_date}"

    # ✅ Zet de credentials correct in de Base64-authenticatie
    credentials = f"{consumer_key}:{consumer_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Controleer of de API-aanroep succesvol was

        products = response.json()

        total_revenue = 0
        total_items_sold = 0

        for product in products:
            total_revenue += product.get("net_revenue", 0)
            total_items_sold += product.get("items_sold", 0)

        return {
            "total_revenue": total_revenue,
            "total_items_sold": total_items_sold
        }

    except requests.exceptions.RequestException as e:
        return {"error": "API call failed", "details": str(e)}

