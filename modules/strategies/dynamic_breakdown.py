"""
If BarNumber = 1 then lookBackDays = 20
Else do the following
Today's market volatility = StdDev(Close,30)
Yesterday's market volatility = StdDev(Close[1],30)
deltaVolatility = (today's volatility - yesterday's
volatility)/today's volatility
lookBackDays = (1 + deltaVolatility) * lookBackDays
lookBackDays = MinList(lookBackDays,60)
lookBackDays = MaxList(lookBackDays,20)

upBand = Average(Close,lookBackDays) + StdDev(Close,lookBackDays) *2.00
dnBand = Average(Close,lookBackDays) - StdDev(Close,lookBackDays) *2.00
buyPoint = Highest(High,lookBackDays)
sellPoint = Lowest(Low,lookBackDays)
longLiqPoint = Average(Close,lookBackDays)
shortLiqPoint = Average(Close,lookBackDays)
If Close of yesterday > upBand) then initiate a long position if today's
market action >= buyPoint
If (Close of yesterday < dnBand) then initiate a short position if today's
market action <= sellPoint
Liquidate long position if today's market action <= longLiqPoint
Liquidate short position if today's market action >= shortLiqPoint
"""

"""
{Dynamic Break Out II by George Pruitt
This system is an extension of the original Dynamic Break Out system written
by George for Futures Magazine in 1996. In addition to the channel break out
methodology, DBS II incorporates Bollinger Bands to determine trade entry.}
Inputs: ceilingAmt(60),floorAmt(20),bolBandTrig(2.00);
Vars: lookBackDays(20),todayVolatility(0),yesterDayVolatility(0),
deltaVolatility(0);
Vars: buyPoint(0),sellPoint(0),longLiqPoint(0),shortLiqPoint(0),upBand(0),
dnBand(0);
todayVolatility = StandardDev(Close,30,1);
yesterDayVolatility = StandardDev(Close[1],30,1); {See how I offset the
function call to get
yesterday's value}
deltaVolatility = (todayVolatility - yesterDayVolatility)/todayVolatility;
lookBackDays = lookBackDays * (1 + deltaVolatility);
lookBackDays = Round(lookBackDays,0);
lookBackDays = MinList(lookBackDays,ceilingAmt); {Keep adaptive engine within bounds}

lookBackDays = MaxList(lookBackDays,floorAmt);
upBand = BollingerBand(Close,lookBackDays,+bolBandTrig);
dnBand = BollingerBand(Close,lookBackDays,-bolBandTrig);
buyPoint = Highest(High,lookBackDays);
sellPoint = Lowest(Low,lookBackDays);
longLiqPoint = Average(Close,lookBackDays);
shortLiqPoint = Average(Close,lookBackDays);
if(Close > upBand) then Buy("DBS-2 Buy") tomorrow at buyPoint stop;
if(Close < dnBand) then SellShort("DBS-2 Sell") tomorrow at sellPoint stop;
if(MarketPosition = 1) then Sell("LongLiq") tomorrow at longLiqPoint stop;
if(MarketPosition = -1) then BuyToCover("ShortLiq") tomorrow at shortLiqPoint
stop;
"""