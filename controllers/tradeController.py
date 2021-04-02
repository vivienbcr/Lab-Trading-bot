import logging
from services.binanceRequests import get_balance, get_average_asset_price, valid_buy_order,post_live_buy_order
from models.context import Context
from models.order import Order
import math
from services.tools import truncate, get_asset_in_binance_account, apply_trust_index, risk_division_from_balance, get_out_price_for_percent_loss, get_out_price_for_percent_win, get_quantity

def compute_new_trade(ctx: Context, trust_index: int, pair: str)->Order:
    """
    Take balance : get trading asset dict : {asset :"USDT",free:10.00,locked:10.00}
    """
    account = get_balance(ctx)
    trading_asset = get_asset_in_binance_account(account, ctx.trading_asset)
    """
    Compute Total asset balancefree and locked balance
    """
    total_asset_balance = float(
        trading_asset["free"])+float(trading_asset["locked"])
    """
    Compute trade part from risk_division part
    """
    trade_amount = risk_division_from_balance(
        total_asset_balance, ctx.risk_division)
    logging.info('📊  Check if trade {} {} | with {} trust_index {} {} is possible...'.format(trade_amount,
                                                                                   ctx.trading_asset, trust_index, apply_trust_index(trade_amount, trust_index), ctx.trading_asset))
    if ctx.min_order_value < float(trading_asset["free"]):
        """
        Apply trust index
        """
        trade_amount = apply_trust_index(trade_amount, trust_index)
        if trade_amount < ctx.min_order_value and ctx.risk_force == 1:
            logging.error("⚠️  Balance is too low : {}, RISK_DIVISION cannot be respected, RISK_FORCE is enabled, cancel trade.".format(
                total_asset_balance))
            return None
        if trade_amount < ctx.min_order_value and ctx.risk_force == 0:
            logging.warning("⚠️  Balance is too low : {}, RISK_DIVISION cannot be respected, MIN_ORDER_VALUE as {} will be used".format(
                total_asset_balance, ctx.min_order_value))
            trade_amount = ctx.min_order_value
        """
        Compute Quantity, stop_loss, tp
        """
        order = dict()
        order["asset_price"] = truncate(get_average_asset_price(ctx, pair),2)
        order["trade_sl"] = get_out_price_for_percent_loss(trade_amount, ctx.target_loss_limit, order["asset_price"])
        order["trade_tp"] = get_out_price_for_percent_win(trade_amount, ctx.target_win_limit, order["asset_price"])
        order["quantity"] = get_quantity(order["asset_price"], trade_amount)
        order["pair"] = pair
        order["type"]="buy"
        
        logging.info("📊  ORDER BUY {} {} for {} {}, current price : {} {}, STOP : {} {}, TP : {} {}".format(order["quantity"], pair, trade_amount,ctx.trading_asset, order["asset_price"], ctx.trading_asset, order["trade_sl"], ctx.trading_asset, order["trade_tp"], ctx.trading_asset))
        t_order = Order()
        t_order.from_compute(ctx,order)                                                                            
        return t_order
    logging.error("⚠️  Balance is lower than minimum BINANCE accept orders, check your BINANCE balance account on https://www.binance.com ")
    return None

# FIXME améliorer les cas ou les ordres sont cassés
def post_buy_order(ctx:Context,order:Order):
    r = valid_buy_order(ctx,order)
    if r :
        order_response = post_live_buy_order(ctx,order)
        order.atBuyOrder(order_response["clientOrderId"],order_response["transactTime"])
        return True
    else:
        logging.error("📊  Invalid order")
        return False
    # parse trades_history.csv
    # find order with open status and buyed status
    # place OCO order
    # update csv status
    return

# def check_buy_orders_status(ctx:Context):

#     return
# def post_oco_sell_order(ctx:Context,order:Order):
