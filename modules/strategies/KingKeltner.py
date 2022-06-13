
# Create a subclass of Strategy to define the indicators and logic
import backtrader as bt
from conf import *

class KingKeltner(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        length=40
    )

    alias = ("KingKeltner", "KingKeltner")

    def __init__(self):
        self.movAvg = bt.ind.SMA(period=self.p.length).data0_close
        self.atr = bt.ind.ATR(period=self.p.length)  # fast moving average
       
        self.upBand = self.movAvg + self.atr 
        self.dnBand = self.movAvg - self.atr 

        self.MarketPosition = 0
        self.prevMovAvg= 0
        self.executionPrice = 0
       
    def next(self):
        
        
        if(self.MarketPosition == 0) :             

            if self.movAvg < self.prevMovAvg  and self.data.close[0] < self.upBand:
                print("self.sell at -> "+ self.data.close[0].__str__())
                self.executionPrice = self.data.close[0]
                quantity = round ((startcash * (portfolioutilizationpercentage/100)) / self.executionPrice)
                self.buy(size=quantity)
                self.targetPrice = self.executionPrice - (self.executionPrice * target / 100)
                self.slPrice = self.executionPrice + (self.executionPrice * sl / 100)
                self.MarketPosition=1
            elif self.movAvg > self.prevMovAvg and self.data.close[0] > self.dnBand:
                 print("self.buy at -> "+ self.data.close[0].__str__())
                 self.executionPrice = self.data.close[0]
                 quantity = round ((startcash * (portfolioutilizationpercentage/100)) / self.executionPrice)
                 self.buy(size=quantity)
                 self.targetPrice = self.executionPrice + (self.executionPrice * target / 100)
                 self.slPrice = self.executionPrice - (self.executionPrice * sl / 100)
                 self.MarketPosition=-1
            else :
                self.prevMovAvg = self.movAvg

        else:
            #self.liqDays = self.liqDays - 1;
            #print(self.liqDays)
            #self.liqDays = 50;
            #self.avgClose= bt.ind.SMA(period=self.liqDays)
            hour = self.data.datetime.time().hour
            minute = self.data.datetime.time().minute

            if intraday==True and (hour == 9 and minute == 45):
                 print("self.exit at  -> "+ self.data.close[0].__str__())
                 self.close()
                 self.MarketPosition =0
            #elif self.MarketPosition == 1 and (self.executionPrice - self.data.close[0] > 100 or self.executionPrice - self.data.close[0] < -100): #self.avgClose < self.upBand:
            elif self.MarketPosition == 1 and (self.targetPrice > self.data.close[0]  or self.slPrice < self.data.close[0]) : 
                 print("self.exit at  -> "+ self.data.close[0].__str__())
                 self.close()
                 self.MarketPosition =0
            
            #elif self.MarketPosition == -1 and (self.data.close[0] - self.executionPrice  > 100 or self.data.close[0] - self.executionPrice  < -100):#and self.avgClose > self.dnBand:
            elif self.MarketPosition == -1 and (self.targetPrice < self.data.close[0]  or self.slPrice > self.data.close[0]) : 
                 print("self.exit at  -> "+ self.data.close[0].__str__())
                 self.close()
                 self.MarketPosition =0
            


            
     