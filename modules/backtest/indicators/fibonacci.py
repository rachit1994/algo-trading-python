from backtrader import Indicator
import backtrader as bt
from lib.utils.convert_candle_by_time import get_grouped_candles, alttf_to_tf_factor

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

    

class Fibonn(Indicator):
    alias = ('FIB', 'Fibonn',)
    data = None
    period = None

    lines = ('non_none_szs',)
    #params = (dict(period=1, safediv=True))

    plotlines = dict(
                non_none_szs=dict(_name='CP', marker='v', markersize=6.0, ls='', color='pink', _skipnan=True),
               

                )

    plotinfo = dict(subplot=True)

    def __init__(self,period,candle,interval,alt_time_frame,use_alt_timeframe):
    #   self.data=data
      self.candle=candle
      self.period=period
      self.interval=interval
      self.alt_time_frame=alt_time_frame
      self.use_alt_timeframe=use_alt_timeframe
      self.setup()
      # Before super to ensure mixins (right-hand side in subclassing)
      # can see the assignment operation and operate on the line
      
      #self.lines.is_bat=self.is_bat(1)
      self.lines.non_none_szs =  self.non_none_sz
    #   for i in range(0, len(self.non_none_sz)):
    #     self.lines.non_none_szs[0].append(bt.Max(0.0, self.non_none_sz[i]))
      #self.lines.non_none_szs = bt.Max(0.0, self.non_none_sz) 

      super(Fibonn, self).__init__()

    def setup(self):
       
        sz=self.calculate_sz()
        non_none_sz = [sz[i] for i in range(0,len(sz)) if sz[i]]
        self.non_none_sz=non_none_sz
        if len(non_none_sz) >= 5:
            self.fibonums = FiboFactors(*non_none_sz[-5:])
            self.lines.non_none_szs =  self.non_none_sz

    # def apply(self):
    #    # self.data.df['pandas_SMA_3'] = self.data.df.iloc[:,1].rolling(window=self.period).mean()
    #     return self

    def calculate_sz(self):
        #alt_factor = alttf_to_tf_factor(interval=self.interval, altinterval=self.alt_time_frame)
        #grouped_candle = get_grouped_candles(self.candle, self.interval, self.alt_time_frame)
        alt_factor=1
        grouped_candle=self.candle
        len_grouped_candle=len(self.candle.get('TIME')[0].array)
        sz = [None]*(alt_factor)
        for i in range(1, len_grouped_candle):
            nextsz = None
            if  self.candle["isup"][0][i-1]==1.0 and self.candle["isdown"][0][i]==1.0 :
                nextsz = max(grouped_candle["High"][0][i], grouped_candle["High"][0][i-1])
            elif  self.candle["isdown"][0][i-1]==1.0 and self.candle["isup"][0][i]==1.0:
                nextsz = min(grouped_candle["Low"][0][i], grouped_candle["Low"][0][i-1])
            else :
                nextsz = None
            
            sz += [nextsz] + [None]*(alt_factor-1)
        sz += [None]*(alt_factor-len(sz))
        return sz
    
    def is_bat(self, _mode):
        _xab = self.fibonums.xab >= 0.382 and self.fibonums.xab <= 0.5
        _abc = self.fibonums.abc >= 0.382 and self.fibonums.abc <= 0.886
        _bcd = self.fibonums.bcd >= 1.618 and self.fibonums.bcd <= 2.618
        _xad = self.fibonums.xad <= 0.618 and self.fibonums.xad <= 1.000  # 0.886
        _is_bat = _xab and _abc and _bcd and _xad and (self.fibonums.d < self.fibonums.c if _mode == 1 else self.fibonums.d > self.fibonums.c)
        return _is_bat


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