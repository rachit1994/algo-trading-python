"""
averageRange = Average(Range of Daily Data,10)
averageOCRange = Average(Abs(Open-Close of Daily Data),10)
canTrade = Abs(Open-Close of Daily Data) < 85% of averageOCRange
buyEasierDay = 0
sellEasierDay = 0
if(Close of Daily Data <= Close[1] of Daily Data) then buyEasierDay = 1
if(Close of Daily Data > Close[1] of Daily Data) then sellEasierDay = 1
if(buyEasierDay) then
buyBOPoint = Open of tomorrow + 30% of averageRange
sellBOPoint = Open of tomorrow – 60% of averageRange
if(sellEasierDay) then
sellBOPoint = Open of tomorrow – 30% of averageRange
buyBOPoint = Open of tomorrow + 60% of averageRange
longBreakPt = High of Daily Data + 25% of averageRange {upside break out achieved}
shortBreakPt = Low of Daily Data – 25% of averageRange {dnside break out achieved}
longFBOPoint = Low of Daily Data + 25% of averageRange {dnside BO failure buy pt}

shortFBOPoint = High of Daily Data – 25% of averageRange {upside BO failure sell pt}

"""

"""

{Super Combo by George Pruitt
This intraday trading system will illustrate the multiple data handling
capabilities of TradeStation. All pertinent buy and sell calculations will be
based on daily bars and actual trades will be executed on 5-min bars. I have
made most of the parameters input variables.}
Inputs:waitPeriodMins(30),initTradesEndTime(1430),liqRevEndTime(1200),
thrustPrcnt1(0.30),thrustPrcnt2(0.60),breakOutPrcnt(0.25),
failedBreakOutPrcnt(0.25),protStopPrcnt1(0.25),protStopPrcnt2(0.15),
protStopAmt(3.00),breakEvenPrcnt(0.50),avgRngLength(10),avgOCLength(10);
Variables:averageRange(0),averageOCRange(0),canTrade(0),buyEasierDay(FALSE),
sellEasierDay(FALSE),buyBOPoint(0),sellBOPoint(0),longBreakPt(0),
shortBreakPt(0),longFBOPoint(0),shortFBOPoint(0),barCount(0),
intraHigh(0),intraLow(999999),buysToday(0),sellsToday(0),
currTrdType(0),longLiqPoint(0),shortLiqPoint(0),yesterdayOCRRange(0),
intraTradeHigh(0),intraTradeLow(999999);
{Just like we did in the pseudocode—let's start out with the daily bar
calculations. If Date <> Date[1]—first bar of day}
if(Date <> Date[1]) then {save time by doing these calculations once per day}
begin
averageRange = Average(Range,10) of Data2; {Data 2 points to daily bars}
yesterdayOCRRange = AbsValue(Open of Data2-Close of Data2);
averageOCRange = Average(AbsValue(Open of Data2-Close of Data2),10);
canTrade = 0;
if(yesterdayOCRRange< 0.85*averageOCRange) then canTrade = 1;
buyEasierDay = FALSE;
sellEasierDay = FALSE;
{See how we refer to Data2 - the daily data}
if(Close of Data2 <= Close[1] of Data2) then buyEasierDay = TRUE;
if(Close of Data2 > Close[1] of Data2) then sellEasierDay = TRUE;
if(buyEasierDay) then
begin
buyBOPoint = Open of data1 + thrustPrcnt1*averageRange;
sellBOPoint = Open of data1 - thrustPrcnt2*averageRange;
end;
if(sellEasierDay) then
begin
sellBOPoint = Open of data1 - thrustPrcnt1*averageRange;
buyBOPoint = Open of data1 + thrustPrcnt2*averageRange;
end;
longBreakPt = High of Data2 + breakOutPrcnt*averageRange;
shortBreakPt = Low of Data2 - breakOutPrcnt*averageRange;
shortFBOPoint = High of Data2 - failedBreakOutPrcnt*averageRange;
longFBOPoint = Low of Data2 + failedBreakOutPrcnt*averageRange;
{Go ahead and initialize any variables that we may need later on in the day}
barCount = 0;
intraHigh = 0;intraLow = 999999; {Didn't know you could do this}
buysToday = 0;sellsToday = 0;{You can put multiple statements on one
line}
currTrdType = 0;
end; {End of the first bar of data}
{Now let's trade and manage on 5-min bars}
if(High > intraHigh) then intraHigh = High;
if(Low < intraLow ) then intraLow = Low;
barCount = barCount + 1; {count the number of bars of intraday data}
if(barCount > waitPeriodMins/BarInterval and canTrade = 1) then
{have we waited long enough—wait PeriodMin is an input variable and
BarInterval is set by TradeStation. Wait PeriodMins = 30 and BarInterval = 5,
so 30/5 = 6}
begin
if(MarketPosition = 0) then
begin
intraTradeHigh = 0;
intraTradeLow = 999999;
end;
if(MarketPosition = 1) then
begin
intraTradeHigh = MaxList(intraTradeHigh,High);
buysToday = 1;
end;
if(MarketPosition =-1) then
begin
intraTradeLow = MinList(intraTradeLow,Low);
sellsToday = 1;
end;
if(buysToday = 0 and Time < initTradesEndTime) then
Buy("LBreakOut") next bar at buyBOPoint stop;
if(sellsToday = 0 and Time < initTradesEndTime) then
SellShort("SBreakout") next bar at sellBOPoint stop;
if(intraHigh > longBreakPt and sellsToday = 0 and Time <
initTradesEndTime) then
SellShort("SfailedBO") next bar at shortFBOPoint stop;
if(intraLow < shortBreakPt and buysToday = 0 and Time <
initTradesEndTime) then
Buy("BfailedBO") next bar at longFBOPoint stop;

{The next module keeps track of positions and places protective stops}
if(MarketPosition = 1) then
begin
longLiqPoint = EntryPrice - protStopPrcnt1*averageRange;
longLiqPoint = MinList(longLiqPoint,EntryPrice - protStopAmt);
if(MarketPosition(1) = -1 and BarsSinceEntry = 1 and
High[1] >= shortLiqPoint and shortLiqPoint < shortFBOPoint)
then
currTrdType = -2; {we just got long from a short liq reversal}
if(currTrdType = -2) then
begin
longLiqPoint = EntryPrice - protStopPrcnt2*averageRange;
longLiqPoint = MinList(longLiqPoint,EntryPrice -
protStopAmt);
end;
if(intraTradeHigh >= EntryPrice + breakEvenPrcnt*averageRange)
then
longLiqPoint = EntryPrice; {BreakEven trade}
if(Time >= initTradesEndTime) then
longLiqPoint = MaxList(longLiqPoint,Lowest(Low,3)); {Trailing
stop}
if(Time < liqRevEndTime and sellsToday = 0 and
longLiqPoint <> EntryPrice and BarsSinceEntry ≥ 4) then
begin
SellShort("LongLiqRev") next bar at longLiqPoint stop;
end
else begin
Sell("LongLiq") next bar at longLiqPoint stop;
end;
end;
if(MarketPosition =-1) then
begin
shortLiqPoint = EntryPrice+protStopPrcnt1*averageRange;
shortLiqPoint = MaxList(shortLiqPoint,EntryPrice + protStopAmt);
if(MarketPosition(1) = 1 and BarsSinceEntry(0) = 1 and
Low [1] <= longLiqPoint and longLiqPoint > longFBOPoint) then
currTrdType = +2; {we just got long from a short liq reversal}
if(currTrdType = +2) then
begin
shortLiqPoint = EntryPrice + protStopPrcnt2*averageRange;
shortLiqPoint = MaxList(shortLiqPoint,EntryPrice + protStopAmt);
end;
if(intraTradeLow <= EntryPrice - breakEvenPrcnt*averageRange) then
shortLiqPoint = EntryPrice; {BreakEven trade}
if(Time >= initTradesEndTime) then
shortLiqPoint = MinList(shortLiqPoint,Highest(High,3));
{Trailing stop}
if(Time < liqRevEndTime and buysToday = 0 and
shortLiqPoint <> EntryPrice and BarsSinceEntry ≥ 4) then
begin
Buy("ShortLiqRev") next bar at shortLiqPoint stop;
end
else begin
BuyToCover("ShortLiq") next bar at shortLiqPoint stop;
end;
end;
end;
SetExitOnClose;
"""