import pandas as pd
from constants.common import CSV_PATH, mode
from datetime import datetime

def get_ticks_between_times(symbol, from_date, to_date):
    if mode == 'back_test':
        df = get_historical_data_from_csv(CSV_PATH+symbol+'.csv')
        return df[df.TIME.between(from_date, to_date)]

def subtract_minutes_from_time(timestamp, n):
    date_format_str = '%d/%m/%Y %H:%M:%S'
    given_time = datetime.strptime(timestamp, date_format_str)
    final_time = given_time - pd.DateOffset(minutes=n)
    final_time_str = final_time.strftime(date_format_str)
    return final_time_str