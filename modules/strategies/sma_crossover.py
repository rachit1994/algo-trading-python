from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


import backtest.indicators as indicators


class MA_CrossOver():
    '''This is a long-only strategy which operates on a moving average cross

    Note:
      - Although the default

    Buy Logic:
      - No position is open on the data

      - The ``fast`` moving averagecrosses over the ``slow`` strategy to the
        upside.

    Sell Logic:
      - A position exists on the data

      - The ``fast`` moving average crosses over the ``slow`` strategy to the
        downside

    Order Execution Type:
      - Market

    '''
   
    fast = 10
    slow = 30
    data = None

    def __init__(self, data):
        print("inside init of MA_CrossOver")
        self.data=data

    def execute(self):
        sma_fast = indicators.SimpleMovingAverage(self.data,self.fast).apply()
        print(sma_fast)
        
        #sma_slow = self.p._movav(period=self.p.slow)
        #print(sma_fast)

        #self.buysig = btind.CrossOver(sma_fast, sma_slow)

    # def next(self):
    #     if self.position.size:
    #         if self.buysig < 0:
    #             self.sell()

    #     elif self.buysig > 0:
    #         self.buy()
