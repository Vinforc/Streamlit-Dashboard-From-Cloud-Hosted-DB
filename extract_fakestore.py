# extract_fakestore.py

import requests

def fetch_fakestore_data():
    base_url = "https://fakestoreapi.com"
    endpoints = ["users", "products", "carts"]
    data = {}

    for endpoint in endpoints:
        res = requests.get(f"{base_url}/{endpoint}")
        res.raise_for_status()
        data[endpoint] = res.json()

    return data
