-- schema.sql

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    email TEXT,
    username TEXT,
    password TEXT,
    name TEXT,
    phone TEXT
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    title TEXT,
    price NUMERIC,
    description TEXT,
    category TEXT,
    image TEXT
);

CREATE TABLE IF NOT EXISTS carts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    date TIMESTAMP,
    products JSONB
);
