import pandas as pd
import unittest
from datetime import datetime  
from datetime import timedelta 
from configuration.reader import read_configuration
from models.context import Context
from controllers.fileProcessor import get_local_last_close, get_next_close_from_local
# def get_local_last_close(pair,interval):
#     df = pd.read_csv("data/raw/"+pair+"_"+interval+".csv", sep=',')
#     return int(df.iloc[0]['Open_time'])/1000

class TestFileProcessor(unittest.TestCase):
    def setUp(self):
        config = read_configuration("config.cfg")
        self.ctx = Context(config)

    def test_get_local_last_close(self):
        last_timestamp_in_raw_data = get_local_last_close(self.ctx.pairs[0],self.ctx.timeframes[0])
        now = int(datetime.timestamp(datetime.now()))
        self.assertEqual(now > last_timestamp_in_raw_data,True)
    
    def test_get_next_close_from_local(self):
        last_timestamp_in_raw_data = get_local_last_close(self.ctx.pairs[0],self.ctx.timeframes[0])
        next_close = get_next_close_from_local(self.ctx.pairs[0],self.ctx.min_timeframe)
        print(last_timestamp_in_raw_data)
        print(next_close)
        self.assertEqual(last_timestamp_in_raw_data<next_close,True)