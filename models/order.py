import uuid
from pathlib import Path
import csv
import logging
import pandas as pd
from datetime import datetime  
import numpy as np
import time
from models.context import Context
class Order():
    def __init__(self):
        self.trade_id = ""
        self.status = ""
        self.state = ""
        self.created = ""
        self.type = ""
        self.asset_price : float = 0
        self.trade_sl : float = 0
        self.trade_tp : float= 0
        self.quantity : float= 0
        self.pair=""
        self.buy_order_id=""
        self.oco_list_client_order_id=""
        self.oco_order_tp_id=""
        self.oco_order_tp_status=""
        self.oco_order_sl_id=""
        self.oco_order_sl_status=""
        self.buy_order_time=""
        self.oco_time=""
        self.result=""
        self.trades_history_file=""

    def from_compute(self,ctx : Context, order):
        self.trade_id = str(uuid.uuid4())
        self.status = "created"
        self.state = "ready"
        self.created = str(datetime.now())
        self.type = order["type"]
        self.asset_price : float = order["asset_price"]
        self.trade_sl : float = order["trade_sl"]
        self.trade_tp : float= order["trade_tp"]
        self.quantity : float= order["quantity"]
        self.pair=order["pair"]
        self.buy_order_id=""
        self.oco_list_client_order_id=""
        self.oco_order_tp_id=str(uuid.uuid4())
        self.oco_order_tp_status=""
        self.oco_order_sl_id=str(uuid.uuid4())
        self.oco_order_sl_status=""
        self.buy_order_time=""
        self.oco_time=""
        self.result=""
        self.trades_history_file=ctx.trades_history_file
        self.add_to_csv()
    def atBuyOrder(self,buy_order_id,buy_order_time):
        self.buy_order_id = buy_order_id
        self.buy_order_time = buy_order_time
        self.status = 'open'
        self.type = 'buy'
        self.state = 'buy'
        self.add_to_csv()
    def atCancelBuyOrder(self,state):
        self.status = 'close'
        self.add_to_csv()
    def atError(self):
        self.status = 'error'
        self.add_to_csv()
    def atBuyOrderConfirmation(self):
        self.state = 'buyed'
        self.add_to_csv()

    def atOcoOrder(self,oco_time):
        self.oco_order_sl_status="open"
        self.oco_order_tp_status="open"
        self.oco_time = oco_time
        self.state = 'oco_sell'
        self.add_to_csv()

    def atOcoOrderClose(self,oco_order_sl_status,oco_order_tp_status):
        self.status = "close"
        self.oco_order_sl_status= oco_order_sl_status
        self.oco_order_tp_status= oco_order_tp_status
        self.state = 'oco_sell'
        #FIXME gere le résultat avec le profit
        if oco_order_sl_status == "EXPIRED" and oco_order_tp_status == "FILLED":
            self.result="win"
        elif oco_order_sl_status == "FILLED" and oco_order_tp_status == "EXPIRED":
            self.result="loss"
        else:
            self.result="unknow"
        self.add_to_csv()

    def from_model(self,
                    trade_id="",
                    status="",
                    state="",
                    created="",
                    side_type="",
                    asset_price=float(0),
                    trade_sl=float(0),
                    trade_tp=float(0),
                    quantity=float(0),
                    pair="",
                    buy_order_id="",
                    oco_list_client_order_id="",
                    oco_order_tp_id="",
                    oco_order_tp_status="",
                    oco_order_sl_id="",
                    oco_order_sl_status="",
                    buy_order_time="",
                    oco_time="",
                    result=""):
        self.trade_id = trade_id
        self.status = status
        self.state = state
        self.created = created
        self.type = side_type
        self.asset_price = asset_price
        self.trade_sl = trade_sl
        self.trade_tp = trade_tp
        self.quantity = quantity
        self.pair = pair
        self.buy_order_id = buy_order_id
        self.oco_list_client_order_id=oco_list_client_order_id
        self.oco_order_tp_id=oco_order_tp_id
        self.oco_order_tp_status=oco_order_tp_status
        self.oco_order_sl_id=oco_order_sl_id
        self.oco_order_sl_status=oco_order_sl_status
        self.buy_order_time=buy_order_time
        self.oco_time=oco_time
        self.result=result
    
    def add_to_csv(self):

        data = [self.trade_id,self.state,self.status,self.created,self.type,self.asset_price,self.trade_sl,self.trade_tp,self.quantity,self.pair,self.buy_order_id,self.oco_list_client_order_id,self.oco_order_tp_id,self.oco_order_tp_status,self.oco_order_sl_id,self.oco_order_sl_status,self.buy_order_time,self.oco_time,self.result]
        df = pd.DataFrame(np.array([data]),columns= ['trade_id','state','status','created','type',"asset_price","trade_sl","trade_tp","quantity",'pair','buy_order_id','oco_list_client_order_id','oco_order_tp_id','oco_order_tp_status','oco_order_sl_id','oco_order_sl_status','buy_order_time','oco_time','result'])
        csv = Path(self.trades_history_file)
        if csv.is_file():
            trades_old = pd.read_csv(self.trades_history_file, sep=',', index_col=0)
            newer_trades = pd.concat([df,trades_old]).drop_duplicates(subset="trade_id",ignore_index=True)
            newer_trades.to_csv(self.trades_history_file)
        else:
            df.to_csv(self.trades_history_file)

def get_trade_history(ctx: Context,state:str,status=''):
    csv = Path(ctx.trades_history_file)
    if csv.is_file():
        trades = pd.read_csv(ctx.trades_history_file, sep=',', index_col=0)
        trades = trades.loc[trades['state'] == state]
        if(status != ''):
            trades = trades.loc[trades['status'] == status]
        list_buy_order = []
        for index,row in trades.iterrows():
            trade = Order()
            trade.from_model(trade_id=row["trade_id"],
                                        status=row["status"],
                                        state=row["state"],
                                        created=row["created"],
                                        side_type=row["type"],
                                        asset_price=row["asset_price"],
                                        trade_sl=row["trade_sl"],
                                        trade_tp=row["trade_tp"],
                                        quantity=row["quantity"],
                                        pair=row["pair"],
                                        buy_order_id=row["buy_order_id"],
                                        oco_list_client_order_id=row["oco_list_client_order_id"],
                                        oco_order_tp_id=row["oco_order_tp_id"],
                                        oco_order_tp_status=row["oco_order_tp_status"],
                                        oco_order_sl_id=row["oco_order_sl_id"],
                                        oco_order_sl_status=row["oco_order_sl_status"],
                                        buy_order_time=row["buy_order_time"],
                                        oco_time=row["oco_time"],
                                        result=row["result"])
            list_buy_order.append(trade)
        return list_buy_order
    else:
        return []