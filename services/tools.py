import math
def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper

def get_asset_in_binance_account(account:dict, asset:str)-> dict:
    for balance in account["balances"]:
        if balance["asset"] == asset:
            return balance
    return dict()

def get_quantity(asset_price,spent):
    return truncate(spent / asset_price,6)

def get_out_price_for_percent_win(spent,percent_win,asset_price):
    return truncate(asset_price + spent * percent_win / 100 + 1,2)

def get_out_price_for_percent_loss(spent,percent_loss,asset_price):
    return truncate(asset_price - percent_loss / 100 * spent,2)

def apply_trust_index(trade_amount,trust_index):
    return truncate(trade_amount + trade_amount * trust_index / 100 ,2)

def risk_division_from_balance(total_asset_balance,risk_division):
    return truncate(truncate(total_asset_balance,2)/risk_division,2)