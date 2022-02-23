"""
- From book building winning trading systems by george pruitt

King Keltner Pseudocode
    movAvg = Average(((High + Low + Close)/3),40)
    upBand = movAvg + Average(TrueRange,40)
    dnBand = movAvg – Average(TrueRange,40)
    liquidPoint = Average(((High + Low + Close)/3),40)

    A long position will be initiated when today's movAvg is greater than
    yesterday's and market action >= upBand

    A short position will be initiated when today's movAvg is less than
    yesterday's and market action <= dnBand
    
    A long position will be liquidated when today's market action
    <= liquidPoint
    
    A short position will be liquidated when today's market action
    >= liquidPoint
"""