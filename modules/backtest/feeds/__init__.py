from .localfeed import * 

def pull(instrumenttype, symbol, tf):
    mode = "local_back_test"
    if mode=="local_back_test":
        return localfeed(instrumenttype, symbol, tf, None, None)

def pull(instrumenttype, symbol, tf, fromDate, toDate):
    mode = "local_back_test"
    if mode=="local_back_test":
        return localfeed(instrumenttype, symbol, tf, fromDate, toDate)