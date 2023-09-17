import pandas as pd
from trane.metadata import MultiTableMetadata

def load_instacart_data():
    """Load Instacart data from CSV files and return a
    dictionary containing the dataframes.
    """
    aisles = pd.read_csv('data/aisles.csv', dtype_backend='pyarrow')
    departments = pd.read_csv('data/departments.csv', dtype_backend='pyarrow')
    order_products = pd.concat([pd.read_csv("data/order_products__prior.csv"),
                                pd.read_csv("data/order_products__train.csv")]
                                , dtype_backend='pyarrow')
    orders = pd.read_csv('data/orders.csv', dtype_backend='pyarrow')
    products = pd.read_csv('data/products.csv', dtype_backend='pyarrow')

    dataframes = {
        'aisles': aisles,
        'departments': departments,
        'order_products': order_products,
        'orders': orders,
        'products': products,
    }
    relationships = [
        ('orders', 'order_id', 'order_products', 'order_id'),
        ('order_products', 'product_id', 'products', 'product_id'),
        ('products', 'aisle_id', 'aisles', 'aisle_id'),
        ('products', 'department_id', 'departments', 'department_id'),
    ]
    metadata = MultiTableMetadata.from_data(dataframes)
    metadata.add_relationships(relationships)
    assert orders['order_id'].is_unique
    assert orders['order_products'].is_unique
    assert orders['order_id'].is_unique
    assert orders['order_id'].is_unique
    assert orders['order_id'].is_unique
    metadata.set_primary_key('orders', 'order_id')
    metadata.set_primary_key('order_products', 'order_id')
    metadata.set_primary_key('products', 'product_id')
    metadata.set_primary_key('aisles', 'aisle_id')
    metadata.set_primary_key('departments', 'department_id')
    return dataframes, metadata

load_instacart_data()