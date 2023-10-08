import pandas as pd
from trane import SingleTableMetadata

def load_data():
    index_names = ['Engine', 'Cycle']
    setting_names = ['Setting 1', 'Setting 2', 'Setting 3']
    sensor_names = [ "(Fan Inlet Temperature) (◦R)",
        "(LPC Outlet Temperature) (◦R)",
        "(HPC Outlet Temperature) (◦R)",
        "(LPT Outlet Temperature) (◦R)",
        "(Fan Inlet Pressure) (psia)",
        "(Bypass-Duct Pressure) (psia)",
        "(HPC Outlet Pressure) (psia)",
        "(Physical Fan Speed) (rpm)",
        "(Physical Core Speed) (rpm)",
        "(Engine Pressure Ratio(P50/P2)",
        "(HPC Outlet Static Pressure) (psia)",
        "(Ratio of Fuel Flow to Ps30) (pps/psia)",
        "(Corrected Fan Speed) (rpm)",
        "(Corrected Core Speed) (rpm)",
        "(Bypass Ratio) ",
        "(Burner Fuel-Air Ratio)",
        "(Bleed Enthalpy)",
        "(Required Fan Speed)",
        "(Required Fan Conversion Speed)",
        "(High-Pressure Turbines Cool Air Flow)",
        "(Low-Pressure Turbines Cool Air Flow)",
        "Sensor 26",
        "Sensor 27"]
    col_names = index_names + setting_names + sensor_names
    df_train = pd.read_csv('data/train_FD001.txt',sep='\s+',header=None,index_col=False,names=col_names)

    def add_date(df):
        df["date"] = pd.to_datetime("2023-01-01") + pd.to_timedelta(df["Cycle"], unit="d")
        df = df.sort_values(["Engine", "date"])
        return df

    df_train = add_date(df_train)
    metadata = SingleTableMetadata.from_data(df_train)
    return df_train, metadata