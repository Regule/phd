'''
This script takes train, test and validation csv files then either loads neural network or trains
a new one. If only validation set is given no training occures.
'''

import logging
import argparse
import numpy as np
import glob
import json
import time
import os
import sys


import theano, keras
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation 
from keras.layers.core import Flatten, Permute, Reshape
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM, GRU
from keras.layers.convolutional import Convolution1D, MaxPooling1D, Convolution2D, MaxPooling2D
from keras.preprocessing.sequence import pad_sequences





logger = None # Global logger for this script
DEFAULT_LOGGER_LEVEL = logging.INFO
LOGGER_NAME = 'GRU_RUNNER'
LOGGER_FORMAT = '%(name)s %(levelname)s %(asctime)s:%(message)s'


def setup_logger(logging_level=logging.INFO, log_file=None):
    global logger
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging_level)
    formatter = logging.Formatter(LOGGER_FORMAT)
    
    # Logging to stdout
    ch = logging.StreamHandler()
    ch.setLevel(logging_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    # Logging to file
    if log_file is not None:
        fileHandler = logging.FileHandler(log_file)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)

    logger.info("Started Logger")


def string_to_log_level(level_str):
    level_map = {
            'critical': logging.CRITICAL,
            'error': logging.ERROR,
            'warining': logging.WARNING,
            'info': logging.INFO,
            'debug': logging.DEBUG,
            'silent': logging.CRITICAL
            }
    try:
        return level_map[level_str]
    except KeyError:
        return logging.INFO


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--log_level', type=string_to_log_level, default=DEFAULT_LOGGER_LEVEL,
            help='Logging level, valid values: silent, critical, error, warning, info, debug')
    parser.add_argument('--log_file', type=str, default=None,
            help='If set logs will be written to this file.')
    return parser.parse_args()


def main(args):
    setup_logger(args.log_level, args.log_file)
    logger.info(f'Using Keras version {keras.__version__}' )
    logger.info(f'Using Theano version {theano.__version__}')

if __name__ == '__main__':
    main(parse_arguments())

if logger is None:
    setup_logger()
