import pandas as pd
import os

chunksize = 10 ** 8

def read_csv(file_path, callback, *argv):
    for chunk in pd.read_csv(file_path, chunksize=chunksize):
        for i in chunk.itertuples():
            callback(i, *argv)
            break

def get_historical_data_from_csv(file_path):
    return pd.read_csv(file_path, parse_dates=['TIME', 'Date', 'TIME1'], infer_datetime_format=True, index_col=0)

def read_all_csv_in_dir(path, cb):
    for root,dirs,files in os.walk(path):
            for file in files:
                if file.endswith(".csv"):
                    cb(file)