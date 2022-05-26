import pandas as pd
import pandas_ta as ta

def MACD(df: pd.DataFrame):
    # # Calculate MACD values using the pandas_ta library
    # Get the 26-day EMA of the closing price
    k = df['close'].ewm(span=12, adjust=False, min_periods=12).mean()
    # Get the 12-day EMA of the closing price
    d = df['close'].ewm(span=26, adjust=False, min_periods=26).mean()
    # Subtract the 26-day EMA from the 12-Day EMA to get the MACD
    macd = k - d
    # Get the 9-Day EMA of the MACD for the Trigger line
    macd_s = macd.ewm(span=9, adjust=False, min_periods=9).mean()
    # Calculate the difference between the MACD - Trigger for the Convergence/Divergence value
    macd_h = macd - macd_s
    # Add all of our new values for the MACD to the dataframe
    df['macd'] = df.index.map(macd)
    df['macd_h'] = df.index.map(macd_h)
    df['macd_s'] = df.index.map(macd_s)
    # View our data
    return df


def parabolicSar():
    pass


def stochastic(df):
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['open'] = df['open'].astype(float)
    df = df.join(df.ta.stoch(high='high', low='low', k=14, d=3))
    return df


def EMA(df):
    df['MA25'] = df['close'].rolling(window=25).mean()
    df['MA50'] = df['close'].rolling(window=50).mean()
    df['MA100'] = df['close'].rolling(window=100).mean()
    df['MA200'] = df['close'].rolling(window=200).mean()


def EMA(df):
    df['EMA25'] = df['close'].ewm(span=25, adjust=False).mean()
    df['EMA50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['EMA100'] = df['close'].ewm(span=100, adjust=False).mean()
    df['EMA200'] = df['close'].ewm(span=200, adjust=False).mean()
    return df


def RSI(df, periods=14):

    df = df.join(df.ta.rsi(close='close', length=periods))
    return df
