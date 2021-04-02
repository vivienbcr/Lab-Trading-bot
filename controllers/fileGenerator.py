import logging
from models.context import Context
from services.binanceRequests import get_ohlc
import pandas as pd
from pathlib import Path


def write_raw_ticker_file(ctx: Context, pair: str, timeframe: str):
    logging.debug(
        "🛰️ Worker_Data Write raw data for {} on {}".format(pair, timeframe))
    newer_ohlc = get_ohlc(ctx, pair, timeframe)
    csv = Path("data/raw/"+pair+"_"+timeframe+".csv")
    if csv.is_file():
        logging.debug(
            "🛰️ Worker_Data Write raw data file exist, append data...")
        ohlc_old = pd.read_csv("data/raw/"+pair + "_" +
                               timeframe+".csv", sep=',', index_col=0)
        newer_ohlc = pd.concat([newer_ohlc, ohlc_old]).drop_duplicates(
            subset="Open_time")
    else:
        logging.debug(
            "🛰️ Worker_Data Write raw data file not exist, create file...")
    newer_ohlc = newer_ohlc.sort_values(by="Open_time" ,ascending=False)    
    newer_ohlc.to_csv("data/raw/" + pair + "_"+timeframe+".csv")