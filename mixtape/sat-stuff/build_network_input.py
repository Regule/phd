'''
This script takes train, test and validation csv files then either loads neural network or trains
a new one. If only validation set is given no training occures.
'''


#==================================================================================================
#                                           IMPORTS
#==================================================================================================

import logging
import argparse
import numpy as np
import glob
import json
import time
import os
import sys

import pandas as pd
import numpy as np

#==================================================================================================
#                                            GLOBALS
#==================================================================================================

DEFAULT_LOGGER_LEVEL = logging.INFO
LOGGER_NAME = 'OBSERVATION_GENERATION'
LOGGER_FORMAT = '%(name)s %(levelname)s %(asctime)s:%(message)s'

logger = None # Global logger for this script

#==================================================================================================
#                                        DATA PROCESSING
#==================================================================================================


def data_from_csv(file_name):
    data = pd.read_csv(file_name, sep=';')
    X = data.iloc[:,0].to_numpy()
    Y = data.iloc[:,1:].to_numpy()
    return X, Y

def build_input_with_derivatives(timeseries, derivative_level):
    derivative = timeseries
    logger.info(f'Derivative 0 shape = {derivative.shape}')
    derivatives = [derivative.reshape(derivative.shape[0]), ]
    for l in range(derivative_level):
        derivative = np.diff(derivative, axis=0)
        logger.info(f'Derivative {l+1} shape = {derivative.shape}')
        derivatives.append(derivative.reshape(derivative.shape[0]))

def build_windowed_data(time_series, window_size):
    windows = []
    outputs = []
    step = 0
    while step + window_size < time_series.shape[0]:
        windows.append(time_series[step:step+window_size])
        outputs.append(time_series[step+window_size])
        step += 1
    return np.asarray(windows), np.asarray(outputs)

#==================================================================================================
#                                       UTILITY FUNCTIONS
#==================================================================================================

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
    parser.add_argument('-t', '--training_file', type=str, default=None,
            help='File with training observations')
    parser.add_argument('-d', '--derivative_level', type=int, default=2,
            help='To what degree a derivative should be included in input')
    return parser.parse_args()


#==================================================================================================
#                                       MAIN FUNCTION
#==================================================================================================

def main(args):
    setup_logger(args.log_level, args.log_file)
    X, Y = data_from_csv(args.training_file)
    X = build_input_with_derivatives(Y, args.derivative_level)

if __name__ == '__main__':
    main(parse_arguments())

if logger is None:
    setup_logger()
