import logging
import threading 
import re
from datetime import datetime  
from datetime import timedelta 
from queue import Queue 
import time
"""
Custom deps
"""
from models.context import Context
from controllers.fileGenerator import write_raw_ticker_file
from controllers.fileProcessor import get_local_last_close,get_next_close_from_local, compute_macd_rsi

class WorkerDataGetter(threading.Thread):

    def __init__(self, qTimer: Queue, qTrader: Queue, ctx: Context):
        threading.Thread.__init__(self)
        self.queueTimer = qTimer
        self.queueTrader = qTrader
        self.shutdown_flag = threading.Event()
        self.request_counter = 0
        self.ctx = ctx
        self.last_tick=0



    def run(self):
        logging.info('🛰️ Worker_Data has spawn.')
        while not self.shutdown_flag.is_set():
            # Check queu to reset request count
            event = self.queueTimer.empty()
            """
            Control request counter
            """
            if not event:
                event = self.queueTimer.get()
                logging.debug("🛰️  Worker_Data clean request_counter")
                self.request_counter = 0
            if self.request_counter < self.ctx.request_limit:
                logging.info('🛰️  Worker_Data Search new tick ... {} requests last minute ...'.format(self.request_counter))
                """
                Start iteration over PAIRS
                """       
                for pair in self.ctx.pairs:
                    """
                    Control new tick
                    """
                    now = datetime.timestamp(datetime.now())
                    next_close = get_next_close_from_local(pair,self.ctx.min_timeframe)
                    if now < next_close:
                        logging.debug("🛰️ 💤 Worker_Data No new closing, don't iterate in pairs ")
                        break
                    for timeframe in self.ctx.timeframes:

                        """
                        Get raw history
                        """
                        write_raw_ticker_file(self.ctx,pair,timeframe)
                        self.request_counter += 1
                        """
                        Start parsing strategy
                        """
                        compute_macd_rsi(pair,timeframe)

                        """
                        End parsing strategy
                        """
                        # Si la dernière cloture est supérieur à la dernière cloture enregistrée on call le trader
                        last_close = get_local_last_close(pair,timeframe)
                        if last_close > self.last_tick:
                            # on process les indicateurs dans un autre thread
                            logging.info("🛰️ ⌚ Worker_Data New tick detected, wake up trader")
                            self.queueTrader.put({"pair":pair,"timeframe":timeframe})
                        else:
                            logging.debug("🛰️ 💤 Worker_Data {} {} already used, iddle".format(pair,timeframe))
                        time.sleep(0.5)

            self.last_tick = get_local_last_close(pair,self.ctx.timeframes[0])
            time.sleep(10)

        # ... Clean shutdown code here ...
        logging.warning('🛰️ Worker : DataGetter Thread #%s stopped' % self.ident)
