import os
from constants.common import CSV_PATH
from lib.utils.read_csv import get_historical_data_from_csv
from lib.utils.candle import Candle

class BackTest():
    def test_strategy(self, df, strategy):
        current_strategy = strategy(df)
        for i in df.itertuples():
            current_strategy.setup()
            if current_strategy.long():
                print("bought")
        
    def test_local_csv(self, strategy):
        for root,dirs,files in os.walk(CSV_PATH):
            for file in files:
                if file.endswith(".csv"):
                    df = get_historical_data_from_csv(CSV_PATH+file)
                    self.test_strategy(df, strategy)