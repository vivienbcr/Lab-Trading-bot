import configparser
import logging

def read_configuration(file_name):
    """Parsing configuration file

    Parameters:
    file_name (str): Configuration file name : "config.conf"

    Returns:
    config:ConfigParser

    """
    logging.info("Read file {} as configuration file".format(file_name))
    config = configparser.ConfigParser()
    config.read(file_name)
    return config
