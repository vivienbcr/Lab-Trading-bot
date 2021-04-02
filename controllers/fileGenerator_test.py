import os
import pandas as pd
from pathlib import Path
import unittest
import configparser
from models.context import Context
from controllers.fileGenerator import write_raw_ticker_file
from configuration.reader import read_configuration

class TestFileGenerator(unittest.TestCase):

    def setUp(self):
        config = read_configuration("config.cfg")
        self.ctx = Context(config)
        if os.path.exists("data/raw/{}_{}.csv".format(self.ctx.pairs[0], self.ctx.timeframes[0])):
            os.remove(
                "data/raw/{}_{}.csv".format(self.ctx.pairs[0], self.ctx.timeframes[0]))

    def test_write_raw_file_init(self):
        write_raw_ticker_file(
            self.ctx, self.ctx.pairs[0], self.ctx.timeframes[0])
        file_created = os.path.exists(
            "data/raw/{}_{}.csv".format(self.ctx.pairs[0], self.ctx.timeframes[0]))
        self.assertEqual(file_created, True)

    def test_write_raw_file_routine(self):
        write_raw_ticker_file(
            self.ctx, self.ctx.pairs[0], self.ctx.timeframes[0])
        self.df = pd.read_csv(
            "data/raw/{}_{}.csv".format(self.ctx.pairs[0], self.ctx.timeframes[0]), index_col=0)
        self.assertEqual(len(self.df.columns),8)