"""
    atr10 = AverageTrueRange(10)
    keyOfDay = (High + Low + Close)/3
    buyEasierDay = 0
    sellEasierDay = 0
    if(Close > keyOfDay) then sellEasierDay = 1
    if(Close<=keyOfDay) then buyEasierDay = 1
    avg3Hi = Average(High,3)
    avg3Lo = Average(Low,3)
    if(buyEasierDay = 1) then
    longEntryPoint = Open + atr10 * 0.5
    shortEntryPoint = Open - atr10 * 0.75
    if(sellEasierDay = 1) then
    longEntryPoint = Open + atr10 * 0.75
    shortEntryPoint = Open - atr10 * 0.5
    longEntryPoint = MaxList(longEntryPoint,avg3Lo)
    shortEntryPoint = MinList(shortEntryPoint,avg3Hi)
    Initiate a long position of today's market action >= longEntryPoint
    Initiate a short position of today's market action <= shortEntryPoint

    If the ChoppyMarketIndex function returns a value greater than or equal
    to 20, then the system goes into the long-term trend-following mode.
"""

"""
Inputs: bollingerLengths(50),trendLiqLength(50),numStdDevs(2),
swingPrcnt1(0.50),swingPrcnt2(0.75),atrLength(10),
swingTrendSwitch(20);
Vars:cmiVal(0),buyEasierDay(0),sellEasierDay(0),trendLokBuy(0),
trendLokSell(0),keyOfDay(0),swingBuyPt(0),swingSellPt(0),
trendBuyPt(0),trendSellPt(0),swingProtStop(0);
cmiVal = ChoppyMarketIndex(30);
buyEasierDay = 0;
sellEasierDay = 0;
trendLokBuy = Average(Low,3);
trendLokSell= Average(High,3);
keyOfDay = (High + Low + Close)/3;
if(Close > keyOfDay) then sellEasierDay = 1;
if(Close <= keyOfDay) then buyEasierDay = 1;
if(buyEasierDay = 1) then
begin
swingBuyPt = Open of tomorrow + swingPrcnt1*AvgTrueRange(atrLength);
swingSellPt = Open of tomorrow - swingPrcnt2*AvgTrueRange(atrLength);
end;
if(sellEasierDay = 1) then
begin
swingBuyPt = Open of tomorrow + swingPrcnt2*AvgTrueRange(atrLength);
swingSellPt = Open of tomorrow - swingPrcnt1*AvgTrueRange(atrLength);
end;
swingBuyPt = MaxList(swingBuyPt,trendLokBuy);
swingSellPt = MinList(swingSellPt,trendLokSell);
trendBuyPt = BollingerBand(Close,bollingerLengths,numStdDevs);
trendSellPt = BollingerBand(Close,bollingerLengths,- numStdDevs);

if(cmiVal < swingTrendSwitch)then
begin
if (MarketPosition <> 1) then Buy("SwingBuy") next bar at swingBuyPt
stop;
if(MarketPosition <> -1) then SellShort("SwingSell") next bar at
swingSellPt stop;
end
else
begin
swingProtStop = 3*AvgTrueRange(atrLength);
Buy("TrendBuy") next bar at trendBuyPt stop;
SellShort("TrendSell") next bar at trendSellPt stop;
Sell from Entry("TrendBuy") next bar at Average(Close,trendLiqLength)
stop;
BuyToCover from Entry("TrendSell") next bar at
Average(Close,trendLiqLength) stop;
Sell from Entry("SwingBuy") next bar at EntryPrice - swingProtStop
stop;
BuyToCover from Entry("SwingSell") next bar at EntryPrice +
swingProtStop stop;
end;
"""