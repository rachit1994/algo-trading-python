"""
Bollinger Bandit Pseudocode
    LiqDay is initially set to 50
    upBand = Average(Close,50) + StdDev(Close,50) *1.25
    dnBand = Average(Close,50) - StdDev(Close,50) *1.25
    rocCalc = Close of today - Close of thirty days ago
    Set liqLength to 50
    If rocCalc is positive, a long position will be initiated when
    today's market action >= upBand
    If rocCalc is negative, a short position will be initiated when
    today's market action <= dnBand
    liqPoint = Average(Close, 50)
    If liqPoint is above the upBand, we will liquidate a long position if
    today's market action <= liqPoint
    If liqPoint is below the dnBand, we will liquidate a short position
    if today's market action >= liqPoint
    If we are not stopped out today, then liqLength = liqLength - 1
    If we are stopped out today, then reset liqLength to fifty
Bollinger Bandit Program
    {Bollinger Bandit by George Pruitt—program uses Bollinger Bands and Rate of
    change to determine entry points. A trailing stop that is proportional with
    the amount of time a trade is on is used as the exit technique.}
    Inputs: bollingerLengths(50),liqLength(50),rocCalcLength(30);
    Vars: upBand(0),dnBand(0),liqDays(50),rocCalc(0);
    upBand = BollingerBand(Close,bollingerLengths,1.25);
    dnBand = BollingerBand(Close,bollingerLengths,-1.25);
    rocCalc = Close - Close[rocCalcLength-1]; {remember to subtract 1}
    if(MarketPosition <> 1 and rocCalc > 0) then Buy("BanditBuy")tomorrow upBand
    stop;
    if(MarketPosition <>-1 and rocCalc < 0) then SellShort("BanditSell") tomorrow
    dnBand stop;
    if(MarketPosition = 0) then liqDays = liqLength;
    if(MarketPosition <> 0) then
    begin
    liqDays = liqDays - 1;
    liqDays = MaxList(liqDays,10);
    116 Building Winning Trading Systems with TradeStation

    end;
    if(MarketPosition = 1 and Average(Close,liqDays) < upBand) then
    Sell("Long Liq") tomorrow Average(Close,liqDays) stop;
    if(MarketPosition = -1 and Average(Close,liqDays) > dnBand) then
    BuyToCover("Short Liq") tomorrow Average(Close,liqDays) stop;
"""