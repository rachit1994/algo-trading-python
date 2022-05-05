# Reference -> https://www.academia.edu/26092045/THE_BOLLINGER_BANDIT_TRADING_STRATEGY

# Create a subclass of Strategy to define the indicators and logic
import backtrader as bt

class BollingerBandit(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        bollingerLengths=50,  
        liqLength=50,   
        rocCalcLength=30,
        #size=20,
        #debug=True,
    )

    alias = ("BollBand", "BollingerBandit")

    def __init__(self):
        self.boll = bt.ind.BollingerBands(period=self.p.bollingerLengths, devfactor=1.25)  # fast moving average
        self.upBand = self.boll.lines.top
        self.dnBand = self.boll.lines.bot
        self.rocCalc = self.data.close - self.data.close[self.p.rocCalcLength-1];
        self.MarketPosition = 0
        self.liqDays = self.p.liqLength
        self.avgClose= bt.ind.SMA(period=self.liqDays).data0_close
        self.executionPrice = 0
       
    def next(self):
        
        if(self.MarketPosition == 0) :             

            if self.rocCalc > 0 and self.avgClose < self.upBand:
                print("self.sell at -> "+ self.data.close[0].__str__())
                self.sell()
                self.executionPrice = self.data.close[0]
                self.MarketPosition=1
            elif self.rocCalc < 0 and self.avgClose > self.dnBand:
                 print("self.buy at -> "+ self.data.close[0].__str__())
                 self.buy()
                 self.executionPrice = self.data.close[0]
                 self.MarketPosition=-1

        else:
            #self.liqDays = self.liqDays - 1;
            #print(self.liqDays)
            #self.liqDays = 50;
            #self.avgClose= bt.ind.SMA(period=self.liqDays)
            if self.MarketPosition == 1 and (self.executionPrice - self.data.close[0] > 100 or self.executionPrice - self.data.close[0] < -200): #self.avgClose < self.upBand:
                 print("self.exit at  -> "+ self.data.close[0].__str__())
                 self.close()
                 self.MarketPosition =0
            elif self.MarketPosition == -1 and (self.data.close[0] - self.executionPrice  > 100 or self.data.close[0] - self.executionPrice  < -200):#and self.avgClose > self.dnBand:
                 print("self.exit at  -> "+ self.data.close[0].__str__())
                 self.close()
                 self.MarketPosition =0
            
     