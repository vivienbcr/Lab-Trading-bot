import os
import pandas as pd
from pathlib import Path
import unittest
import configparser
from models.context import Context
from models.order import Order
from services.binanceRequests import get_balance,get_average_asset_price, valid_buy_order
from configuration.reader import read_configuration

class TestBinanceRequests(unittest.TestCase):

    def setUp(self):
        config = read_configuration("config.cfg")
        self.ctx = Context(config)


    def test_get_balance(self):
        r = get_balance(self.ctx)
        self.assertEqual(r["canTrade"],True)
    def test_get_avg_asset_price(self):
        r=get_average_asset_price(self.ctx,"BTCUSDT")
        print(r)
        self.assertEqual(r>0,True)
    def test_valid_buy_order(self):
        r = Order(self.ctx,{'asset_price': 18254.69, 'trade_sl': 18254.34, 'trade_tp': 18256.04, 'quantity': 0.000965, 'pair': 'BTCUSDT','type':'buy'})
        o = valid_buy_order(self.ctx,r)
        self.assertEqual(o,True)