import streamlit as st
import pandas as pd
import psycopg2
import json
import altair as alt
from datetime import datetime
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()  # Load .env file

# --- DB CONFIG ---
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)

# --- LOAD & FLATTEN DATA ---
@st.cache_data
def load_data():
    query = """
    SELECT
        u.id AS user_id,
        u.name,
        u.address,
        c.id AS cart_id,
        c.date,
        c.products::jsonb AS cart_products
    FROM users u
    JOIN carts c ON c.user_id = u.id
    """
    df = pd.read_sql(query, conn)

#should be done in ETL
    df["firstname"] = df["name"].apply(lambda x: x["firstname"] if isinstance(x, dict) else json.loads(x)["firstname"])
    df["lastname"] = df["name"].apply(lambda x: x["lastname"] if isinstance(x, dict) else json.loads(x)["lastname"])
    df["full_name"] = df["firstname"] + " " + df["lastname"]
    df["city"] = df["address"].apply(lambda x: x["city"] if isinstance(x, dict) else json.loads(x)["city"])
    df["zipcode"] = df["address"].apply(lambda x: x["zipcode"] if isinstance(x, dict) else json.loads(x)["zipcode"])
    df["date"] = pd.to_datetime(df["date"])

    expanded_rows = []
    for _, row in df.iterrows():
        products = row["cart_products"]
        if isinstance(products, str):
            products = json.loads(products)
        for item in products:
            expanded_rows.append({
                "user_id": row["user_id"],
                "full_name": row["full_name"],
                "firstname": row["firstname"],
                "lastname": row["lastname"],
                "city": row["city"],
                "zipcode": row["zipcode"],
                "cart_id": row["cart_id"],
                "date": row["date"],
                "product_id": item["productId"],
                "quantity": item["quantity"]
            })

    return pd.DataFrame(expanded_rows)

@st.cache_data
def load_products():
    return pd.read_sql("SELECT id, title, price FROM products", conn)

# --- LOAD DATA ---
df_items = load_data()
products = load_products()
df = df_items.merge(products, left_on="product_id", right_on="id", how="left")
df["revenue"] = df["quantity"] * df["price"]

# --- SIDEBAR FILTERING ---
st.sidebar.title("Filters")

preset_options = {
    "All Data": {},
    "Top Buyer": {"full_name": df.groupby("full_name")["revenue"].sum().idxmax()},
    "Last 30 Days": {"date_from": datetime.now().date() - pd.Timedelta(days=30)},
    "Last 7 Days": {"date_from": datetime.now().date() - pd.Timedelta(days=7)}
}

preset = st.sidebar.selectbox("Select a filter preset", list(preset_options.keys()))
user_filter = st.sidebar.multiselect("Filter by Name", df["full_name"].unique())
date_range = st.sidebar.date_input("Date Range", [])

preset_config = preset_options[preset]
if "full_name" in preset_config:
    df = df[df["full_name"] == preset_config["full_name"]]
if "date_from" in preset_config:
    df = df[df["date"] >= pd.to_datetime(preset_config["date_from"])]
if user_filter:
    df = df[df["full_name"].isin(user_filter)]
if len(date_range) == 2:
    df = df[(df["date"] >= pd.to_datetime(date_range[0])) & (df["date"] <= pd.to_datetime(date_range[1]))]

# --- KPI SUMMARY ---
st.title("Fakestore Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${df['revenue'].sum():,.2f}")
col2.metric("Total Carts", df["cart_id"].nunique())
col3.metric("Unique Users", df["user_id"].nunique())

# --- TABS LAYOUT ---
tabs = st.tabs(["Overview", "Users", "Products"])

# --- OVERVIEW TAB ---
with tabs[0]:
    st.subheader("Revenue by User")
    user_rev = df.groupby("full_name")["revenue"].sum().reset_index()
    user_chart = alt.Chart(user_rev).mark_bar().encode(
        x=alt.X("full_name:N", sort="-y", title="User"),
        y=alt.Y("revenue:Q", title="Revenue"),
        tooltip=["full_name", "revenue"]
    ).interactive()
    st.altair_chart(user_chart, use_container_width=True)

# --- USERS TAB ---
with tabs[1]:
    st.subheader("User Purchases")
    st.dataframe(df[["full_name", "city", "zipcode", "cart_id", "date", "title", "quantity", "revenue"]])

# --- PRODUCTS TAB ---
with tabs[2]:
    st.subheader("Top Products by Revenue")
    prod_rev = df.groupby("title")[["revenue",'quantity']].sum().reset_index().sort_values("revenue", ascending=False).head(10)
    prod_chart = alt.Chart(prod_rev).mark_bar(color="#2E86AB").encode(
        x=alt.X("revenue:Q", title="Revenue"),
        y=alt.Y("title:N", sort="-x", title="Product"),
        tooltip=["title", "revenue",'quantity']
    ).interactive()
    st.altair_chart(prod_chart, use_container_width=True)

    st.subheader("Revenue by Date")
    rev_by_date = df.groupby(df["date"].dt.date)["revenue"].sum().reset_index()
    date_chart = alt.Chart(rev_by_date).mark_line(point=True).encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("revenue:Q", title="Revenue"),
        tooltip=["date", "revenue"]
    ).interactive()
    st.altair_chart(date_chart, use_container_width=True)
