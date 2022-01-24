from lib.backtesting.backtesting import BackTest
from lib.strategies.abcd import Abcd

back = BackTest()

back.test_local_csv(Abcd)