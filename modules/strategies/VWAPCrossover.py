# Create a subclass of Strategy to define the indicators and logic
import modules.backtest as btest

class VWAPCrossover(btest.bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        size=30
    )

    alias = ("VWAPCROSS", "VWAPCrossover")

    def __init__(self):
        self.vwap = btest.indicators.VWAP(period=self.p.size) 
        print ("Moving to next step...")

    def prenext(self):
        print("I am here")
        #print('prenext:: current period:', len(self))

    def next(self):
        print("I am in next")
        if not self.position:  # not in the market
            if self.vwap > self.data.open and self.vwap < self.data.close:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.vwap < self.data.open and self.vwap > self.data.close:  # in the market & cross to the downside
            self.close()  # close long position