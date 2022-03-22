import os
from lib.database.SQLAlchemy import SourceSqlalchemy
import time
import pandas as pd
from lib.utils.convert_candle_by_time import *


class localfeed():
      
      currentpointer=-1
      df=None
      

      def __init__(self,instrumentype,symbol, tf):
          num_candles=200
          from_data = "2022-01-03 09:00:00+05:30"
          to_data = "2022-01-07 16:00:00+05:30"
          if instrumentype=="STOCK":
            interval =  360 if interval_to_number(tf) == 1440 else interval_to_number(tf)

            sourcedbsession, sourcedbengine = SourceSqlalchemy()
            with sourcedbengine.connect() as con:
                df = pd.read_sql('SELECT TIMESTAMP as datetime, OPEN, HIGH, LOW, CLOSE, VOLUME, OI as openinterest FROM '+symbol+' WHERE TIMESTAMP >= "'+from_data+'" AND TIMESTAMP<="'+to_data+'"', con)
                #df = pd.read_sql('SELECT TIMESTAMP as datetime, OPEN, HIGH, LOW, CLOSE, VOLUME, OI as openinterest FROM '+symbol+' LIMIT '+(num_candles*interval).__str__(), con)
                #df = pd.read_sql('SELECT TIMESTAMP as datetime, OPEN, HIGH, LOW, CLOSE, VOLUME, OI as openinterest FROM '+symbol+' LIMIT 720', con)
                df['datetime']=pd.to_datetime(df['datetime'])  
          
                self.df = df
                self.df = self.groupby(interval)
                self.currentpointer=0  
                con.close()

    

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