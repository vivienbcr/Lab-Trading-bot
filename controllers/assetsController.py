import logging
from models.context import Context
from models.order import Order, get_trade_history
from models.context import Context
from services.binanceRequests import get_order,post_sell_oco_order
import time
def search_update_buy_order(ctx:Context):
    buy_history = get_trade_history(ctx,state="open",status="buy")
    for order in buy_history:
        # trade_id == order buy id
        response = get_order(ctx,order.trade_id,order.pair)
        if response and response["status"]=="FILLED":
            order.atBuyOrderConfirmation()
            logging.info("🎩  Worker_Asset POST SELL OCO ORDER ")
            oco_response = post_sell_oco_order(ctx,order)
            print(oco_response)
            if oco_response :
                order.atOcoOrder(oco_response["transactionTime"])
            #post oco order
        elif response and response["status"]=="CANCELED":
            order.atCancelBuyOrder("CANCELED")
        elif response and response["status"]=="REJECTED":
            order.atCancelBuyOrder("REJECTED")
        elif response and response["status"]=="EXPIRED":
            order.atCancelBuyOrder("EXPIRED")
        else:
            logging.warning("🎩  Search update buy order not able to compute response {}".format(response))
        time.sleep(1)

def search_to_close_order(ctx):
    sell_history=get_trade_history(ctx,"open",'oco_sell')
    for order in sell_history:
        sl_order = dict()
        tp_order = dict()
        if order.oco_order_sl_id != '':
            sl_order = get_order(ctx,order.oco_order_sl_id,order.pair)
            time.sleep(0.25)
        if order.oco_order_tp_id != '':
            tp_order = get_order(ctx,order.oco_order_tp_id,order.pair)
            time.sleep(0.25)
        if sl_order and tp_order:
            if sl_order["status"] =="EXPIRED" or tp_order["status"] == "EXPIRED":
                order.atOcoOrderClose(sl_order["status"],tp_order["status"])
            else:
                logging.debug("Order {} always on order book ".format(order))
        else:
            logging.error("Order {} cannot be found on Binance, set error status")
            order.atError()