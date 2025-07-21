# etl_pipeline.py

from extract.extract_fakestore import fetch_fakestore_data
from transform.transform_fakestore import transform
from load.load_to_postgres import load_to_postgres


def run_etl():
    data = fetch_fakestore_data()
    users, products, carts = transform(data)
    load_to_postgres(users, "users")
    load_to_postgres(products, "products")
    load_to_postgres(carts, "carts")

if __name__ == "__main__":
    run_etl()
