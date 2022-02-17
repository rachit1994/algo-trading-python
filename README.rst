export PYTHONPATH="${PYTHONPATH}:/Developer/algoTrading/scratch

Folder structure

constants
    - common.py : should have all common constants
    - kite.py : should have constants related to zerodha, similary other brokers files should be created. These should have brokerages etc

kite_historical_data
    - these should have csv stocks file data

lib
    - this is created in a scope of microservices, this can be shared among other microservices

modules ( this is the main code for this micro service, no modules should be dependent except lib folder )
    - backtest : all backtesting functions or code should only be here and will be imported from this
    - portfolio : this module handles portfolioo management and money management
    - strategies : all strategies should be inside this ( remember only dependency should be modules )

src
    - This is not supposed to be shared, specific things should be inside this

temp
    - All data that is not supposed to be pushed should be inside this folder. Any temp csv files etc