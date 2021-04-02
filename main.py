import logging
import logging.config
# import time
# import random
# from datetime import datetime  
# from datetime import timedelta 
# # https://github.com/dominiktraxl/pykrakenapi
# import krakenex
# import pandas as pd
# from pykrakenapi import KrakenAPI
# ## custom helpers
# import stratBasics 
# import fileGenerator
# import fileProcessor
# import orderController
# import tradeController
## interupt signal
import signal
import sys
## threading
from queue import Queue 
import threading 
# ## logging

from binance.client import Client
import configparser
import time
"""
Custom deps
"""
from configuration.reader import read_configuration
from models.context import Context
from services.binanceRequests import get_ohlc
from controllers.workerDataGetter import WorkerDataGetter
from controllers.workerTrader import WorkerTrader
from services.logger import init as logger_init
from controllers.workerAssetManagement import WorkerAsset
class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass
 
 
def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit


def main():
    # logger configuration
    # FIXME Problème avec la récupération de la configuration
    logger_init(logging.DEBUG)
    config = read_configuration("config.cfg")  
    ctx = Context(config)
    logging.info("🔥🔥🔥 TradingBot just spawned, start program. 🔥🔥🔥")
    # Setup core system features
    queueTimer = Queue() 
    queueTrader = Queue() 
    signal.signal(signal.SIGINT, service_shutdown)
    try:
        t1 = WorkerDataGetter(queueTimer, queueTrader,ctx)
        t1.start() 
        t2 = WorkerTrader(queueTrader,ctx)
        t2.start()
        t3= WorkerAsset(ctx)
        t3.start()
        while True:
            time.sleep(60)
            queueTimer.put(537)

    except ServiceExit:
        # Terminate the running threads.
        # Set the shutdown flag on each thread to trigger a clean shutdown of each thread.
        t1.shutdown_flag.set()
        t2.shutdown_flag.set()
        t3.shutdown_flag.set()
        # Wait for the threads to close...
        t1.join()
        t2.join()
        t3.join()

        


   

if __name__ == "__main__":
    main()
