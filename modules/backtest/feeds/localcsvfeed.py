import os
import time
import pandas as pd
from lib.utils.convert_candle_by_time import *
from lib.utils.read_csv import *
from constants.common import CSV_PATH

class localcsvfeed():
      
      currentpointer=-1
      df=None
      

      def __init__(self,instrumentype,symbol, tf, fromDate, toDate):
          num_candles=200
         
          if instrumentype=="STOCK":
            interval =  360 if interval_to_number(tf) == 1440 else interval_to_number(tf)
            df=pd.read_csv(CSV_PATH+symbol+'.csv')
            #df['datetime']=pd.to_datetime(df['date'])  
            df.insert(0, 'datetime', pd.to_datetime(df['date']))
            df = df[df.datetime.between(fromDate, toDate)]
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

# if __name__ == '__main__':
#     obj = localfeed("STOCK","TCS", "15minute")
    #print(obj.df)
   
   
    
   # modes - live and backtesting
   # live 200 candles max previous - 200
   # default backtest day's candles max previous - 200 implement queue
   # 