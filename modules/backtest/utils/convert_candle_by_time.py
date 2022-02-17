from .stock_data import *

def interval_to_number(interval):
    m = {"minute": 1, "day": 1440, "3minute": 3, "3min": 3, "5minute": 5, "5min": 5, "10minute": 10, "10min": 10, "15minute": 15, "15min": 15, "30minute": 30, "30min": 30,
         "60minute": 60, "60min": 60 }
    return m[interval]

def alttf_to_tf_factor(interval, altinterval):
    m = interval_to_number(interval)
    if m[interval] > m[altinterval]:
        raise Exception("alttf can not be less than tf")
    if m[altinterval] % m[interval]:
        raise Exception("alttf needs to be a multiple of tf")
    return m[altinterval] // m[interval]

def get_grouped_candles(candle, interval, altinterval):
    grouped_candles = []
    current_time = candle.datetime
    m = interval_to_number(altinterval)
    before_time = subtract_minutes_from_time(current_time, m)
    candles = get_ticks_between_times(candle, before_time, current_time)
    if not candles.empty:
        grouped_candles = candles.resample(altinterval).mean()
    return grouped_candles