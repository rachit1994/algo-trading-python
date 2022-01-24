from lib.utils.stock_data import get_ticks_between_times, subtract_minutes_from_time

def interval_to_number(interval):
    m = {"minute": 1, "day": 1440, "3minute": 3, "5minute": 5, "10minute": 10, "15minute": 15, "30minute": 30,
         "60minute": 60}
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
    current_time = candle.TIME
    m = interval_to_number(altinterval)
    before_time = subtract_minutes_from_time(current_time, m)
    candles = get_ticks_between_times(candle.symbol, before_time, current_time)
    if not candles.empty:
        grouped_candles = candles.resample("1H").mean()
    return grouped_candles