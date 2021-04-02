import logging
import threading 
import re
from datetime import datetime  
from datetime import timedelta 
import time


"""
Custom deps
"""
from models.context import Context
from services.signals import macd_find_signal
from controllers.assetsController import search_update_buy_order,search_to_close_order

class WorkerAsset(threading.Thread):

    def __init__(self, ctx: Context):
        threading.Thread.__init__(self)
        self.shutdown_flag = threading.Event()
        self.ctx = ctx

    def run(self):
        logging.info('🎩  Worker_Asset has spawn.')
        
        while not self.shutdown_flag.is_set():
            logging.info('🎩  Worker_Asset search trade updates ....')
            """
            traite les ,state open,status buyed => post oco order
            """
            search_update_buy_order(self.ctx)
            """
            traite les ,state open,
            """
            logging.info('🎩  Worker_Asset search trade closed ....')
            search_to_close_order(self.ctx)
            """
            traite les ,state open,status ocosell
            """
            time.sleep(10)


        # ... Clean shutdown code here ...
        logging.warning('🎩  Worker_Asset : DataGetter Thread #%s stopped' % self.ident)
