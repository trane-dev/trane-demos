import os

import pandas as pd
from trane.metadata import MultiTableMetadata


def load_instacart_data(dtype_backend='pyarrow', nrows=None):
    """Load Instacart data from CSV files and return a
    dictionary containing the dataframes.
    """
    directory = os.path.dirname(os.path.realpath(__file__))
    directory = os.path.join(directory, 'data')
    aisles = pd.read_csv(f'{directory}/aisles.csv', nrows=nrows,
                         dtype_backend=dtype_backend)
    departments = pd.read_csv(f'{directory}/departments.csv', nrows=nrows,
                              dtype_backend=dtype_backend)
    order_products = pd.read_csv(f"{directory}/order_products__prior.csv",
                                       nrows=nrows, dtype_backend=dtype_backend)
    # prior_order_train = pd.read_csv(f"{directory}/order_products__train.csv",
    #                                 nrows=nrows, dtype_backend=dtype_backend)

    # order_products = pd.concat([prior_order_products, prior_order_train])

    orders = pd.read_csv(f'{directory}/orders.csv',
                         dtype_backend=dtype_backend,
                         nrows=nrows)
    products = pd.read_csv(f'{directory}/products.csv',
                           dtype_backend=dtype_backend,
                           nrows=nrows)

    orders = orders.groupby("user_id").apply(add_time)
    orders.reset_index(drop=True, inplace=True)
    orders = orders[["order_id", "order_time", "user_id"]]

    order_products.reset_index(drop=True, inplace=True)
    order_products["order_product_id"] = range(order_products.shape[0])
    order_products.drop(["add_to_cart_order"], axis=1, inplace=True)

    dataframes = {
        'aisles': aisles,
        'departments': departments,
        'products': products,
        'order_products': order_products,
        'orders': orders,
    }
    relationships = [
        ('aisles', 'aisle_id', 'products', 'aisle_id'),
        ('departments', 'department_id', 'products', 'department_id'),
        ('products', 'product_id', 'order_products', 'product_id'),
        ('orders', 'order_id', 'order_products', 'order_id'),
    ]
    metadata = MultiTableMetadata.from_data(dataframes)
    metadata.add_relationships(relationships)
    assert aisles['aisle_id'].is_unique
    assert departments['department_id'].is_unique
    assert order_products['order_product_id'].is_unique
    assert products['product_id'].is_unique
    assert orders['order_id'].is_unique
    metadata.set_primary_key('aisles', 'aisle_id')
    metadata.set_primary_key('departments', 'department_id')
    metadata.set_primary_key('order_products', 'order_product_id')
    metadata.set_primary_key('products', 'product_id')
    metadata.set_primary_key('orders', 'order_id')

    metadata.set_time_index('orders', 'order_time')

    metadata.set_type('aisles', 'aisle', 'Categorical')
    metadata.set_type('departments', 'department', 'Categorical')
    metadata.set_type('products', 'product_name', 'Categorical')
    return dataframes, metadata

def add_time(df):
    df["order_time"] = pd.NaT
    days_since = df.columns.tolist().index("days_since_prior_order")
    hour_of_day = df.columns.tolist().index("order_hour_of_day")
    order_time = df.columns.tolist().index("order_time")

    df.iloc[0, order_time] = pd.Timestamp('Jan 1, 2015') +  pd.Timedelta(df.iloc[0, hour_of_day], "h")
    for i in range(1, df.shape[0]):
        df.iloc[i, order_time] = df.iloc[i-1, order_time] \
                                    + pd.Timedelta(df.iloc[i, days_since], "d") \
                                    + pd.Timedelta(df.iloc[i, hour_of_day], "h")

    to_drop = ["order_number", "order_dow", "order_hour_of_day", "days_since_prior_order", "eval_set"]
    df.drop(to_drop, axis=1, inplace=True)
    return df