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
from lib.utils.read_csv import read_all_csv_in_dir

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


def thread_loop():
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

def add_headers(csv_path):
    path = './kite_historical_data/' + csv_path
    file = pd.read_csv(path)
    # adding header
    headerList = ['date','open','high','low','close','volume','oi']
    # converting data frame to csv
    file.to_csv(path, header=headerList, index=False)


def read_and_all_header():
    read_all_csv_in_dir('./kite_historical_data', add_headers)

if __name__ == "__main__":
    # kite = KiteConnect(api_key=api_key)
    # print(kite.login_url())
    # login()
    # asyncio.run(fill_data())
    # thread_loop()
    # dict_to_pandas()
    # fill_data2()
    read_and_all_header()
