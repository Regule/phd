'''
This scribt generates networks that try to predict clock bias relying only on a perviously
masured biases.
Depending on configuration it is possible to create either a single network that attempts to
predict bias for group of clocks or a network per clock.
'''

import argparse
import os
import neat
import numpy as np
import pandas as pd


def prepare_datasets(data_folder, window_size, separator):
    for root, _, files in os.walk(args.data_folder):
        for file in files:
            if '.csv' in file:
                single_satellite = pd.read_csv(os.path.join(root, file), sep=separator)

def main(args):
    pass


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-t', '--training_folder', type=str, default='local/data/training',
            help='Folder with CSV files used for training the network.')
    parser.add_argument('-v', '--validation_folder', type=str, default='local/data/validation',
            help='Folder where csv files with test data are stored, names must correspond to those in training folder')
    parser.add_argument('-c', '--config_file', type=str, required=True, 
            help='File with NEAT configuration.')
    parser.add_argument('-o', '--outpu_folder', type=str, default='local/output',
            help='Root folder for all generated outputs.')
    parser.add_argument('-s', '--single_network_mode', action='store_true',
            help='If set only a single network is generated for all clocks.')
    parser.add_argument('--separator', type=str, default=';',
            help='Character used for column separation in csv file.')
    return parser.parse_args()

if __name__ == '__main__':
    main(parse_arguments())
