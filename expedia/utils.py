import pandas as pd
from trane import metadata
from trane.metadata import SingleTableMetadata

def load_data(nrows):
    data = pd.read_csv("data/train.csv", dtype_backend='pyarrow', nrows=nrows)

    metadata = SingleTableMetadata.from_data(data)
    ml_types = {
        "date_time": "Datetime",
        "site_name": "Categorical",
        "posa_continent": "Categorical",
        "user_location_country": "Categorical",
        "user_location_region": "Categorical",
        "user_location_city": "Categorical",
        "orig_destination_distance": "Double",
        "user_id": "Categorical",
        "is_mobile": "Boolean",
        "is_package": "Boolean",
        "channel": "Categorical",
        "srch_ci": "Datetime",
        "srch_co": "Datetime",
        "srch_adults_cnt": "Integer",
        "srch_children_cnt": "Integer",
        "srch_rm_cnt": "Integer",
        "srch_destination_id": "Categorical",
        "srch_destination_type_id": "Categorical",
        "hotel_continent": "Categorical",
        "hotel_country": "Categorical",
        "hotel_market": "Categorical",
        "is_booking": "Boolean",
        "cnt": "Integer",
        "hotel_cluster": "Categorical"
    }
    for column, ml_type in ml_types.items():
        metadata.set_type(column, ml_type)
    return data, metadata