import pandas as pd

def printTradeAnalysis(analyzer, strategyName,symbol,from_date, to_date):
    '''
    Function to print the Technical Analysis results in a nice format.
    '''
    #Get the results we are interested in
    total_open = analyzer.total.open
    total_closed = analyzer.total.closed
    total_won = analyzer.won.total
    total_lost = analyzer.lost.total
    win_streak = analyzer.streak.won.longest
    lose_streak = analyzer.streak.lost.longest
    pnl_net = round(analyzer.pnl.net.total,2)
    strike_rate = (total_won / total_closed) * 100
    #Designate the rows
    h1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost']
    h2 = ['Strike Rate','Win Streak', 'Losing Streak', 'PnL Net']
    r1 = [total_open, total_closed,total_won,total_lost]
    r2 = [strike_rate, win_streak, lose_streak, pnl_net]
    c1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost','Strike Rate','Win Streak', 'Losing Streak', 'PnL Net']
    d1 = [total_open, total_closed,total_won,total_lost,strike_rate, win_streak, lose_streak, pnl_net]
    #Check which set of headers is the longest.
    if len(h1) > len(h2):
        header_length = len(h1)
    else:
        header_length = len(h2)
    #Print the rows
    print_list = [h1,r1,h2,r2]
    row_format ="{:<15}" * (header_length + 1)
    print("Trade Analysis Results for Symbol:"+symbol)
    for row in print_list:
        print(row_format.format('',*row))

    export_csv(c1,d1,strategyName,symbol,from_date, to_date)

def export_csv(c1,d1,strategyName,symbol,from_date, to_date):
   
    df1 = pd.DataFrame([d1], index=[0], columns=c1)
    # print(df1)
    df1.to_csv("temp/Trade_Summary_"+strategyName+"_"+symbol+"_"+from_date+"_to_"+to_date+".csv",index=False)


def export_trade_list(trade_list,strategyName,symbol,from_date, to_date):
    df = pd.DataFrame(trade_list)
    df = df.drop(['pnl', 'pnl/bar', 'ticker'], axis=1)
    df.to_csv("temp/Trade_List_"+strategyName+"_"+symbol+"_"+from_date+"_to_"+to_date+".csv",index=False)
