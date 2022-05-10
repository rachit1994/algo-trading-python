import pandas as pd
import glob
import os
import datetime

def printTradeAnalysis(analyzer, strategyName, symbol, from_date, to_date):
    '''
    Function to print the Technical Analysis results in a nice format.
    '''
    # Get the results we are interested in
    total_open = analyzer.total.open
    total_closed = analyzer.total.closed
    total_won = analyzer.won.total
    total_lost = analyzer.lost.total
    win_streak = analyzer.streak.won.longest
    lose_streak = analyzer.streak.lost.longest
    pnl_net = round(analyzer.pnl.net.total, 2)
    strike_rate = round((total_won / total_closed) * 100, 2)
    # Designate the rows
    h1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost']
    h2 = ['Strike Rate', 'Win Streak', 'Losing Streak', 'PnL Net']
    r1 = [total_open, total_closed, total_won, total_lost]
    r2 = [strike_rate, win_streak, lose_streak, pnl_net]
    c1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost',
          'Strike Rate', 'Win Streak', 'Losing Streak', 'PnL Net']
    d1 = [total_open, total_closed, total_won, total_lost,
          strike_rate, win_streak, lose_streak, pnl_net]
    # Check which set of headers is the longest.
    if len(h1) > len(h2):
        header_length = len(h1)
    else:
        header_length = len(h2)
    # Print the rows
    print_list = [h1, r1, h2, r2]
    row_format = "{:<15}" * (header_length + 1)
    print("Trade Analysis Results for Symbol : "+symbol)
    for row in print_list:
        print(row_format.format('', *row))

    export_csv(c1, d1, strategyName, symbol, from_date, to_date)


def export_csv(c1, d1, strategyName, symbol, from_date, to_date):
    path = "temp/"+strategyName
    try:
        os.mkdir(path)
    except FileExistsError as e:
        print("Folder already exists")
    df1 = pd.DataFrame([d1], index=[0], columns=c1)
    # df1["Symbol"]=symbol
    df1.insert(0, 'Symbol', symbol)
    # print(df1)
    df1.to_csv("temp/"+strategyName+"/Trade_Summary_"+symbol +
               "_"+from_date+"_to_"+to_date+".csv", index=False)


def export_trade_list(trade_list, strategyName, symbol, from_date, to_date):
    df = pd.DataFrame(trade_list)
    df.insert(0, 'formatteddatein', pd.to_datetime(df['datein']))
    path = "temp/"+strategyName
    df1 = df.groupby(
        [df.formatteddatein.dt.strftime('%b %Y')]
    )['pnl%'].mean().reset_index(name='Monthly Average PnL')
    #print(df1)
    totalavgpnlpercent = round(df1['Monthly Average PnL'].mean(), 3)
    quantity = 30
    df['BROKERAGE'] = df.apply(lambda x: brokerageCalculator(x['pricein'],x['priceout'],quantity), axis=1)
    
    # print(round(totalavgpnlpercent,5))
    df = df.drop(['pnl/bar', 'ticker', 'formatteddatein'], axis=1)
    # print(df)

    if totalavgpnlpercent <= 0:
        df.to_csv(path+"/Trade_List_"+symbol+"_L_"+abs(totalavgpnlpercent).__str__() +
                  "_"+from_date+"_to_"+to_date+".csv", index=False)
    else:
        df.to_csv(path+"/Trade_List_"+symbol+"_P_"+abs(totalavgpnlpercent).__str__() +
                  "_"+from_date+"_to_"+to_date+".csv", index=False)

def export_trade_summary(strategyName, from_date, to_date):
    # setting the path for joining multiple files
    files = os.path.join("temp/"+strategyName, "Trade_Summary*.csv")

    # list of merged files returned
    files = glob.glob(files)

    print("Resultant CSV after joining all CSV files at a particular location...")

    # joining files with concat and read_csv
    df = pd.concat(map(pd.read_csv, files), ignore_index=True)
    # print(df)
    df.to_csv("temp/"+strategyName+"/Trade_Summary_" +
              from_date+"_to_"+to_date+".csv", index=False)


def brokerageCalculator(bp,sp,qty):
                   
    # bp = float(request['buy_price'] if 'buy_price' in request else 0)
    # sp = float(request['sell_price'] if 'sell_price' in request else 0)
    # qty = float(request['quantity'])
    brokerage = 20 if bp is None or sp is None else 40
    turnover = ((bp + sp) * qty)
    stt_total = sp * qty * 0.0005
    etc = (0.0005 * turnover)
    stax = (0.18 * (brokerage + etc))
    sebi_charges = turnover * 0.0000005
    stamp_charges = bp * qty * 0.00003
    return brokerage + stt_total + etc + stax + sebi_charges + stamp_charges


# export_trade_summary("BollingerBandit","2020-01-01","2022-01-01")
