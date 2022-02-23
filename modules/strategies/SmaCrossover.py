# Create a subclass of Strategy to define the indicators and logic
import modules.backtest as btest

class SmaCrossover(btest.bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30   # period for the slow moving average
    )

    alias = ("SMACROSSOVER", "SmaCrossover")

    def __init__(self):
        sma1 = btest.bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = btest.bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = btest.bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position