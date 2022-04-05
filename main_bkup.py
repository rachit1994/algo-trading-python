import modules.backtest as btest
import pandas as pd
from modules.strategies.SmaCrossover import SmaCrossover
from constants.common import CSV_PATH
import datetime
# import yfinance as yf
import argparse
import pandas

cerebro = btest.bt.Cerebro()  # create a "Cerebro" engine instance

# Create a data feed
skiprows = 0
header = 0

dataframe = pandas.read_csv(CSV_PATH+"ADANIPORTS.csv",
                            skiprows=skiprows,
                            header=header,
                            parse_dates=True,
                            index_col=0)

# dataframe = btest.feeds.pull("STOCK", "TCS", "15minute")
data = btest.bt.feeds.PandasData(dataname=dataframe)

cerebro.adddata(data)  # Add the data feed
cerebro.addstrategy(SmaCrossover)  # Add the trading strategy

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.addanalyzer(btest.analyzers.tradelist, _name="tradelist")
#cerebro.run() 
strat = cerebro.run(tradehistory=True)

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Save trade list.
trade_list = strat[0].analyzers.getbyname("tradelist").get_analysis()
df = pd.DataFrame(trade_list)
df = df.drop(['pnl', 'pnl/bar', 'ticker'], axis=1)
df.to_csv("temp/trade_list_1.csv")

#cerebro.plot()  # and plot it with a single command