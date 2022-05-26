from threading import Thread, Lock
import math
from binance_api import *
from binance_api import BIANANCE_API
import time
import Indicators
import pandas as pd
import logging
import traceback

pd.set_option("display.max_columns", None)
logging.basicConfig(filename="LOG.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

###############################################
#                   Globals

BUYPOS = False
Coins = []
mutex = Lock()

###############################################


class CoinStructure:

    def __init__(self, coinPair, df):

        self.coinPair = coinPair
        df = Indicators.stochastic(df)
        df = Indicators.MACD(df)
        self.df = Indicators.RSI(df)
        self.df['POS'] = None

def initService():

    start = time.time()

    # Get all Coins
    coin_pairs = BIANANCE_API.get_usdt_currency_pairs()

    # For each coin get 75 last candles
    for coin in coin_pairs:
        try:
            Coins.append(CoinStructure(coin, BIANANCE_API.get_coin_df(coin)))
        except Exception as ex:
            print(coin + ' ' + ex.__str__())
            continue
        time.sleep(0.4)
    
    excecution_time = time.time() - start
    print("Execution time: {0}:{1} minutes.".format(math.floor(excecution_time / 60), math.floor(excecution_time % 60)))

    return Coins


def sell_thread(coin):

    global BUYPOS

    buy_price = BIANANCE_API.get_coin_price(coin)

    while 1:
        time.sleep(5)
        Coin = CoinStructure(coin, BIANANCE_API.get_coin_df(coin))
        logger.info("""LOG : 
        In Sell Thread
        Coin.df.iloc[-1]['close'] > buy_price * 1.03 or Coin.df.iloc[-1]['close'] < buy_price * 0.99:
        Coin : {0}
        Coin.df.iloc[-1]['STOCHk_14_3_3'] : {1}
        Coin.df.iloc[-1]['STOCHd_14_3_3'] : {2}
        buy_price : {3}
        Coin.df.iloc[-1]['close'] : {4}
        """.format(Coin.coinPair, Coin.df.iloc[-1]['STOCHk_14_3_3'], Coin.df.iloc[-1]['STOCHd_14_3_3'], buy_price, Coin.df.iloc[-1]['close'])
 )
        # Sell Triger
        if Coin.df.iloc[-1]['close'] > buy_price * 1.02 or Coin.df.iloc[-1]['close'] < buy_price * 0.99:
            BIANANCE_API.sell_on_binance(coin, logger)
            time.sleep(1)
            price = BIANANCE_API.get_coin_price(coin)
            new_balance = BIANANCE_API.get_total_balance()
            logger.info("Sell:\n----\nCoin : {0}\nPrice : {1}\nNew Balance : {3}\nTime : {2}".format(Coin.coinPair, price, new_balance, (datetime.datetime.now() + datetime.timedelta(hours=2)).strftime("%d-%m-%y %H:%M:%S")))
            print("Sell:\n----\nCoin : {0}\nPrice : {1}\nNew Balance : {3}\nTime : {2}".format(Coin.coinPair, price, new_balance, (datetime.datetime.now() + datetime.timedelta(hours=2)).strftime("%d-%m-%y %H:%M:%S")))
            BUYPOS = False
            break

def checkforBuyPos(Coin : CoinStructure):

    global BALANCE
    global COINS_AMOUNT
    global BUYPOS

    # If Seen Stochastic under 20% - Oversold - Mark 'Pos' == 'Stochastic Oversold'
    if Coin.df.iloc[-1]['STOCHk_14_3_3'] < 20 and Coin.df.iloc[-1]['STOCHd_14_3_3'] < 20:
        Coin.df.iloc[-1, Coin.df.columns.get_loc('POS')] = 'Stochastic Oversold'
    # Stochastic middle
    if (Coin.df.iloc[-2]['POS'] == 'Stochastic Oversold' and (Coin.df.iloc[-1]['STOCHk_14_3_3'] > 20 and Coin.df.iloc[-1]['STOCHd_14_3_3'] > 20)) or Coin.df.iloc[-2]['POS'] == 'Stochastic Mid':
        Coin.df.iloc[-1, Coin.df.columns.get_loc('POS')] = 'Stochastic Mid'
        #print("Coin __{0}__ In Stochastic Mid POS. (MACD : {1}, RSI : {2})".format(Coin.coinPair, Coin.df.iloc[-1]['macd_h'], Coin.df.iloc[-1]['RSI_14']))
        logger.info("Coin __{0}__ In Stochastic Mid POS. (MACD : {1}, RSI : {2})".format(Coin.coinPair, Coin.df.iloc[-1]['macd_h'], Coin.df.iloc[-1]['RSI_14']))
    #Stocastic over 80% - overbought
    if Coin.df.iloc[-1]['STOCHk_14_3_3'] > 80 and Coin.df.iloc[-1]['STOCHd_14_3_3'] > 80:
        Coin.df.iloc[-1, Coin.df.columns.get_loc('POS')] = None
    # If'Pos' = 'Stochastic Mid & RSI > 50 & macd_h > 0 -> BUY
    if Coin.df.iloc[-1]['POS'] == 'Stochastic Mid' and Coin.df.iloc[-1]['macd_h'] > 0 and Coin.df.iloc[-1]['RSI_14'] > 50:
        logger.info("""LOG :
        if Coin.df.iloc[-1]['POS'] == 'Stochastic Mid' and Coin.df.iloc[-1]['macd_h'] > 0 and Coin.df.iloc[-1]['RSI_14'] > 50:
        Coin : {0}
        Coin.df.iloc[-1]['POS'] : {1}
        Coin.df.iloc[-1]['macd_h'] : {2}
        Coin.df.iloc.[-1]['RSI_14'] : {3}
        BUYPOS : {4}
        Time : {5}
        """.format(Coin.coinPair, Coin.df.iloc[-1]['POS'], Coin.df.iloc[-1]['macd_h'],Coin.df.iloc[-1]['RSI_14'], BUYPOS, (datetime.datetime.now() + datetime.timedelta(hours=2)).strftime("%d-%m-%y %H:%M:%S")))
        mutex.acquire()
        if BUYPOS:
            mutex.release()
            return
        # Send Buy Command
        BUYPOS = True
        logger.info("Coin __{}__In mutex\n".format(Coin.coinPair))
        BUYPOS = BIANANCE_API.buy_on_binance(Coin.coinPair, logger)
        mutex.release()
        time.sleep(1)
        price = BIANANCE_API.get_coin_price(Coin.coinPair)
        logger.info("Buy:\n----\nCoin : {0}\nPrice : {1}\nMACD : {2}\nTime : {3}".format(Coin.coinPair, price, Coin.df.iloc[-1]['macd_h'], (datetime.datetime.now() + datetime.timedelta(hours=2)).strftime("%d-%m-%y %H:%M:%S")))
        print("Buy:\n----\nCoin : {0}\nPrice : {1}\nMACD : {2}\nTime : {3}".format(Coin.coinPair, price, Coin.df.iloc[-1]['macd_h'], (datetime.datetime.now() + datetime.timedelta(hours=2)).strftime("%d-%m-%y %H:%M:%S")))
        if BUYPOS:
            sellThread = Thread(target=sell_thread, args=[Coin.coinPair])
            sellThread.start()


def coinThread(coin: CoinStructure):
    symbol = coin.coinPair

    twm = ThreadedWebsocketManager(api_key=Config.API_KEY, api_secret=Config.SECRET_KEY)
    # start is required to initialise its internal loop
    twm.start()

    def handle_socket_message(msg):
        try:
            msg = msg['k']
            msg['t'] = str(datetime.datetime.fromtimestamp(msg['t'] / 1000))
            msg['T'] = str(datetime.datetime.fromtimestamp(msg['T'] / 1000))

            # If the new msg need to enter the table -> Append
            to_insert = {'time': msg['t'], 'open': msg['o'], 'close': msg['c'], 'high': msg['c'], 'low': msg['l'],
                             'volume': msg['v']}
            if msg['t'] != str(coin.df.iloc[-1]['time']):
                coin.df = coin.df.append(to_insert, ignore_index=True)
            else:
                coin.df.iloc[-1] = to_insert
            coin.df = Indicators.stochastic(
            coin.df.drop(columns=['STOCHk_14_3_3', 'STOCHd_14_3_3', 'macd',
                                          'macd_h', 'macd_s', 'RSI_14']))
            coin.df = Indicators.MACD(coin.df)
            coin.df = Indicators.RSI(coin.df)
            # Check for buyPos
            checkforBuyPos(coin)
        except Exception:
            logger.info("Coin : {0}\n{1}".format(coin.coinPair ,traceback.format_exc()))
    twm.start_kline_socket(callback=handle_socket_message, symbol=symbol, interval='5m')


def mainLoop(Coins):

    for Coin in Coins:
        coinThread(Coin)

if __name__ == '__main__':
    print("Server Start Initialization. It might take 5 minutes.\n")
    Coins = initService()
    logger.info("Server Initialized Succesfully. Good Luck.\nNum Of Assets: {}".format(len(Coins)))
    print("Server Initialized Succesfully. Good Luck.\nNum Of Assets: {}".format(len(Coins)))
    print("Starting Balance : {}\n{}".format(BIANANCE_API.get_total_balance(), datetime.datetime.now() + datetime.timedelta(hours=2)))
    mainLoop(Coins)
