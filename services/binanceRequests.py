import logging
import pandas as pd
import numpy as np
from binance.client import Client
from models.context import Context
from datetime import datetime
from requests.exceptions import Timeout, ReadTimeout, TooManyRedirects, RequestException
from models.order import Order
import time
from binance.enums import *
from binance.client import BinanceAPIException
# def get_oco_order(ctx:Context,id:str,pair):
#     retry = 0
#     status = False
#     while status == False or retry > ctx.requests_retry_limit:
#         try:
#             r = ctx.binance_client.query(origClientOrderId = origClientOrderId)
#             print(r)
#             status = True
#             return r
#         except BinanceAPIException as e:
#             logging.error(e)
#             retry +=1
#             time.sleep(ctx.requests_cooldown)
#     return dict()
def get_order(ctx:Context,txid:str ,pair:str):
    retry = 0
    status = False
    while status == False or retry > ctx.requests_retry_limit:
        try:
            r = ctx.binance_client.get_order(origClientOrderId=txid,symbol=pair)
            print(r)
            status = True
            return r
        except BinanceAPIException as e:
            logging.error(e)
            retry +=1
            time.sleep(ctx.requests_cooldown)
    return dict()
def post_sell_oco_order(ctx:Context,order:Order):
    logging.info("✉️  Post OCO SELL ORDER , {}".format(order))
    retry = 0
    status = False
    while status == False or retry > ctx.requests_retry_limit:
        try:
            r = ctx.binance_client.order_oco_sell(symbol=order.pair,listClientOrderId=order.trade_id,quantity=order.quantity,limitClientOrderId= order.oco_order_tp_id,stopClientOrderId=order.oco_order_sl_id, price=order.trade_tp,stopPrice=order.trade_sl, stopLimitPrice=order.trade_sl)
            print(r)
            status = True
            return r
        except BinanceAPIException as e:
            logging.error("🚨🚨 Post OCO SELL ORDER  Error {}".format(e))
            retry +=1
            time.sleep(ctx.requests_cooldown)
    return dict()

def post_live_buy_order(ctx:Context,order:Order):
    logging.info("✉️  Post LIVE BUY ORDER , {}".format(order))
    try:
        r = ctx.binance_client.create_order(symbol=order.pair,newClientOrderId=order.trade_id, side=SIDE_BUY,type=ORDER_TYPE_LIMIT,quantity=order.quantity,price=order.asset_price, timeInForce=TIME_IN_FORCE_GTC)
        print(r)
        return r
    except BinanceAPIException as e:
        logging.error("🚨🚨 Post LIVE BUY ORDER  Error {}".format(e))
        return 

def valid_buy_order(ctx:Context,order:Order):
    logging.info("✉️  Post VALIDATION BUY ORDER , {}".format(order))
    try:
        r = ctx.binance_client.create_test_order(symbol=order.pair,newClientOrderId=order.trade_id,side=SIDE_BUY,type=ORDER_TYPE_LIMIT,quantity=order.quantity,price=order.asset_price, timeInForce=TIME_IN_FORCE_GTC)
        print(r)
        return True
    except BinanceAPIException as e:
        logging.error("🚨🚨 Post validation BUY ORDER  Error {}".format(e))
        return False
# FIXME  CATCH https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#ip-limits

# def post_sell_oco_order(ctx: Context,pair:str,):
#     order = ctx.binance_client.create_oco_order()
def get_average_asset_price(ctx: Context,pair:str):
    logging.info('Get average {} price'.format(pair))
    retry = 0
    status = False
    while status == False or retry > ctx.requests_retry_limit:
        try:
            print(pair)
            avg_price = ctx.binance_client.get_avg_price(symbol=pair)
            status = True
        except ReadTimeout:
            logging.warning("⚠️  Request Binance get_avg_price TimeReadTimeout, retry in {} seconds. Retry {} / {}".format(ctx.requests_retry_limit,retry,ctx.request_limit))
            pass
        except TooManyRedirects:
            logging.warning("⚠️  Request Binance get_avg_price TooManyRedirects, retry in {} seconds. Retry {} / {}".format(ctx.requests_retry_limit,retry,ctx.request_limit))
            pass
        except RequestException as e:
            logging.warning("⚠️  Request Binance get_avg_price RequestException {}, retry in {} seconds. Retry {} / {}".format(e,ctx.requests_retry_limit,retry,ctx.request_limit))
            pass
        retry +=1
        time.sleep(ctx.requests_cooldown)
    if status == False :
        logging.error("🚨  Error while requests Binance get_avg_price, closing bot")
        raise SystemExit("🚨  Error while requests Binance get_avg_price, closing bot")
    return float(avg_price["price"])

