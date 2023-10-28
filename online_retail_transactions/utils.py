import pandas as pd
from trane.metadata import SingleTableMetadata
import os

def load_retail(force_reload=False):
    """Load retail data from CSV files and return a
    dictionary containing the dataframes.
    """
    directory = os.path.dirname(os.path.realpath(__file__))
    directory = os.path.join(directory, 'data')
    parquet_file = os.path.join(directory, 'online_retail_II.parquet')
    excel_file = os.path.join(directory, 'online_retail_II.xlsx')

    dtypes = {
        'Invoice': 'string[pyarrow]',
        'StockCode': 'string[pyarrow]',
        'Description': 'string[pyarrow]',
        'Quantity': 'int64[pyarrow]',
        'InvoiceDate': 'datetime64[ns]',
        'Price': 'float64[pyarrow]',
        'Customer ID': 'int64[pyarrow]',
        'Country': 'category'
    }
    if not os.path.exists(parquet_file) or force_reload:
        df = pd.read_excel(excel_file, dtype_backend='pyarrow')
    else:
        df = pd.read_parquet(parquet_file, dtype_backend='pyarrow')
    df = df.astype(dtypes)
    metadata = SingleTableMetadata.from_data(df)
    metadata.set_type('Invoice', 'Categorical')
    metadata.set_type('StockCode', 'Categorical')
    metadata.set_type('Description', 'Categorical')
    metadata.set_type('Customer ID', 'Categorical')
    metadata.set_type('Country', 'Categorical')
    metadata.set_time_key('InvoiceDate')
    metadata.ml_types['Customer ID'].add_tags('foreign_key')
    df.to_parquet(parquet_file, engine='pyarrow', index=False, compression='gzip')
    return df, metadata