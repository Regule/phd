'''
This script takes train, test and validation csv files then either loads neural network or trains
a new one. If only validation set is given no training occures.
'''

import logging
import argparse



logger = None # Global logger for this script
DEFAULT_LOGGER_LEVEL = logging.INFO
LOGGER_NAME = 'GRU_RUNNER'
LOGGER_FORMAT = '%(name)s %(levelname)s %(asctime)s:%(message)s'


def setup_logger(logging_level=logging.INFO, log_file=None):
    global logger
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging_level)
    ch = logging.StreamHandler()
    ch.setLevel(logging_level)
    formatter = logging.Formatter(LOGGER_FORMAT)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
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
    return parser.parse_args()

def main(args):
    setup_logger(args.log_level)
    logger.critical('critical')
    logger.error('error')
    logger.warning('warning')
    logger.info('info')
    logger.debug('debug')

if __name__ == '__main__':
    main(parse_arguments())
