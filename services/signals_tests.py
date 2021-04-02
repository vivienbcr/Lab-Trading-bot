import os
import pandas as pd
from pathlib import Path
import unittest
import configparser
from models.context import Context
from services.signals import macd_find_signal

class TestSignals(unittest.TestCase):

    def test_macd_find_signal_invalid_1(self):
        res = macd_find_signal("BTCUSDT","1m",6,True,"invalid_1_macd_BTCUSDT_1m.csv")
        self.assertEqual(res,0)
    def test_macd_find_signal_invalid_2(self):
        res = macd_find_signal("BTCUSDT","1m",6,True,"invalid_2_macd_BTCUSDT_1m.csv")
        self.assertEqual(res,0)
    def test_macd_find_signal_valid_1(self):
        res = macd_find_signal("BTCUSDT","1m",6,True,"valid_1_macd_BTCUSDT_1m.csv")
        self.assertEqual(res,1)
    def test_macd_find_signal_valid_2(self):
        res = macd_find_signal("BTCUSDT","1m",6,True,"valid_2_macd_BTCUSDT_1m.csv")
        self.assertEqual(res,1)