import pandas as pd
from trane.metadata import SingleTableMetadata


def load_data(nrows=None):
    train = pd.read_csv('data/train.csv', nrows=nrows)
    weather = pd.read_csv('data/weather_train.csv', nrows=nrows)
    building = pd.read_csv('data/building_metadata.csv', nrows=nrows)
    train['meter_id'] = range(train.shape[0])

    train = train.merge(building, left_on = "building_id", right_on = "building_id", how = "left")
    train = train.merge(weather, left_on = ["site_id", "timestamp"], right_on = ["site_id", "timestamp"])
    del weather, building

    dataframe = train
    metadata = SingleTableMetadata.from_data(dataframe)
    metadata.set_primary_key('meter_id')
    metadata.set_time_key('timestamp')
    metadata.set_type('primary_use', 'Categorical')
    return dataframe, metadata
