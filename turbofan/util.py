import pandas as pd

def load_data():
    index_names = ['unit_number', 'time_cycles']
    setting_names = ['setting_1', 'setting_2', 'setting_3']
    sensor_names = ['s_{}'.format(i+1) for i in range(0,21)]
    col_names = index_names + setting_names + sensor_names

    df_train = pd.read_csv('data/train_FD001.txt',sep='\s+',header=None,index_col=False,names=col_names)
    #df_valid = pd.read_csv('data/test_FD001.txt',sep='\s+',header=None,index_col=False,names=col_names)
    #y_valid = pd.read_csv('data/RUL_FD001.txt',sep='\s+',header=None,index_col=False,names=['RUL'])

    def add_date(df):
        df["date"] = pd.to_datetime("2023-01-01") + pd.to_timedelta(df["time_cycles"], unit="d")
        df = df.sort_values(["unit_number", "date"])
        return df

    df_train = add_date(df_train)
    #df_valid = add_date(df_valid)

    return df_train