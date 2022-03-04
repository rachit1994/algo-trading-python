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

    def next(self):
        
        if(self.MarketPosition == 0) : 
            

            if self.rocCalc > 0 :
                print("self.buy at -> "+ self.data.close.__str__())
                self.buy()
                self.MarketPosition=1
            elif self.rocCalc < 0 :
                 print("self.sell at -> "+ self.data.close.__str__())
                 self.sell()
                 self.MarketPosition=-1

        else:
            self.liqDays = self.liqDays - 1;
            avgClose= bt.ind.Average(self.data.close,period=self.liqDays)
            if self.MarketPosition == 1 and [avgClose < self.upBand]:
                 print("self.exit at  -> "+ self.data.close.__str__())
                 self.sell()
                 self.MarketPosition =0
            elif self.MarketPosition == -1 and [avgClose > self.dnBand] :
                 print("self.exit at  -> "+ self.data.close.__str__())
                 self.buy()
                 self.MarketPosition =0
            
     