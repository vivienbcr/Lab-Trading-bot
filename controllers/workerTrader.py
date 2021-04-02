import logging
import threading 
import re
from datetime import datetime  
from datetime import timedelta 
from queue import Queue 
import time
from models.order import get_trade_history

"""
Custom deps
"""
from models.context import Context
from services.signals import macd_find_signal
from controllers.tradeController import compute_new_trade,post_buy_order

class WorkerTrader(threading.Thread):

    def __init__(self, q: Queue, ctx: Context):
        threading.Thread.__init__(self)
        self.queue = q
        self.shutdown_flag = threading.Event()
        self.request_counter = 0
        self.ctx = ctx
        self.last_tick=0



    def run(self):
        logging.info('📊  Worker_Trader has spawn.')
        
        while not self.shutdown_flag.is_set():
            event = self.queue.get()
            currentTrades = len(get_trade_history(self.ctx,state='open'))
            logging.debug("📊  Worker_Trader current open trades {}, maximum is set to {}".format(currentTrades,self.ctx.max_order_count))
            if self.ctx.max_order_count > currentTrades:
                
                if event["pair"]:
                    """
                    TODO IF CURRENT_ORDER =< MAXORDER
                    """
                    logging.info('📊  Worker_Trader, search strategy on {}'.format(event["pair"]))
                    """
                    Find signals
                    """
                    trust_index = 0
                    if 'macd' in self.ctx.strategies.keys():
                        macd = macd_find_signal(event["pair"],event["timeframe"],self.ctx.strategies["macd"]["minimum_negative_tick_len"])
                        if macd > 0 : 
                            logging.info("🎉  MACD signal found")
                            trust_index += macd

                    """
                    End signals
                    """
                    if trust_index > 0 :
                        """
                        Start compute risk, order params
                        """
                        #TODO add other results here
                        order = compute_new_trade(self.ctx,trust_index,event["pair"])
                        """
                        End
                        """
                        """
                        Post order
                        """
                        res = post_buy_order(self.ctx,order )
                        """
                        End
                        """
                time.sleep(1)

        # ... Clean shutdown code here ...
        logging.warning('📊  Worker_Trader : DataGetter Thread #%s stopped' % self.ident)
