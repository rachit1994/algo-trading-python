from lib.convert_candle_by_time import get_grouped_candles, alttf_to_tf_factor
from lib.utils.candle import Candle
from constants.common import TEMP_CSV_PATH

class FiboFactors:
    def __init__(self,x,a,b,c,d):
        self.x = x
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.xab = (abs(b - a) / max(0.01, abs(x - a)))
        self.xad = (abs(a - d) / max(0.01, abs(x - a)))
        self.abc = (abs(b - c) / max(0.01, abs(a - b)))
        self.bcd = (abs(c - d) / max(0.01, abs(b - c)))

sz = []

class Abcd():
    def __init__(self, df):
        self.candle = df
        use_alt_timeframe=True
        current_time_frame="5minute"
        alt_time_frame="60minute"
        self.interval = current_time_frame
        self.alt_time_frame = alt_time_frame
        self.use_alt_timeframe = use_alt_timeframe
        self.fibonums = None
        self.dataframe = {
            "TIME": [self.candle.date],
            "Open": [self.candle.open],
            "High": [self.candle.high],
            "Low": [self.candle.low],
            "CLOSE": [self.candle.close],
            "direction": [],
            "sz": [],
            "long": [],
            "close_long": [],
            "short": [],
            "close_short": []
        }
    
    def get_directon(self):
        direction = 1 if self.candle.isup else -1
        self.dataframe["direction"].append(direction)
        return direction
    
    def calculate_sz(self):
        alt_factor = alttf_to_tf_factor(interval=self.interval, altinterval=self.alt_time_frame)
        grouped_candle = get_grouped_candles(self.candle, self.interval, self.alt_time_frame)
        directions = self.get_directon()
        
        sz = [None]*(alt_factor)
        for i in range(1, len(grouped_candle)):
            nextsz = None
            if self.candle[i - 1].isup and self.candle[i].isdown and directions[i - 1] != -1:
                nextsz = max(grouped_candle[i].high, grouped_candle[i - 1].high)
            elif self.candle[i - 1].isdown and self.candle[i].isup and directions[i - 1] != 1:
                nextsz = min(grouped_candle[i].low, grouped_candle[i - 1].low)
            sz += [nextsz] + [None]*(alt_factor-1)
        sz += [None]*(len(self.candle)-len(sz))
        return sz
    
    def is_bat(self, _mode):
        _xab = self.fibonums.xab >= 0.382 and self.fibonums.xab <= 0.5
        _abc = self.fibonums.abc >= 0.382 and self.fibonums.abc <= 0.886
        _bcd = self.fibonums.bcd >= 1.618 and self.fibonums.bcd <= 2.618
        _xad = self.fibonums.xad <= 0.618 and self.fibonums.xad <= 1.000  # 0.886
        return _xab and _abc and _bcd and _xad and (self.fibonums.d < self.fibonums.c if _mode == 1 else self.fibonums.d > self.fibonums.c)


    def is_anti_bat(self, _mode):
        _xab = self.fibonums.xab >= 0.500 and self.fibonums.xab <= 0.886  # 0.618
        _abc = self.fibonums.abc >= 1.000 and self.fibonums.abc <= 2.618  # 1.13 --> 2.618
        _bcd = self.fibonums.bcd >= 1.618 and self.fibonums.bcd <= 2.618  # 2.0  --> 2.618
        _xad = self.fibonums.xad >= 0.886 and self.fibonums.xad <= 1.000  # 1.13
        return _xab and _abc and _bcd and _xad and (self.fibonums.d < self.fibonums.c if _mode == 1 else self.fibonums.d > self.fibonums.c)


    def is_alt_bat(self, _mode):
        _xab = self.fibonums.xab <= 0.382
        _abc = self.fibonums.abc >= 0.382 and self.fibonums.abc <= 0.886
        _bcd = self.fibonums.bcd >= 2.0 and self.fibonums.bcd <= 3.618
        _xad = self.fibonums.xad <= 1.13
        return _xab and _abc and _bcd and _xad and (self.fibonums.d < self.fibonums.c if _mode == 1 else self.fibonums.d > self.fibonums.c)


    def is_butterfly(self, _mode):
        _xab = self.fibonums.xab <= 0.786
        _abc = self.fibonums.abc >= 0.382 and self.fibonums.abc <= 0.886
        _bcd = self.fibonums.bcd >= 1.618 and self.fibonums.bcd <= 2.618
        _xad = self.fibonums.xad >= 1.27 and self.fibonums.xad <= 1.618
        return _xab and _abc and _bcd and _xad and (self.fibonums.d < self.fibonums.c if _mode == 1 else self.fibonums.d > self.fibonums.c)


    def is_anti_butterfly(self, _mode):
        _xab = self.fibonums.xab >= 0.236 and self.fibonums.xab <= 0.886  # 0.382 - 0.618
        _abc = self.fibonums.abc >= 1.130 and self.fibonums.abc <= 2.618  # 1.130 - 2.618
        _bcd = self.fibonums.bcd >= 1.000 and self.fibonums.bcd <= 1.382  # 1.27
        _xad = self.fibonums.xad >= 0.500 and self.fibonums.xad <= 0.886  # 0.618 - 0.786
        return _xab and _abc and _bcd and _xad and (self.fibonums.d < self.fibonums.c if _mode == 1 else self.fibonums.d > self.fibonums.c)


    def is_abcd(self, _mode):
        _abc = self.fibonums.abc >= 0.382 and self.fibonums.abc <= 0.886
        _bcd = self.fibonums.bcd >= 1.13 and self.fibonums.bcd <= 2.618
        return _abc and _bcd and (self.fibonums.d < self.fibonums.c if _mode == 1 else self.fibonums.d > self.fibonums.c)


    def is_gartley(self, _mode):
        _xab = self.fibonums.xab >= 0.5 and self.fibonums.xab <= 0.618  # 0.618
        _abc = self.fibonums.abc >= 0.382 and self.fibonums.abc <= 0.886
        _bcd = self.fibonums.bcd >= 1.13 and self.fibonums.bcd <= 2.618
        _xad = self.fibonums.xad >= 0.75 and self.fibonums.xad <= 0.875  # 0.786
        return _xab and _abc and _bcd and _xad and (self.fibonums.d < self.fibonums.c if _mode == 1 else self.fibonums.d > self.fibonums.c)


    def is_anti_gartley(self, _mode):
        _xab = self.fibonums.xab >= 0.500 and self.fibonums.xab <= 0.886  # 0.618 -> 0.786
        _abc = self.fibonums.abc >= 1.000 and self.fibonums.abc <= 2.618  # 1.130 -> 2.618
        _bcd = self.fibonums.bcd >= 1.500 and self.fibonums.bcd <= 5.000  # 1.618
        _xad = self.fibonums.xad >= 1.000 and self.fibonums.xad <= 5.000  # 1.272
        return _xab and _abc and _bcd and _xad and (self.fibonums.d < self.fibonums.c if _mode == 1 else self.fibonums.d > self.fibonums.c)


    def is_crab(self, _mode):
        _xab = self.fibonums.xab >= 0.500 and self.fibonums.xab <= 0.875  # 0.886
        _abc = self.fibonums.abc >= 0.382 and self.fibonums.abc <= 0.886
        _bcd = self.fibonums.bcd >= 2.000 and self.fibonums.bcd <= 5.000  # 3.618
        _xad = self.fibonums.xad >= 1.382 and self.fibonums.xad <= 5.000  # 1.618
        return _xab and _abc and _bcd and _xad and (self.fibonums.d < self.fibonums.c if _mode == 1 else self.fibonums.d > self.fibonums.c)


    def is_anti_crab(self, _mode):
        _xab = self.fibonums.xab >= 0.250 and self.fibonums.xab <= 0.500  # 0.276 -> 0.446
        _abc = self.fibonums.abc >= 1.130 and self.fibonums.abc <= 2.618  # 1.130 -> 2.618
        _bcd = self.fibonums.bcd >= 1.618 and self.fibonums.bcd <= 2.618  # 1.618 -> 2.618
        _xad = self.fibonums.xad >= 0.500 and self.fibonums.xad <= 0.750  # 0.618
        return _xab and _abc and _bcd and _xad and (self.fibonums.d < self.fibonums.c if _mode == 1 else self.fibonums.d > self.fibonums.c)


    def is_shark(self, _mode):
        _xab = self.fibonums.xab >= 0.500 and self.fibonums.xab <= 0.875  # 0.5 --> 0.886
        _abc = self.fibonums.abc >= 1.130 and self.fibonums.abc <= 1.618  #
        _bcd = self.fibonums.bcd >= 1.270 and self.fibonums.bcd <= 2.240  #
        _xad = self.fibonums.xad >= 0.886 and self.fibonums.xad <= 1.130  # 0.886 --> 1.13
        return _xab and _abc and _bcd and _xad and (self.fibonums.d < self.fibonums.c if _mode == 1 else self.fibonums.d > self.fibonums.c)


    def is_anti_shark(self, _mode):
        _xab = self.fibonums.xab >= 0.382 and self.fibonums.xab <= 0.875  # 0.446 --> 0.618
        _abc = self.fibonums.abc >= 0.500 and self.fibonums.abc <= 1.000  # 0.618 --> 0.886
        _bcd = self.fibonums.bcd >= 1.250 and self.fibonums.bcd <= 2.618  # 1.618 --> 2.618
        _xad = self.fibonums.xad >= 0.500 and self.fibonums.xad <= 1.250  # 1.130 --> 1.130
        return _xab and _abc and _bcd and _xad and (self.fibonums.d < self.fibonums.c if _mode == 1 else self.fibonums.d > self.fibonums.c)


    def is5o(self, _mode):
        _xab = self.fibonums.xab >= 1.13 and self.fibonums.xab <= 1.618
        _abc = self.fibonums.abc >= 1.618 and self.fibonums.abc <= 2.24
        _bcd = self.fibonums.bcd >= 0.5 and self.fibonums.bcd <= 0.625  # 0.5
        _xad = self.fibonums.xad >= 0.0 and self.fibonums.xad <= 0.236  # negative?
        return _xab and _abc and _bcd and _xad and (self.fibonums.d < self.fibonums.c if _mode == 1 else self.fibonums.d > self.fibonums.c)


    def is_wolf(self, _mode):
        _xab = self.fibonums.xab >= 1.27 and self.fibonums.xab <= 1.618
        _abc = self.fibonums.abc >= 0 and self.fibonums.abc <= 5
        _bcd = self.fibonums.bcd >= 1.27 and self.fibonums.bcd <= 1.618
        _xad = self.fibonums.xad >= 0.0 and self.fibonums.xad <= 5
        return _xab and _abc and _bcd and _xad and (self.fibonums.d < self.fibonums.c if _mode == 1 else self.fibonums.d > self.fibonums.c)


    def is_hns(self, _mode):
        _xab = self.fibonums.xab >= 2.0 and self.fibonums.xab <= 10
        _abc = self.fibonums.abc >= 0.90 and self.fibonums.abc <= 1.1
        _bcd = self.fibonums.bcd >= 0.236 and self.fibonums.bcd <= 0.88
        _xad = self.fibonums.xad >= 0.90 and self.fibonums.xad <= 1.1
        return _xab and _abc and _bcd and _xad and (self.fibonums.d < self.fibonums.c if _mode == 1 else self.fibonums.d > self.fibonums.c)


    def is_con_tria(self, _mode):
        _xab = self.fibonums.xab >= 0.382 and self.fibonums.xab <= 0.618
        _abc = self.fibonums.abc >= 0.382 and self.fibonums.abc <= 0.618
        _bcd = self.fibonums.bcd >= 0.382 and self.fibonums.bcd <= 0.618
        _xad = self.fibonums.xad >= 0.236 and self.fibonums.xad <= 0.764
        return _xab and _abc and _bcd and _xad and (self.fibonums.d < self.fibonums.c if _mode == 1 else self.fibonums.d > self.fibonums.c)


    def is_exp_tria(self, _mode):
        _xab = self.fibonums.xab >= 1.236 and self.fibonums.xab <= 1.618
        _abc = self.fibonums.abc >= 1.000 and self.fibonums.abc <= 1.618
        _bcd = self.fibonums.bcd >= 1.236 and self.fibonums.bcd <= 2.000
        _xad = self.fibonums.xad >= 2.000 and self.fibonums.xad <= 2.236
        return _xab and _abc and _bcd and _xad and (self.fibonums.d < self.fibonums.c if _mode == 1 else self.fibonums.d > self.fibonums.c)


    def f_last_fib(self, _rate, fib_range):
        return self.fibonums.d - (fib_range * _rate) if self.fibonums.d > self.fibonums.c else self.fibonums.d + (fib_range * _rate)
    
    def fib_range(self):
        return abs(self.fibonums.d - self.fibonums.c)
    
    def long(self):
        buy_patterns_00 = self.is_abcd(1) or self.is_bat(1) or self.is_alt_bat(1) or self.is_butterfly(1) \
                      or self.is_gartley(1) or self.is_crab(1) or self.is_shark(1) or self.is5o(1) \
                      or self.is_wolf(1) or self.is_hns(1) or self.is_con_tria(1) or self.is_exp_tria(1)
        buy_patterns_01 = self.is_anti_bat(1) or self.is_anti_butterfly(1) or self.is_anti_gartley(1)\
                      or self.is_anti_crab(1) or self.is_anti_shark(1)
        return True if (buy_patterns_00 or buy_patterns_01 and self.candle.close <= self.f_last_fib(0.236, self.fib_range())) else False
    
    def short(self):
        sel_patterns_00 = self.is_abcd(-1) or self.is_bat(-1) or self.is_alt_bat(-1) or self.is_butterfly(-1) \
                      or self.is_gartley(-1) or self.is_crab(-1) or self.is_shark(-1) or self.is5o(-1) \
                      or self.is_wolf(-1) or self.is_hns(-1)  or self.is_con_tria(-1) or self.is_exp_tria(-1)
        sel_patterns_01 = self.is_anti_bat(-1) or self.is_anti_butterfly(-1) or self.is_anti_gartley(-1)\
                      or self.is_anti_crab(-1) or self.is_anti_shark(-1)
        return True if (sel_patterns_00 or sel_patterns_01 and self.candle.close >= self.f_last_fib(0.236, self.fib_range())) else False
    
    def close_buy(self):
        target01_buy_close = self.candle.high >= self.f_last_fib(0.618, self.fib_range()) or self.candle.low <= self.f_last_fib(-0.236, self.fib_range())
        target02_buy_close = self.candle.high >= self.f_last_fib(1.618, self.fib_range()) or self.candle.low <= self.f_last_fib(-0.236, self.fib_range())
        return True if (target01_buy_close or target02_buy_close) else False
    
    def close_sell(self):
        target01_sel_close = self.candle.low <= self.f_last_fib(0.618, self.fib_range()) or self.candle.high >= self.f_last_fib(-0.236, self.fib_range())
        target02_sel_close = self.candle.low <= self.f_last_fib(1.618, self.fib_range()) or self.candle.high >= self.f_last_fib(-0.236, self.fib_range())
        return target01_sel_close or target02_sel_close
    
    def setup(self):
        sz.append(self.calculate_sz())
        non_none_sz = [i for i in sz if i]
        if len(non_none_sz) >= 5:
            self.fibonums = FiboFactors(non_none_sz[-5:])
