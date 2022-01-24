import os
from constants.common import CSV_PATH
from lib.utils.read_csv import read_csv
from lib.utils.candle import Candle

class BackTest():
    def test_strategy(self, data, strategy):
        current_strategy = strategy(Candle(data))
        current_strategy.setup()
        if current_strategy.long():
            print("bought")
    
    def test_local_csv(self, strategy):
        for root,dirs,files in os.walk(CSV_PATH):
            for file in files:
                if file.endswith(".csv"):
                    read_csv(CSV_PATH+file, self.test_strategy, strategy)