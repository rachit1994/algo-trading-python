"""
{Ghost system}
{Look to see if a trade would have been executed today and keep track
of our position and our entry price. Test today's high/low price
against the trade signal that was generated by offsetting our calculations
by one day.}
if(myPosition = 0 and Xaverage(Close[1],9) > Xaverage(High[1],19) and
RSI(Close[1],9) crosses below 70 and High >= High[1]) then
begin
myEntryPrice = MaxList(Open,High[1]); {Check for a gap open}
myPosition = 1;
end;
if(myPosition = 1 and Low < Lowest(Low[1],20) )then
begin
value1 = MinList((Lowest(low[1],20)),Open); {Check for a gap open}
myProfit = value1 - myEntryPrice {Calculate our trade
profit/loss}
myPosition = 0;
end;
if(myPosition = 0 and Xaverage(Close[1],9) < Xaverage(Low[1],19) and
RSI(Close[1],9) crosses above 30 and Low <= Low[1]) then
begin
myEntryPrice = MinList(Open,Low[1]);
myPosition =-1;
end;
if(myPosition =-1 and High > Highest(High[1],20)) then
begin
value1 = MaxList((Highest(High[1],20)),Open);{Check again for a gap
open}
myProfit = myEntryPrice - value1; {Calculate our trade profit/loss}
myPosition = 0;
end;
"""