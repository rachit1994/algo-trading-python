from backtrader import Strategy
from modules.backtest.indicators.fibonacci import Fibonn as FIB


class Abcd(Strategy):

    alias = ("ABCD", "Abcd")

    def __init__(self):
        #print(self.data)
        self.candle = self.data
        self.candle["is_up"]: [self.candle.close >= self.candle.open]
        self.candle["isdown"]: [self.candle.close < self.candle.open]
        use_alt_timeframe=True
        current_time_frame="5minute"
        alt_time_frame="60minute"
        self.interval = current_time_frame
        self.alt_time_frame = alt_time_frame
        self.use_alt_timeframe = use_alt_timeframe
        self.fibonums = None
        self.dataframe = {
            "TIME": [self.candle.datetime],
            "Open": [self.candle.open],
            "High": [self.candle.high],
            "Low": [self.candle.low],
            "CLOSE": [self.candle.close],
            "isup": [self.candle.close >= self.candle.open],
            "isdown": [self.candle.close < self.candle.open],
            "sz": [],
            "long": [],
            "close_long": [],
            "short": [],
            "close_short": []
        }
        

    def next(self):
        self.fib_ind = FIB(period=1,candle=self.dataframe,interval=self.interval,alt_time_frame=self.alt_time_frame,use_alt_timeframe=self.use_alt_timeframe)
        
        #print(self.dataframe)
        fib_ind = self.fib_ind
        print("###############################")
        #self.is_bat = fib_ind.is_bat(1)
        if not self.position:  # not in the market
            if  self.buy_long(fib_ind):  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.sell_long(fib_ind):  # in the market & cross to the downside
            self.close()  # close long position
    
    def buy_long(self,fib_ind):
        buy_patterns_00 = fib_ind.is_abcd(1) or fib_ind.is_bat(1) or fib_ind.is_alt_bat(1) or fib_ind.is_butterfly(1) \
                      or fib_ind.is_gartley(1) or fib_ind.is_crab(1) or fib_ind.is_shark(1) or fib_ind.is5o(1) \
                      or fib_ind.is_wolf(1) or fib_ind.is_hns(1) or fib_ind.is_con_tria(1) or fib_ind.is_exp_tria(1)
        buy_patterns_01 = fib_ind.is_anti_bat(1) or fib_ind.is_anti_butterfly(1) or fib_ind.is_anti_gartley(1)\
                      or fib_ind.is_anti_crab(1) or fib_ind.is_anti_shark(1)
        return True if (buy_patterns_00 or buy_patterns_01 and self.candle.close <= fib_ind.f_last_fib(0.236, fib_ind.fib_range())) else False
    
    def sell_long(self,fib_ind):
            target01_buy_close = self.candle.high >= fib_ind.f_last_fib(0.618, fib_ind.fib_range()) or self.candle.low <= fib_ind.f_last_fib(-0.236, fib_ind.fib_range())
            target02_buy_close = self.candle.high >= fib_ind.f_last_fib(1.618, fib_ind.fib_range()) or self.candle.low <= fib_ind.f_last_fib(-0.236, fib_ind.fib_range())
            return True if (target01_buy_close or target02_buy_close) else False
    
  
    
   
