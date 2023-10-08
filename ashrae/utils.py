import pandas as pd
from trane.metadata import MultiTableMetadata


def load_data(nrows):
    train = pd.read_csv('data/train.csv', nrows=nrows)
    weather = pd.read_csv('data/weather_train.csv', nrows=nrows)
    building = pd.read_csv('data/building_metadata.csv', nrows=nrows)
    train['meter_id'] = range(train.shape[0])
    dataframes = {
        'meter_readings': train,
        'weather': weather,
        'building': building
    }
    metadata = MultiTableMetadata.from_data(dataframes)
    metadata.set_primary_key('building', 'building_id')
    metadata.set_primary_key('weather', 'site_id')
    metadata.set_primary_key('meter_readings', 'meter_id')
    metadata.set_time_index('meter_readings', 'timestamp')

    metadata.set_type('building', 'primary_use', 'Categorical')

    relationships = [
        ('building', 'building_id', 'meter_readings', 'building_id'),
        ('weather', 'site_id', 'building', 'site_id')
    ]
    metadata.add_relationships(relationships)
    return dataframes, metadata
