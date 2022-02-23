"""
Inputs: goLongStart(301),goLongEnd(701),goShortStart(702),goShortEnd(228);
Vars: monthAndDay(0);
{The inputs represent the months and days that we can enter long and short
trades}
{301 is March 01 >> can only go long from this date and up to
701 is July 01 >> this date
702 is July 02 >> can only go short from this date and up to
228 is February 28 >> this date}
{Let's use the date and extract the information that we need from it to
determine the month and the day}
{If we divide the date by 10000, the remainder is the month and day. We can
use the modulus function}
monthAndDay = Mod(Date of tomorrow,10000);
if(monthAndDay >= goLongStart and monthAndDay <= goLongEnd) then
begin
buy("Seasonal Buy") tomorrow at Open;
end;
if(monthAndDay >= goShortStart or monthAndDay <= goShortEnd) then
{Notice that we had to use "or" instead of "and"—this is due
to the goShortEnd date is less than the goShortStart date}
begin
sellShort("Seasonal Sell") tomorrow at Open;
end;
"""