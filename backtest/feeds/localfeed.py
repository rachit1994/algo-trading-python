import os
from config.database.SQLAlchemy import SourceSqlalchemy
import time
import pandas as pd


class localfeed():
      
      currentpointer=-1
      df=None

      def __init__(cls,instrumentype,symbol):
          if instrumentype=="STOCK":
            sourcedbsession, sourcedbengine = SourceSqlalchemy()
            with sourcedbengine.connect() as con:
                cls.df = pd.read_sql('SELECT * FROM '+symbol+' LIMIT 20', con)
                cls.df["IS_UP"]= cls.df["CLOSE"] > cls.df["OPEN"]
                cls.df["IS_DOWN"]= cls.df["CLOSE"] < cls.df["OPEN"] 
                cls.currentpointer=0
                con.close()

      def __getitem__(self, index):
        try:
            return self.df.loc[self.currentpointer+index]
        except Exception as e:
              return None

      @property
      def next(self):
          self.currentpointer=self.currentpointer+1
          try:
            return self.df.loc[self.currentpointer]
          except Exception as e:
            return None

      @property
      def previous(self):
          try:
            self.currentpointer=self.currentpointer-1
            return self.df.loc[self.currentpointer]
          except Exception as e:
            return None


      

if __name__ == '__main__':
    obj = localfeed("STOCK","TCS")
    print(obj[2])
    print(obj[-2])
    obj.next
    print(obj[0])
   
    
   # modes - live and backtesting
   # live 200 candles max previous - 200
   # default backtest day's candles max previous - 200 implement queue
   # 


