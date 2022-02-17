import os
from lib.database.SQLAlchemy import SourceSqlalchemy
from lib.entities.StockData import StockData
from lib.entities.Candle import Candle
import time



class DataFeedProvider():
      
      currentCandlePointer=-1
      stockdataobjresultset=None
      def __init__(cls,symbol, fromdate, todate):
        cls.symbol=symbol
        cls.currentCandlePointer=-1
        sourcedbsession, sourcedbengine = SourceSqlalchemy()
        stockdataobj=StockData().get_table_object(symbol)
        cls.stockdataobjresultset=sourcedbsession.query(stockdataobj).filter(stockdataobj.c.TIMESTAMP >= fromdate+"+05:30",stockdataobj.c.TIMESTAMP <= todate+"+05:30").all()
        if cls.stockdataobjresultset != None:
           cls.currentCandlePointer=0
      
      def currentCandle(self):
          return Candle(self.stockdataobjresultset[self.currentCandlePointer], self.symbol)
      
      def nextCandle(self):
          return Candle(self.stockdataobjresultset[self.currentCandlePointer+1], self.symbol)

      def previousCandle(self):
          return Candle(self.stockdataobjresultset[self.currentCandlePointer-1], self.symbol)

      def moveToNextCandle(self):
          self.currentCandlePointer=self.currentCandlePointer+1
          return Candle(self.stockdataobjresultset[self.currentCandlePointer], self.symbol)

      def moveToPreviousCandle(self):
          self.currentCandlePointer=self.currentCandlePointer-1
          return Candle(self.stockdataobjresultset[self.currentCandlePointer], self.symbol)

      def __getitem__(self, index):
        return Candle(self.stockdataobjresultset[self.currentCandlePointer+index], self.symbol)

      def __len__(self):
          return len(self.stockdataobjresultset)

      @property
      def next(self):
          self.currentCandlePointer=self.currentCandlePointer+1
          return Candle(self.stockdataobjresultset[self.currentCandlePointer], self.symbol)

      @property
      def previous(self):
          self.currentCandlePointer=self.currentCandlePointer-1
          return Candle(self.stockdataobjresultset[self.currentCandlePointer], self.symbol)

      
      def next(self, count):
          self.currentCandlePointer=self.currentCandlePointer+count
          return Candle(self.stockdataobjresultset[self.currentCandlePointer], self.symbol)

      def previous(self, count):
          self.currentCandlePointer=self.currentCandlePointer-count
          return Candle(self.stockdataobjresultset[self.currentCandlePointer], self.symbol)

      def slice(self, fromCount, toCount):
          res=self.stockdataobjresultset[fromCount:toCount]
          finalres=[]
          for r in res:
            finalres.append(Candle(r, self.symbol))
          return finalres

      

if __name__ == '__main__':
    obj=DataFeedProvider("TCS","2015-02-02 09:15:00","2015-02-02 09:50:00")
    # print(obj[0])
    # print(obj[-2]) # Returns next candle without moving pointer
    # print(obj[0])
    # print(obj[-2]) # Returns next candle without moving pointer
    # print(len(obj)) # Print length of resultset
    # obj.next
    # obj.previous
    obj.next(3)
    print(obj[0])
   
    
   # modes - live and backtesting
   # live 200 candles max previous - 200
   # default backtest day's candles max previous - 200 implement queue
   # 