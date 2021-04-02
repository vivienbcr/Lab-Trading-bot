import pandas as pd
from datetime import datetime
from datetime import timedelta
import logging
import ta
from pathlib import Path


def compute_macd_rsi(pair: str, timeframe: str) -> None:
    logging.debug(
        "🛰️ Worker_Data Read from raw/tickers/{}_{}.csv".format(pair, timeframe))
    # Load data
    df = pd.read_csv("data/raw/"+pair+"_"+timeframe+".csv", sep=',',index_col=0)
    df = df.sort_values(by="Open_time")
    # Clean nan values
    df = ta.utils.dropna(df)
    # Add bollinger band high indicator filling nans values
    df['macd'] = ta.trend.macd(df["Close"], n_slow=26, n_fast=12, fillna=False)
    df["rsi"] = ta.momentum.rsi(df["Close"], 14, fillna=False)
    df = df.sort_values(by="Open_time", ascending=False)
    logging.debug(
        "🛰️ Worker_Data Write computed/macd_rsi_{}_{}.csv".format(pair, str(timeframe)))
    df.to_csv("data/computed/macd_rsi_"+pair+"_"+str(timeframe)+".csv")


def get_local_last_close(pair: str, timeframe: str) -> int:
    csv = Path("data/raw/"+pair+"_"+timeframe+".csv")
    if csv.is_file():
        df = pd.read_csv("data/raw/"+pair+"_"+str(timeframe)+".csv", sep=',')
        return int(int(df.iloc[0]['Open_time'])/1000)
    return 0


def get_next_close_from_local(pair: str, min_timeframe: int) -> int:
    csv = Path("data/raw/"+pair+"_"+str(min_timeframe)+"m.csv")
    if csv.is_file():
        df = pd.read_csv("data/raw/"+pair+"_" +
                         str(min_timeframe)+"m.csv", sep=',')
        last_tick = datetime.fromtimestamp(
            int(int(df.iloc[0]['Open_time'])/1000))
        next_tick = last_tick + timedelta(minutes=min_timeframe)
        next_tick = datetime.timestamp(next_tick)
        return int(next_tick)
    return 0

