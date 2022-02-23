"""
{Real System}
{Only enter a new position if the last simulated or real trade was a loser.
If last trade was a loser, myProfit will be less than zero.}
if(marketPosition = 0 and myProfit < 0 and Xaverage(Close,9) >
Xaverage(High,19) and
RSI(Close,9) crosses below 70) then
begin
buy next bar at High stop;
end;
if(marketPosition = 0 and myProfit < 0 and Xaverage(Close,9) <
Xaverage(Low,19) and
RSI(Close,9) crosses above 30) then
begin
sellShort next bar at Low stop;
end;
if(marketPosition = 1) then sell next bar at Lowest(Low,20) stop;
if(marketPosition =-1) then buytocover next bar at Highest(High,20) stop;
"""