import logging
from models.context import Context
def init(log_level:int):
    # logger configuration
    logging.basicConfig(filename='bot.log',format='%(asctime)s:%(levelname)s:%(message)s', level=log_level)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)