def get_balance(ctx: Context):
    logging.info('Get binance account')
    retry = 0
    status = False
    while status == False or retry > ctx.requests_retry_limit:
        try:
            account = ctx.binance_client.get_account()
            status = True
        except ReadTimeout:
            logging.warning("⚠️  Request Binance get_account TimeReadTimeout, retry in {} seconds. Retry {} / {}".format(ctx.requests_retry_limit,retry,ctx.request_limit))
            pass
        except TooManyRedirects:
            logging.warning("⚠️  Request Binance get_account TooManyRedirects, retry in {} seconds. Retry {} / {}".format(ctx.requests_retry_limit,retry,ctx.request_limit))
            pass
        except RequestException as e:
            logging.warning("⚠️  Request Binance get_account RequestException {}, retry in {} seconds. Retry {} / {}".format(e,ctx.requests_retry_limit,retry,ctx.request_limit))
            pass
        retry +=1
        time.sleep(ctx.requests_cooldown)
    if status == False :
        logging.error("🚨  Error while requests Binance get_account, closing bot")
        raise SystemExit("🚨  Error while requests Binance get_account, closing bot")
    return account

def get_ohlc(ctx:Context, pair:str, timeframe:str):
    logging.debug("🛰️ Worker_Data Request BINANCE for {} on {}".format(pair,timeframe))
    retry = 0
    status = False
    while status == False or retry > ctx.requests_retry_limit:
        try:
            candles = ctx.binance_client.get_klines(symbol=pair, interval = timeframe)
            status = True
        except ReadTimeout:
            logging.warning("⚠️  Request Binance get_klines TimeReadTimeout, retry in {} seconds. Retry {} / {}".format(ctx.requests_retry_limit,retry,ctx.request_limit))
            pass
        except TooManyRedirects:
            logging.warning("⚠️  Request Binance get_klines TooManyRedirects, retry in {} seconds. Retry {} / {}".format(ctx.requests_retry_limit,retry,ctx.request_limit))
            pass
        except RequestException as e:
            logging.warning("⚠️  Request Binance get_klines RequestException {}, retry in {} seconds. Retry {} / {}".format(e,ctx.requests_retry_limit,retry,ctx.request_limit))
            pass
        retry +=1
        time.sleep(ctx.requests_cooldown)
    if status == False :
        logging.error("🚨  Error while requests Binance get_klines, closing bot")
        raise SystemExit("🚨  Error while requests Binance get_klines, closing bot")
    df = pd.DataFrame(columns= ['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time'])
    dtime, opentime, lopen, lhigh, llow, lclose, lvol, closetime = [], [], [], [], [], [], [], []

    for candle in candles:
        dtime.append(datetime.fromtimestamp(candle[0]/1000))
        opentime.append(candle[0])
        lopen.append(candle[1])
        lhigh.append(candle[2])
        llow.append(candle[3])
        lclose.append(candle[4])
        lvol.append(candle[5])
        closetime.append(candle[6])

    df['dtime'] = dtime
    df['Open_time'] = opentime
    df['Open'] = np.array(lopen).astype(np.float)
    df['High'] = np.array(lhigh).astype(np.float)
    df['Low'] = np.array(llow).astype(np.float)
    df['Close'] = np.array(lclose).astype(np.float)
    df['Volume'] = np.array(lvol).astype(np.float)
    df['Close_time'] = closetime
 
    return df

