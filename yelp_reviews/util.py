import pandas as pd
import json
from trane.typing.column_schema import ColumnSchema
from trane.typing.logical_types import (
    Categorical,
    Datetime,
    Double,
    Integer,
)

def load_data():
    dataframes = {
        "business": (pd.read_json("data/yelp_academic_dataset_business.json", lines=True), "id"),
        "checkin": (pd.read_json("data/yelp_academic_dataset_checkin.json", lines=True), "id"),
        "review": (pd.read_json("data/yelp_academic_dataset_review.json", lines=True), "id"),
        "user": (pd.read_json("data/yelp_academic_dataset_user.json", lines=True), "id"),
    }
    
    dataframes["checkin"] = (
        dataframes["checkin"][0][['type', 'business_id']],
        "id"
    )

    relationships = [
        ("user", "user_id", "review", "user_id"),
        ("business", "business_id", "review", "business_id"),
        ("checkin", "business_id", "business", "business_id"),
    ]

    return dataframes, relationships

def get_meta(df, entity_col):
    meta = {}
    for col in df.columns:
        if df[col].dtype == "int":
            meta[col] = ColumnSchema(
                Integer,
                semantic_tags=({"numeric"} if col != entity_col else {"numeric", "index"})
            )
        if df[col].dtype == "float":
            meta[col] = ColumnSchema(
                Double,
                semantic_tags=({"numeric"} if col != entity_col else {"numeric", "index"})
            )
        if df[col].dtype == "object":
            meta[col] = ColumnSchema(
                Categorical,
                semantic_tags=({"category"} if col != entity_col else {"category", "index"})
            )
        if df[col].dtype == "datetime64[ns]":
            meta[col] = ColumnSchema(
                Datetime,
                semantic_tags=({} if col != entity_col else {"index"})
            )
    return meta