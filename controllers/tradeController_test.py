from controllers.tradeController import compute_new_trade
from models.context import Context
from models.order import Order
import unittest
from configuration.reader import read_configuration
class TestTradeController(unittest.TestCase):
    
    def setUp(self):
        config = read_configuration("config.cfg")
        self.ctx = Context(config)
        self.ctx.trades_history_file="test_trade_history.csv"


    def test_compute_new_trade(self):
        r = compute_new_trade(self.ctx,10,"BTCUSDT")
        print(r)
        self.assertEqual(isinstance(r,Order),True)