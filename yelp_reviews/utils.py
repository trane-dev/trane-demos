import pandas as pd
from trane.metadata import MultiTableMetadata


def load_data():
    dataframes = {
        "business": pd.read_json("data/yelp_academic_dataset_business.json", lines=True,
                                 dtype_backend='pyarrow'),
        "checkin": pd.read_json("data/yelp_academic_dataset_checkin.json", lines=True,
                                dtype_backend='pyarrow'),
        "review": pd.read_json("data/yelp_academic_dataset_review.json", lines=True,
                               dtype_backend='pyarrow'),
        "user": pd.read_json("data/yelp_academic_dataset_user.json", lines=True,
                             dtype_backend='pyarrow'),
    }
    dataframes["checkin"] = dataframes["checkin"][['type', 'business_id']]
    dataframes['business'].drop(['neighborhoods'], axis=1, inplace=True)
    relationships = [
        ("user", "user_id", "review", "user_id"),
        ("business", "business_id", "review", "business_id"),
        ("checkin", "business_id", "business", "business_id"),
    ]
    metadata = MultiTableMetadata.from_data(dataframes)
    metadata.add_relationships(relationships)
    metadata.set_primary_key("user", "user_id")
    metadata.set_primary_key("business", "business_id")
    metadata.set_primary_key("checkin", "business_id")
    metadata.set_primary_key("review", "review_id")
    metadata.set_time_key("review", "date")
    metadata.set_type("business", "business_id", "Categorical")
    metadata.set_type("business", "name", "Categorical")
    metadata.set_type("business", "address", "NaturalLanguage")
    metadata.set_type("business", "categories", "Categorical")
    metadata.set_type("business", "city", "Categorical")
    metadata.set_type("business", "neighborhoods", "Categorical")
    metadata.set_type("business", "state", "Categorical")
    metadata.set_type("business", "type", "Categorical")
    metadata.set_type("business", "full_address", "NaturalLanguage")

    metadata.set_type("review", "user_id", "Categorical")
    metadata.set_type("review", "review_id", "Categorical")
    metadata.set_type("review", "text", "NaturalLanguage")
    metadata.set_type("review", "business_id", "Categorical")
    metadata.set_type("review", "type", "Categorical")

    metadata.set_type("checkin", "type", "Categorical")
    metadata.set_type("checkin", "business_id", "Categorical")

    metadata.set_type("user", "user_id", "Categorical")
    metadata.set_type("user", "name", "Categorical")
    metadata.set_type("user", "type", "Categorical")
    return dataframes, metadata
