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
"""