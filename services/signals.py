import pandas as pd
import logging
def macd_find_signal(pair:str,interval:str,minimum_negatives_series:int, test=False, test_file_name=''):
    logging.debug("📊  Worker_Trader, search MACD signal ...")
    if test:
        dataset = pd.read_csv("data/tests/"+test_file_name)
    else:
        dataset = pd.read_csv("data/computed/macd_rsi_"+pair+"_"+interval+".csv") 
    last_negative_periods = 0
    current_macd = dataset.iloc[0]['macd']
    previous_macd = dataset.iloc[1]['macd']
    if current_macd > 0 and previous_macd < 0 :
        for i in range(1,minimum_negatives_series+1):
            if dataset.iloc[i]['macd'] < 0 :
                print('neg')
                last_negative_periods = last_negative_periods + 1
            else:
                break
        if last_negative_periods >= minimum_negatives_series:
            logging.debug("📊  Worker_Trader, found MACD signal")
            return 1
    logging.debug("📊  Worker_Trader, MACD not found")
    return 0

# def rsi_find_signal(pair,interval,rsi_min,rsi_max):
#     dataset = pd.read_csv("computed/macd_rsi_"+pair+"_"+str(interval)+"m.csv")
#     rsi = dataset.iloc[0]['rsi']
#     if rsi > rsi_min and rsi < rsi_max:
#         return True
#     else :
#         return False