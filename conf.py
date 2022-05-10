intraday=True
target=0.5
sl=1
symbol=""
from_date = "2021-12-01 09:00:00+05:30"
to_date = "2021-12-31 16:00:00+05:30"
timeframe = "15minute"
#timeframe = "minute"
#Variable for our starting cash
startcash = 100000
portfolioutilizationpercentage = 80
strategyName="BollingerBandit"
# symbols = ["ADANIPORTS","ASIANPAINT","AXISBANK","BAJAJAUTO","BAJAJFINSV","BAJFINANCE"]
symbols = ["ICICIBANK"]
#symbols = pd.read_csv('temp/SYMBOLS.csv', index_col=0)
# print (symbols)