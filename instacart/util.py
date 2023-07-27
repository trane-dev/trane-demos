import pandas as pd
from trane.typing.column_schema import ColumnSchema
from trane.typing.logical_types import (
    Categorical,
    Datetime,
    Double,
    Integer,
)

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

def get_meta(df, entity_col):
    meta = {}
    for col in df.columns:
        if df[col].dtype == "int":
            meta[col] = ColumnSchema(
                Integer,
                semantic_tags=({"numeric"} if col != entity_col else {"numeric", "primary_key"})
            )
        if df[col].dtype == "float":
            meta[col] = ColumnSchema(
                Double,
                semantic_tags=({"numeric"} if col != entity_col else {"numeric", "primary_key"})
            )
        if df[col].dtype == "object":
            meta[col] = ColumnSchema(
                Categorical,
                semantic_tags=({"category"} if col != entity_col else {"category", "primary_key"})
            )
        if df[col].dtype == "datetime64[ns]":
            meta[col] = ColumnSchema(
                Datetime,
                semantic_tags=({} if col != entity_col else {"primary_key"})
            )
    return meta