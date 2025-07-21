# transform_fakestore.py

import pandas as pd
from utils.cleaning import standardize_column_names, deduplicate

def transform(data):
    users = pd.DataFrame(data["users"])
    products = pd.DataFrame(data["products"])
    carts = pd.DataFrame(data["carts"])

    users = standardize_column_names(users)
    products = standardize_column_names(products)
    carts = standardize_column_names(carts)

    users = deduplicate(users, subset=["email"])
    products = deduplicate(products, subset=["title"])
    carts = deduplicate(carts, subset=["id"])
    
    users = users.drop(columns=["__v"], errors="ignore")
    products = products.drop(columns=["rating"], errors="ignore")
    carts = carts.rename(columns={"userid": "user_id"})
    carts = carts.drop(columns=["__v"], errors="ignore")
    
    return users, products, carts
