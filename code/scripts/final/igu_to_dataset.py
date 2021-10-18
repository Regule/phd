'''
This script transforms preprocessed CSV files generated from SP3.
'''
import argparse
import os
import pandas as pd
import numpy as np
import sys

EPOCH_COLUMN = 'Epoch'
BIAS_COLUMN = 'Clock_bias'

def process_clock_readout(input_file, output_file, separator):
    dataset = pd.read_csv(input_file, sep=separator)
    bias = dataset[BIAS_COLUMN].to_numpy()
    new_dataset = {}
    new_dataset['x0'] = bias
    for i in range(4):
        n = i+1
        padding = np.zeros(n)
        derivative = np.diff(bias, n=n)
        new_dataset[f'x{n}'] = np.concatenate((padding, derivative))
    series = pd.Series(new_dataset)
    #for window in series.rolling(window=2):
    #    print(window)
    #    sys.exit()
    new_dataset = pd.DataFrame(new_dataset) 
    new_dataset.to_csv(output_file, sep=separator, index=False)

def main(args):
    for root, _, files in os.walk(args.input_directory):
        for file in files:
            if '.csv' in file:
                process_clock_readout(os.path.join(root, file),
                        os.path.join(args.output_directory, file),
                        args.separator)


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--input_directory', type=str, required=True,
            help='Directory with CSV files for processing')
    parser.add_argument('-o', '--output_directory', type=str, required=True,
            help='Directory to whih processed files will be saved.')
    parser.add_argument('--separator', type=str, default=';',
            help='Character used for column separation in csv file.')
    return parser.parse_args()

if __name__ == '__main__':
    main(parse_arguments())


