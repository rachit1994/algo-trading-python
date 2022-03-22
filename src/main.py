import modules.backtest  as btest
import modules.strategies as strategy
import pandas as pd
from lib.utils.format_analyzer_output import *
# import yfinance as yf

cerebro = btest.bt.Cerebro()  # create a "Cerebro" engine instance
#Variable for our starting cash
startcash = 100000

# Create a data feed

dataframe = btest.feeds.pull("STOCK","TCS", "15minute")
data = btest.bt.feeds.PandasData(dataname=dataframe.df)

cerebro.adddata(data)  # Add the data feed

#cerebro.addstrategy(strategy.SMACROSSOVER)  # Add the trading strategy

cerebro.addstrategy(strategy.BollBand) 

# Set desired cash start
cerebro.broker.setcash(startcash)
# Add analyzers 
cerebro.addanalyzer(btest.analyzers.TradeAnalyzer, _name="ta")

strategies = cerebro.run()


firstStrat = strategies[0]

# print the analyzers
printTradeAnalysis(firstStrat.analyzers.ta.get_analysis())

#Get final portfolio Value
portvalue = cerebro.broker.getvalue()

#Print out the final result
print('Final Portfolio Value: ${}'.format(portvalue))
#Finally plot the end results
cerebro.plot(style='candlestick')

# cerebro.addanalyzer(btest.analyzers.tradelist, _name="tradelist")
# #cerebro.run() 
# strat = cerebro.run(tradehistory=True)
# # Save trade list.
# trade_list = strat[0].analyzers.getbyname("tradelist").get_analysis()
# df = pd.DataFrame(trade_list)
# df = df.drop(['pnl', 'pnl/bar', 'ticker'], axis=1)
# df.to_csv("temp/trade_list_1.csv")

#cerebro.plot()  # and plot it with a single command