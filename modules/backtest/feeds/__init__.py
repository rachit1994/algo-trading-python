from .localfeed import * 


def pull(instrumenttype, symbol, tf, **kwargs):
    mode = "local_back_test"
    fromDate = None
    toDate = None
    for key, value in kwargs.items():
        if key == 'fromDate':
            fromDate = value
        elif key == 'toDate':
            toDate = value
        print ("%s == %s" %(key, value))

    if mode=="local_back_test":

        return localfeed(instrumenttype, symbol, tf, fromDate, toDate)