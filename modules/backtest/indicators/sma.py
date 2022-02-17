

class SimpleMovingAverage():
    alias = ('SMA', 'SimpleMovingAverage',)
    data = None
    period = None
    def __init__(self , data, period):
      self.data=data
      self.period=period


    def apply(self):
        self.data.df['pandas_SMA_3'] = self.data.df.iloc[:,1].rolling(window=self.period).mean()
        return self