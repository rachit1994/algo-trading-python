import numpy as np
import pandas as pd
import requests
import datetime
import openpyxl
from lib.utils.convert_candle_by_time import *


class kiteLiveFeed():

    def __init__(self,instrumentype,symbol, tf, fromDate, toDate):


      if instrumentype=="OPTIONS":
            instrument = 10422786  # BANKNIFTY2260935300PE

            interval =  360 if interval_to_number(tf) == 1440 else interval_to_number(tf)

            header = {
                    "Authorization": "enctoken Kt9kksvYX9plLZytmm+1/bw5OYT6KvIzr42FJzI/5OQo27kLm2kiNSyaWMbe5wzLrz6hR2vbB4zkc2t1RyvI9drP8k/AAFnP7F0PtmlmOmI5dyXYDqXIRg=="}
            url = 'https://kite.zerodha.com/oms/instruments/historical/' + \
                                    instrument.__str__()+'/minute?user_id=YY4988&oi=1&from=' + \
                                                       fromDate+'&to='+toDate
            #print(url)
            response = requests.get(
                                url, headers=header).json()
          

            df = pd.DataFrame (response['data']['candles'])
            df.columns = ['date','open','high','low','close','volume','oi']

            #df['datetime']=pd.to_datetime(df['date'])  
            df.insert(0, 'datetime', pd.to_datetime(df['date']))
            #df = df[df.datetime.between(fromDate, toDate)]
            df.drop(columns =['date'])
          
            self.df = df
            self.df = self.groupby(interval)
            self.currentpointer=0  

     


    def groupby(self, interval):

            if interval==1 or interval==3 or interval==5 or interval==15:
                 base=0
            elif interval==10:
                base=5 
            elif interval==30:
                 base=15
            elif interval==60:
                 base=15
            elif interval==360:
                 base=555
            df = self.df.set_index('datetime').resample(
                '1440min', base=base).mean().dropna()
            return df

            df = self.df.set_index('datetime').resample(
                interval.__str__()+'min', base=base).mean().dropna()
            #print(df)         
            return df


#kiteLiveFeed()

     