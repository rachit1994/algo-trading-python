import logging
from kiteconnect import KiteConnect
from config.kite import api_key, request_token, api_secret, tokens_list, access_token
import pandas as pd
import datetime
from datetime import timedelta
from dateutil.tz import tzoffset
import multiprocessing
import time
from dateutil.relativedelta import relativedelta
from os.path import exists
import os

logging.basicConfig(level=logging.DEBUG)

def login():
    kite = KiteConnect(api_key=api_key)
    data = kite.generate_session(request_token, api_secret=api_secret)
    access_token = data["access_token"]
    print(data["access_token"])
    kite.set_access_token(access_token)


def fill_data(stock):
    now = datetime.datetime.now()
    n = 1440
    time_str = '2015-01-01 09:15:00'
    date_format_str = '%Y-%m-%d %H:%M:%S'
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)
    given_time = datetime.datetime.strptime(time_str, date_format_str)
    file_path = "./kite_historical_data/"+ stock["tradingsymbol"] + ".csv"
    if exists(file_path) and not os.stat(file_path).st_size == 0:
        df1 = pd.read_csv(file_path, header=None, delim_whitespace=True)
        print(stock["tradingsymbol"] , df1.empty)
        if not df1.empty:
            last_row =  df1.iloc[-1]
            time_str = last_row[0]
            given_time = pd.to_datetime(time_str) + timedelta(minutes=1)
    final_time = given_time + timedelta(minutes=n)
    while final_time <= now:
        data = kite.historical_data(
            instrument_token=str(stock["instrument_token"]), from_date=given_time, oi=True, to_date=final_time, interval="minute")
        print("filling : ", stock["tradingsymbol"])
        print("data : ", len(data))
        df = pd.DataFrame.from_records(data)
        df.to_csv("./kite_historical_data/" +
                    stock["tradingsymbol"] + ".csv", mode='a', index=False, header=False)
        given_time = final_time + timedelta(minutes=1)
        final_time = given_time + timedelta(minutes=n)
        time.sleep(5)

def thread_loop(stocks):
    pool = multiprocessing.Pool(len(stocks))
    pool.map(fill_data, stocks)
    # pool.close()

def print_data():
    n = 100
    time_str = '2020-01-01 09:15:00'
    date_format_str = '%Y-%m-%d %H:%M:%S'
    given_time = datetime.strptime(time_str, date_format_str)
    final_time = given_time + timedelta(minutes=n)
    kite = KiteConnect(api_key=api_key)
    data = kite.historical_data(instrument_token=897537, from_date=given_time,
                                oi=True, to_date=final_time, interval="minute")
    print(data)


def dict_to_pandas():
    di = [{'date': datetime.datetime(2020, 1, 1, 9, 15, tzinfo=tzoffset(None, 19800)), 'open': 1194.45, 'high': 1196.9, 'low': 1194.45, 'close': 1195, 'volume': 13143, 'oi': 0}]
    df = pd.DataFrame.from_records(di)
    df.to_csv("test.csv")


if __name__ == "__main__":
    # kite = KiteConnect(api_key=api_key)
    # print(kite.login_url())
    # login()
    # asyncio.run(fill_data())
    for chunk in pd.read_csv('./temp/instruments.csv', chunksize=10):
        thread_loop(chunk.to_dict('records'))
    