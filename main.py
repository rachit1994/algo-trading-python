import modules.backtest  as btest
import pandas as pd
# import yfinance as yf

cerebro = btest.bt.Cerebro()  # create a "Cerebro" engine instance

# Create a data feed

dataframe = btest.feeds.pull("STOCK", "TCS", "15minute")
data = btest.bt.feeds.PandasData(dataname=dataframe.df)

cerebro.adddata(data)  # Add the data feed
cerebro.addstrategy(btest.strategy.SMACROSSOVER)  # Add the trading strategy

cerebro.addanalyzer(btest.analyzers.tradelist, _name="tradelist")
#cerebro.run() 
strat = cerebro.run(tradehistory=True)
# Save trade list.
trade_list = strat[0].analyzers.getbyname("tradelist").get_analysis()
df = pd.DataFrame(trade_list)
df = df.drop(['pnl', 'pnl/bar', 'ticker'], axis=1)
df.to_csv("temp/trade_list_1.csv")

#cerebro.plot()  # and plot it with a single command