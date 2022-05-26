import config
from binance.enums import *
from binance.client import Client
import websocket, json, pprint, talib, numpy

RSI_CYCLE = 15                              # You can adjust the value if you want to be more overbought/oversold
RSI_OVERSOLD = 25
RSI_OVERBOUGHT = 75
HOW_MUCH_TO_BUY = 0.05                      # You can adjust the value if you want to buy more/less
TRADE_SYMBOL = 'ADAUSD'                     # You can adjust the coin (currently the coin is CARDANO)

opens = []                                  # Candelas open values
closes = []                                 # Candelas closes values
in_position = False

# The Candlestick Stream push updates to the current candlestick every 1 minute
# You can change and choose a different intervals by the format: <symbol>@kline_<interval_length>
SOCKET = "wss://stream.binance.com:9443/ws/adausdt@kline_1m"
client = Client(config.API_KEY, config.API_SECRET, tld='us')


"""
* Side = buy/sell order
* Symbol = the symbol of the coin that we want to buy
* Quantity = the quantity of the coin that we ant to buy
"""
def order(side, quantity, symbol, order_type):
    try:
        print("Sending Your Order Right Now.")
        my_order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(f'Order Details => {my_order}')
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True


"""
Function role is to update the user we the connection is open and ready to work.
We have a reference to the websocket.
"""
def mine_on_open(ws):
    print('Good Morning Boss! The Connection Is Open!')


"""
Function role is to update the user we the connection is close.
We have a reference to the websocket.
"""
def mine_on_close(ws):
    print('Good Night Boss! The Connection Is Close!')


"""
Function role is to present the data that we are receiving from the server (more detailed explanation in the documentation).
We have a reference to the websocket & copy of the message.
"""
def mine_on_message(ws, message):
    global opens, closes, in_position                                           # Reference to the globals

    open_price = get_json_data(message, True, 'o')                              # Open price
    close_price = get_json_data(message, True, 'c')                             # Close price
    is_candle_finished = get_json_data(message, True, 'x')                      # Finished = a new candle "born"


    if is_candle_finished:
        print(f'Candle closed => {close_price}')                                # Print the closing price of the candle
        closes.append(float(close_price))                                       # Update the close candelas list
        print(f'Updated closes list => {closes}')

        if len(closes) >= RSI_CYCLE:                                            # Calculate after RSI cycle completed
            np_closes = numpy.array(closes)                                     # Convert the list to numpy array
            rsi = talib.RSI(np_closes, RSI_CYCLE)
            print(rsi)
            print(f'the current rsi is {rsi[-1]}')

            if rsi[-1] < RSI_OVERSOLD:
                if in_position:
                    print("Oversold Alert! You already own it, do nothing.")
                else:
                    print("Oversold Alert! You need to BUY immediately")
                    # Execute order in binance API
                    order_result = order(SIDE_BUY, HOW_MUCH_TO_BUY, TRADE_SYMBOL, ORDER_TYPE_MARKET)
                    if order_result:            # If the order succeeded - we bought a new position,so update it
                        in_position = True

            if rsi[-1] > RSI_OVERBOUGHT:
                if in_position:
                    print("Overbought Alert! You need to SELL immediately")
                    # Execute order in binance API
                    order_result = order(SIDE_SELL, HOW_MUCH_TO_BUY, TRADE_SYMBOL, ORDER_TYPE_MARKET)
                    if order_result:            # If the order succeeded - we no longer in position,so update it
                        in_position = False
                else:
                    print("Overbought Alert! You are not in a position, do nothing.")


"""
Function role is to return the requested data from the given json message.
"""
def get_json_data(message, is_candle, type_of_data):
    json_msg = json.loads(message)
    # pprint.pprint(json_msg)                                   # Unmark this line to receive and print the given data

    if is_candle and type_of_data == 'k': return json_msg['k']  # Candle obj

    if is_candle is False:
        if type_of_data == 'e': return json_msg['e']            # Event type
        if type_of_data == 'E': return json_msg['E']            # Event time
        if type_of_data == 's': return json_msg['s']            # Symbol
        else: return
    else:
        candle = json_msg['k']                                  # A new 'root' for "mini-json" message
        if type_of_data == 't': return candle['t']              # Candle start time
        if type_of_data == 'T': return candle['T']              # Candle close time
        if type_of_data == 's': return candle['s']              # Symbol
        if type_of_data == 'i': return candle['i']              # Interval
        if type_of_data == 'f': return candle['f']              # First trade ID
        if type_of_data == 'L': return candle['L']              # Last trade ID
        if type_of_data == 'o': return candle['o']              # Open price
        if type_of_data == 'c': return candle['c']              # Close price
        if type_of_data == 'h': return candle['h']              # High price
        if type_of_data == 'l': return candle['l']              # Low price
        if type_of_data == 'v': return candle['v']              # Base asset volume
        if type_of_data == 'n': return candle['n']              # Number of trades
        if type_of_data == 'x': return candle['x']              # Is this kline closed?
        if type_of_data == 'q': return candle['q']              # Quote asset volume
        if type_of_data == 'V': return candle['V']              # Taker buy base asset volume
        if type_of_data == 'Q': return candle['Q']              # Taker buy quote asset volume
        if type_of_data == 'B': return candle['B']              # Ignore
        else: return

# on_open function => for when we will open the connection ['ptr' to our executable function]
# on_close function => for when we will close the connection ['ptr' to our executable function]
# on_message function => for when we will need to send/update the user ['ptr' to our executable function]
ws = websocket.WebSocketApp(SOCKET, on_open=mine_on_open, on_close=mine_on_close, on_message=mine_on_message)
# Execute the web socket that we define
ws.run_forever()
