import math

from binance.exceptions import BinanceAPIException, BinanceOrderException

import Config
from binance.client import Client
import datetime
import pandas as pd


class BIANANCE_API:

    client = Client(api_key=Config.API_KEY, api_secret=Config.SECRET_KEY)

    @classmethod
    def get_usdt_currency_pairs(cls):
        output = []
        all_pairs = cls.client.get_all_tickers()
        for pair in all_pairs:
            if pair['symbol'].endswith("USDT"):
                if not (pair['symbol'].endswith("UPUSDT") or pair['symbol'].endswith("DOWNUSDT")):
                    output.append(pair['symbol'])
        try:
            [output.remove(coin + "USDT") for coin in Config.FiatCoins]
            [output.remove(coin + "USDT") for coin in Config.NotExsistCoins]
            [output.remove(coin + "USDT") for coin in Config.USDCoins]
            [output.remove(coin + "USDT") for coin in Config.ignoreCoins]
        except Exception as ex:
            pass

        return output

    @classmethod
    def get_coin_df(cls, symbol, date=datetime.datetime.now(), interval='5m'):

        time_change_back = datetime.timedelta(minutes=1500)

        df = pd.DataFrame(
            cls.client.get_historical_klines(symbol=symbol, start_str=str(date - time_change_back), interval=interval))
        df.columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'qav', 'num_trades',
                      'taker_base_vol', 'taker_quote_vol', 'is_best_match']
        df.drop(['num_trades', 'close_time', 'qav', 'taker_base_vol', 'taker_quote_vol', 'is_best_match'], axis=1,
                inplace=True)
        df.time = [datetime.datetime.fromtimestamp(x / 1000) for x in df.time]
        return df

    @staticmethod
    def __truncate(number, position):
        '''Return number with dropped decimal places past specified position.'''
        return number - number % (10 ** position)

    @classmethod
    def buy_on_binance(cls, coin, logger):
        usdt_balance = float(cls.client.get_asset_balance(asset='USDT')['free'])
        price = float(cls.client.get_symbol_ticker(symbol=coin)['price'])
        price_round_to = float(cls.client.get_symbol_info(symbol=coin)['filters'][0]['minPrice']) * 10
        quantity_round_to = float(cls.client.get_symbol_info(symbol=coin)['filters'][2]['minQty']) * 10
        price_with_insurance = cls.__truncate(price * 1.005, math.log10(price_round_to))
        quantity = cls.__truncate(usdt_balance/price_with_insurance * 0.9975, math.log10(quantity_round_to))
        if str(quantity)[-2:] == '.0':
            quantity = int(quantity)
        logger.info("""
Before BUY client.create_order
USDT Balance : {0}
Price : {1}
quantity_round_to : {2}
quantity : {3}

        """.format(usdt_balance, price, quantity_round_to, quantity))
        print("""
Before BUY client.create_order
USDT Balance : {0}
Price : {1}
quantity_round_to : {2}
quantity : {3}
        """.format(usdt_balance, price, quantity_round_to, quantity))
        try:
            buy_limit = cls.client.create_order(
                symbol=coin,
                side='BUY',
                type='MARKET',
                quantity=quantity)
            logger.info("True returned")
            return True
        except BinanceAPIException as e:
            # error handling goes here
            print(e)
            logger.info(e)
            logger.info("False returned")
            return False
        except BinanceOrderException as e:
            # error handling goes here
            print(e)
            logger.info(e)
            logger.info("False returned")
            return False

    @classmethod
    def sell_on_binance(cls, coin, logger):
        _coin = coin.split('USDT')[0]
        coin_balance = float(str(float(cls.client.get_asset_balance(asset=_coin)['free']))[:-2]) if str(float(cls.client.get_asset_balance(asset=_coin)['free']))[-3] != '.' else int(str(float(cls.client.get_asset_balance(asset=_coin)['free']))[:-3]) 
        logger.info("""
Before SELL client.create_order
Coin Balance : {0}
Coin : {1}

        """.format(coin_balance, coin))
        print("""
Before SELL client.create_order
Coin Balance : {0}
Coin : {1}
""".format(coin_balance, coin))
        while 1:
            try:
                sell_limit = cls.client.create_order(
                    symbol=coin,
                    side='SELL',
                    type='MARKET',
                    quantity=coin_balance)
                break
            except BinanceAPIException as e:
                # error handling goes here
                print(e)
                logger.info(e)
            except BinanceOrderException as e:
                # error handling goes here
                logger.info(e)
                print(e)

    @classmethod
    def get_coin_price(cls, coin):
        return float(cls.client.get_symbol_ticker(symbol=coin)['price'])

    @classmethod
    def get_total_balance(cls):

        balance = 0
        for coin in cls.client.get_account()['balances']:
            balance += float(coin['free']) + float(coin['locked'])

        return round(balance, 2)

