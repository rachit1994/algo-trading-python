from datetime import date
from datetime import datetime
from time import tzname
from datetime import time
from kiteconnect import KiteConnect
from constants.kite import *


class Zerodha():

    def __init__(self, api_key, api_secret, request_token):
        self.kite = KiteConnect(api_key=api_key)
        access_token = self.kite.generate_session(
            request_token=request_token, api_secret=api_secret)
        self.kite.set_access_token(access_token)

    def get_profit(self, buy_price, sell_price, qty, exchange, trade_type):
        total_buy_price = buy_price * qty
        total_sell_price = sell_price * qty

        if exchange == EXCHANGE_BSE:
            transaction_charges = 3
        elif exchange == EXCHANGE_NSE:
            buy_transaction = total_buy_price * TRANSACTION_CHARGES_NSE
            sell_transaction = total_sell_price * TRANSACTION_CHARGES_NSE
            transaction_charges = buy_transaction + sell_transaction

        if trade_type == TRADE_TYPE_INTRADAY:
            buy_brokerage = total_buy_price * BROKERAGE_INTRADAY
            sell_brokerage = total_sell_price * BROKERAGE_INTRADAY

            buy_brokerage = buy_brokerage if buy_brokerage < BROKERAGE_INTRADAY_FLAT else BROKERAGE_INTRADAY_FLAT
            sell_brokerage = sell_brokerage if sell_brokerage < BROKERAGE_INTRADAY_FLAT else BROKERAGE_INTRADAY_FLAT

            brokerage = buy_brokerage + sell_brokerage
            stt_ctt = sell_price * STT_CTT_INTRADAY
        elif trade_type == TRADE_TYPE_DELIVERY:
            stt_ctt = (sell_price * STT_CTT_DELIVERY) + \
                (buy_price * STT_CTT_DELIVERY)
            brokerage = 0

        gst = (brokerage + transaction_charges) * GST
        sebi_buy_charges = buy_price * qty * SEBI_CHARGES
        sebi_sell_charges = sell_price * qty * SEBI_CHARGES
        sebi_charges = sebi_buy_charges + sebi_sell_charges

        total_charges = brokerage + transaction_charges + stt_ctt + gst + sebi_charges
        profit_loss = total_sell_price - total_buy_price
        final_profit_loss = profit_loss - total_charges

        return (final_profit_loss, total_charges)

    def is_tradingday(self):
        today = date.today()
        weekday_index = today.weekday()
        # Saturday and Sunday
        if weekday_index == 5 or weekday_index == 6:
            return False
        else:
            if today in [datetime.strptime(d, "%d/%m/%Y").date() for d in holiday_list]:
                return False
            else:
                return True

    def is_indian_timezone(self):
        if tzname[1] == 'IST':
            return True
        else:
            return False

    def is_pre_market_hour(self):
        now = datetime.now()

        pre_market_open_time = time(*map(int, PRE_MARKET_OPEN_TIME.split(':')))
        pre_market_close_time = time(
            *map(int, PHYSICAL_MARKET_OPEN_TIME.split(':')))

        if pre_market_open_time <= now.time() <= pre_market_close_time:
            return True
        else:
            return False

    def is_market_hour(self):
        now = datetime.now()

        physical_market_open_time = time(
            *map(int, PHYSICAL_MARKET_OPEN_TIME.split(':')))
        physical_market_close_time = time(
            *map(int, PHYSICAL_MARKET_CLOSE_TIME.split(':')))

        if physical_market_open_time <= now.time() <= physical_market_close_time:
            return True
        else:
            return False

    def get_historical_data(self, instrument_token, from_data, to_data, interval):
        return self.kite.historical_data(instrument_token=instrument_token,
                                         from_date=from_data,
                                         to_date=to_data,
                                         interval=interval)
