intraday=False
target=1
sl=4
symbol=""

from_date = "2021-12-01 09:00:00+05:30"
to_date = "2021-12-31 16:00:00+05:30"

# from_date = "2022-05-01"
# to_date = "2022-06-06"

#timeframe = "15minute"
timeframe = "minute"
#Variable for our starting cash
startcash = 100000
portfolioutilizationpercentage = 80
#strategyName="BollingerBandit"
strategyName="KingKeltner"
#strategyName="VWAPCrossover"
# symbols = ["ADANIPORTS","ASIANPAINT","AXISBANK","BAJAJAUTO","BAJAJFINSV","BAJFINANCE"]
symbols = ["ICICIBANK"]
#symbols = ["10422786"] # BANKNIFTY2260935300PE
#symbols = pd.read_csv('temp/SYMBOLS.csv', index_col=0)
# print (symbols)