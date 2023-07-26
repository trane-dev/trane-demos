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

    def votes_json_to_cols(votes):
        return pd.Series([votes["funny"], votes["useful"], votes["cool"]], index=["votes_funny", "votes_useful", "votes_cool"])

    dataframes["review"] = (pd.concat([dataframes["review"][0].drop("votes", axis=1), dataframes["review"][0]["votes"].apply(votes_json_to_cols)], axis=1), "id")
    dataframes["user"] = (pd.concat([dataframes["user"][0].drop("votes", axis=1), dataframes["user"][0]["votes"].apply(votes_json_to_cols)], axis=1), "id")

    keys = []
    for h in range(24):
        for d in range(7):
            keys.append(str(h) + "-" + str(d))

    def checkin_info_json_to_cols(checkin_info):
        return pd.Series([checkin_info[k] if k in checkin_info else 0 for k in keys], index=keys)
    dataframes["checkin"] = (pd.concat([dataframes["checkin"][0].drop("checkin_info", axis=1), dataframes["checkin"][0]["checkin_info"].apply(checkin_info_json_to_cols)], axis=1), "id")
    
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