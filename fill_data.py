import logging
from kiteconnect import KiteConnect
from config.kite import api_key, request_token, api_secret, tokens_list, access_token, stocks
import pandas as pd
import datetime
from datetime import timedelta
from dateutil.tz import tzoffset
import multiprocessing
import time
from dateutil.relativedelta import relativedelta

logging.basicConfig(level=logging.DEBUG)

# Redirect the user to the login url obtained
# from kite.login_url(), and receive the request_token
# from the registered redirect url after the login flow.
# Once you have the request_token, obtain the access_token
# as follows.


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
    final_time = given_time + timedelta(minutes=n)
    while final_time <= now:
        data = kite.historical_data(
            instrument_token=stock["instrumenttoken"], from_date=given_time, oi=True, to_date=final_time, interval="minute")
        print("filling : ", stock["tradingsymbol"])
        print("data : ", len(data))
        df = pd.DataFrame.from_records(data)
        df.to_csv("./kite_historical_data/" +
                    stock["tradingsymbol"] + ".csv", mode='a', index=False, header=False)
        given_time = final_time + timedelta(minutes=1)
        final_time = given_time + timedelta(minutes=n)
        time.sleep(5)

# def fill_data2():
#     now = datetime.datetime.now()
#     n = 200
#     time_str = '2008-01-01 09:15:00'
#     date_format_str = '%Y-%m-%d %H:%M:%S'
#     kite = KiteConnect(api_key=api_key)
#     kite.set_access_token(access_token)
#     for stock in stocks:
#         given_time = datetime.datetime.strptime(time_str, date_format_str)
#         final_time = given_time + timedelta(minutes=n)
#         while final_time <= now:
#             data = kite.historical_data(
#                 instrument_token=stock["instrumenttoken"], from_date=given_time, oi=True, to_date=final_time, interval="minute")
#             if len(data) > 0:
#                 df = pd.DataFrame.from_records(data)
#                 print("filling : ", stock["tradingsymbol"])
#                 print("data : ", len(data))
#                 df.to_csv("./kite_historical_data/" +
#                             stock["tradingsymbol"] + ".csv", mode='a', index=False, header=False)
#                 given_time = final_time + timedelta(minutes=1)
#                 final_time = given_time + timedelta(minutes=n)
#             else:
#                 given_time = final_time + relativedelta(months=1)
#                 final_time = given_time + timedelta(minutes=n)
#             # time.sleep(3)

def thread_loop():
    # processes = []

    # for stock in stocks:
    #     p = multiprocessing.Process(target=fill_data, args=(stock,))
    #     p.start()
    #     processes.append(p)

    # for process in processes:
    #     process.join()
    pool = multiprocessing.Pool(len(stocks))
    pool.map(fill_data, stocks)
    pool.close()

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
    thread_loop()
    # dict_to_pandas()
    # fill_data2()
