import os
from config.database.SQLAlchemy import SourceSqlalchemy
import time
import pandas as pd
from backtest.utils.convert_candle_by_time import *


class localfeed():
      
      currentpointer=-1
      df=None

      def __init__(cls,instrumentype,symbol, tf):
          if instrumentype=="STOCK":
            interval = interval_to_number(tf) if interval_to_number(tf) > 1 else 1

            sourcedbsession, sourcedbengine = SourceSqlalchemy()
            with sourcedbengine.connect() as con:
                df = pd.read_sql('SELECT TIMESTAMP as datetime, OPEN, HIGH, LOW, CLOSE, VOLUME, OI as openinterest FROM '+symbol+' LIMIT '+(200*interval).__str__(), con)
                df['datetime']=pd.to_datetime(cls.df['datetime'])  
                self.df = self.groupby(df,interval)         
                cls.currentpointer=0               
                con.close()

    

      def groupby(self, df, interval):

        base = int(interval/2) if (interval % 2)==0 else 0

        df = df.set_index('datetime').resample(
             interval.__str__()+'min', base=base).mean().dropna()

        return df

if __name__ == '__main__':
    obj = localfeed("STOCK","TCS", "15minute")
    #print(obj.df)
   
   
    
   # modes - live and backtesting
   # live 200 candles max previous - 200
   # default backtest day's candles max previous - 200 implement queue
   # 