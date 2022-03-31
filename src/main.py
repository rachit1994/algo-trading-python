import modules.backtest  as btest
import modules.strategies as strategy
import pandas as pd
from lib.utils.format_analyzer_output import *
# import yfinance as yf

symbol=""
from_date = "2021-01-01 09:00:00+05:30"
to_date = "2021-12-31 16:00:00+05:30"
timeframe = "15minute"
#Variable for our starting cash
startcash = 100000
strategyName="BollingerBandidt"
# symbols = ["ADANIPORTS","ASIANPAINT","AXISBANK","BAJAJAUTO","BAJAJFINSV","BAJFINANCE"]
symbols = ["ADANIPORTS","ASIANPAINT"]
#symbols = pd.read_csv('temp/SYMBOLS.csv', index_col=0)
# print (symbols)
#for symbol in symbols.index:
for symbol in symbols:
    print("Running strategy for symbol -> "+symbol)
    cerebro = btest.bt.Cerebro()  # create a "Cerebro" engine instance
    
    # Create a data feed
    dataframe = btest.feeds.pull("STOCK",symbol, timeframe, fromDate=from_date, toDate=to_date)

    #dataframe = btest.feeds.pull("STOCK",symbol, "15minute") # Use this for running backtest on full dataset

    data = btest.bt.feeds.PandasData(dataname=dataframe.df)

    cerebro.adddata(data)  # Add the data feed

    #cerebro.addstrategy(strategy.SMACROSSOVER)  # Add the trading strategy

    cerebro.addstrategy(strategy.BollBand) 

    # Set desired cash start
    cerebro.broker.setcash(startcash)
    # Add analyzers 
    cerebro.addanalyzer(btest.analyzers.TradeAnalyzer, _name="ta")
    cerebro.addanalyzer(btest.analyzers.tradelist, _name="tradelist")

    strategies = cerebro.run(tradehistory=True)


    firstStrat = strategies[0]

    # print the analyzers
    printTradeAnalysis(firstStrat.analyzers.ta.get_analysis(),"BollingerBandidt",symbol, from_date.split(" ")[0], to_date.split(" ")[0])
    export_trade_list(firstStrat.analyzers.getbyname("tradelist").get_analysis(),"BollingerBandit",symbol, from_date.split(" ")[0], to_date.split(" ")[0])
   
    #Get final portfolio Value
    portvalue = cerebro.broker.getvalue()

    #Print out the final result
    print('Final Portfolio Value : ${}'.format(portvalue))

export_trade_summary(strategyName,from_date.split(" ")[0], to_date.split(" ")[0])

#Finally plot the end results
#cerebro.plot()

#cerebro.plot(style='candlestick')

# cerebro.addanalyzer(btest.analyzers.tradelist, _name="tradelist")
# #cerebro.run() 
# strat = cerebro.run(tradehistory=True)
# # Save trade list.
# trade_list = strat[0].analyzers.getbyname("tradelist").get_analysis()
# df = pd.DataFrame(trade_list)
# df = df.drop(['pnl', 'pnl/bar', 'ticker'], axis=1)
# df.to_csv("temp/trade_list_1.csv")

#cerebro.plot()  # and plot it with a single command