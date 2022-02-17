class Candle:
    def __init__(self,dataframe):
        self.date = dataframe.TIME
        self.open = dataframe.Open
        self.high = dataframe.High
        self.low = dataframe.Low
        self.close = dataframe.CLOSE
        self.volume = dataframe.VOLUME
        self.symbol = dataframe.SYMBOL
        self.isup = self.close >= self.open
        self.isdown = self.close <= self.open

    def __repr__(self):
        return f"(d={self.date},\no={self.open},\nh={self.high},\nl={self.low},\nc={self.close},\nv={self.volume},\nup={self.isup},\ndn={self.isdown})"