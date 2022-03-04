"""
{The Money Manager}
{Demonstrates the programming and use of a money management scheme.}
{The user inputs initial capital and the amount he wants to risk on each
trade.}
Inputs: initCapital(100000),rskAmt(.02);
Vars: marketRisk(0),numContracts(0);
marketRisk = StdDev(Close,30) * BigPointValue;
numContracts = (initialCapital * rskAmt) / marketRisk;
value1 = Round(numContracts,0);
if(value1 > numContracts) then
numContracts = value1 - 1
else
numContracts = value1;
numContracts = MaxList(numContracts,1); {make sure at least 1 contract is

traded}

Buy("MMBuy") numContracts shares tomorrow at Highest(High,40) stop;
SellShort("MMSell") numContracts shares tomorrow at Lowest(Low,40) stop;
if(MarketPosition = 1) then Sell("LongLiq") next bar at Lowest(Low,20) stop;
if(MarketPosition =-1) then BuyToCover("ShortLiq") next bar at
Highest(High,20) stop;
"""