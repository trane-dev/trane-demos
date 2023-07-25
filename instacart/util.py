import pandas as pd

def load_data():
    dataframes = {
        "orders": (pd.read_csv("data/orders.csv"), "id"),
        "order_products": (pd.read_csv("data/order_products.csv"), "id"),
        "products": (pd.read_csv("data/products.csv"), "id"),
        "aisles": (pd.read_csv("data/aisles.csv"), "id"),
        "departments": (pd.read_csv("data/departments.csv"), "id"),
    }
    dataframes["orders"][0]["order_date"] = pd.to_datetime("2023-01-01") + pd.to_timedelta(dataframes["orders"][0]["order_id"] // 10000, unit="D")
    dataframes["orders"][0]["order_date"] = pd.to_datetime(dataframes["orders"][0]["order_date"])
    dataframes["orders"][0]["user_id"] = dataframes["orders"][0]["user_id"].astype("int")
    
    relationships = [
        ("aisles", "aisle_id", "products", "aisle_id"),
        ("departments", "department_id", "products", "department_id"),
        ("products", "product_id", "order_products", "product_id"),
        ("orders", "order_id", "order_products", "order_id"),
    ]

    return dataframes, relationships