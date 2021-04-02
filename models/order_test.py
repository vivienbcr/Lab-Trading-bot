
from models.order import Order, get_trade_history
import unittest
import pandas as pd
from configuration.reader import read_configuration
from models.context import Context
import uuid
class TestOrderModel(unittest.TestCase):
    
    def setUp(self):
        config = read_configuration("config.cfg")
        self.ctx = Context(config)
        self.ctx.trades_history_file="test_trade_history.csv"
        self.trade_test_id=""


    # def test_order_init(self):
    #     order=Order(self.ctx,{'asset_price': 18254.69477233, 'trade_sl': 18254.34, 'trade_tp': 18256.04, 'quantity': 0.000965, 'pair': 'BTCUSDT',"type":"buy"})
    #     df = pd.read_csv("test_trade_history.csv")
    #     self.trade_test_id=df.at[0,"trade_id"]
    #     o = df.loc[df['trade_id']== self.trade_test_id]["state"]
    #     self.assertEqual(o[0] == "ready",True)
    #     order.atBuyOrder(buy_order_id=str(uuid.uuid4()) , buy_order_time=12212121)
    #     df = pd.read_csv("test_trade_history.csv")
    #     o = df.loc[df['trade_id']== self.trade_test_id]["state"]
    #     print(o)
    #     self.assertEqual(o[0] == "buy",True)
    #     order.atBuyOrderConfirmation()
    #     df = pd.read_csv("test_trade_history.csv")
    #     o = df.loc[df['trade_id']== self.trade_test_id]["state"]
    #     print(o)
    #     self.assertEqual(o[0] == "buyed",True)
    #     order.atOcoOrder(str(uuid.uuid4()),str(uuid.uuid4()),str(uuid.uuid4()),213141244)
    #     df = pd.read_csv("test_trade_history.csv")
    #     o = df.loc[df['trade_id']== self.trade_test_id]["state"]
    #     print(o)
    #     self.assertEqual(o[0] == "oco_sell",True)
    #     order.atOcoOrderClose("close","cancel")
    #     df = pd.read_csv("test_trade_history.csv")
    #     o = df.loc[df['trade_id']== self.trade_test_id]["state"]
    #     print(o)
    #     self.assertEqual(o[0] == "oco_sell",True)        

    def test_get_trade_history(self):
        orders = get_trade_history(self.ctx,"open","buy")
        for i in orders:
            print(i.trade_id)
        