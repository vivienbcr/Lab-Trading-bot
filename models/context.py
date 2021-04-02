from binance.client import Client
import re
import configparser

def min_timeframe(timeframes):
    mini = 1
    for time in timeframes:
        int_time = int(re.search(r'\d+', time).group())
        if int_time > mini :
            mini = int_time
    return mini
class Context():
    def __init__(self,config):
        self.pairs = config.get("BINANCE","PAIRS").split(',')
        self.timeframes = config.get("BINANCE","TIMEFRAMES").split(',')
        self.min_timeframe = min_timeframe(config.get("BINANCE","TIMEFRAMES").split(','))
        self.binance_client=Client(config['BINANCE']["PUBLIC_KEY"], config['BINANCE']["PRIVATE_KEY"])
        self.trading_asset=config.get("BINANCE","TRADING_ASSET")
        self.request_limit = int(config.get('BINANCE','REQUEST_LIMIT'))
        self.log_level=config.get('BOT','LOG_LEVEL')
        self.trades_history_file=config.get('BOT','HISTORY_FILE')
        self.max_order_count = int(config.get('WALLET','MAX_ORDER_COUNT'))
        self.max_order_value = int(config.get('WALLET','MAX_ORDER_VALUE'))
        self.min_order_value = int(config.get('WALLET','MIN_ORDER_VALUE'))
        self.risk_division = int(config.get('WALLET','RISK_DIVISION'))
        self.risk_force = int(config.get('WALLET','RISK_FORCE'))
        self.target_win_limit = float(config.get('WALLET','TARGET_WIN_LIMIT'))
        self.target_loss_limit = float(config.get('WALLET','TARGET_LOSS_LIMIT'))
        self.requests_retry_limit=int(config.get('BOT','REQUESTS_RETRY_LIMIT'))
        self.requests_cooldown=int(config.get('BOT','REQUESTS_COOLDOWN'))
        self.strategies = dict()
        if int(config.get("MACD","ENABLE")) == 1 :
            self.strategies["macd"] = {"minimum_negative_tick_len" : int(config.get('MACD','MINIMUM_NEGATIVE_TICK_LENGTH')) }
