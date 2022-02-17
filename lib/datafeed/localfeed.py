import os
from config.database.SQLAlchemy import SourceSqlalchemy
import time
import pandas as pd
from backtest.utils.convert_candle_by_time import *


class localfeed():
      
      currentpointer=-1
      df=None
      

      def __init__(cls,instrumentype,symbol, tf):
          num_candles=5
          if instrumentype=="STOCK":
            interval = interval_to_number(tf) if interval_to_number(tf) > 1 else 1

            sourcedbsession, sourcedbengine = SourceSqlalchemy()
            with sourcedbengine.connect() as con:
                df = pd.read_sql('SELECT TIMESTAMP as datetime, OPEN, HIGH, LOW, CLOSE, VOLUME, OI as openinterest FROM '+symbol+' LIMIT '+(num_candles*interval).__str__(), con)
                df['datetime']=pd.to_datetime(df['datetime'])  
                cls.df = df
                cls.df = cls.groupby(interval)      

                print(cls.df)   
                cls.currentpointer=0               
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
        elif interval==1440:
         base=555

       
        df = self.df.set_index('datetime').resample(
             interval.__str__()+'min', base=base).mean().dropna()

        return df

if __name__ == '__main__':
    obj = localfeed("STOCK","TCS", "day")
    #print(obj.df)
   
   
    
   # modes - live and backtesting
   # live 200 candles max previous - 200
   # default backtest day's candles max previous - 200 implement queue
   # 