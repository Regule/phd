import argparse
import pandas as pd
import numpy as np
from datetime import datetime

EPOCH_STR_FORMAT = '%Y-%m-%d %H:%M:%S'

def read_data_from_csv(csv, epoch_column, bias_column):
    clock_data = pd.read_csv(csv, sep=';')
    clock_data[epoch_column] = clock_data[epoch_column].map(epoch_str_to_timestamp)
    x = clock_data.iloc[:][epoch_column].values
    y = clock_data.iloc[:][bias_column].values
    return x, y

def epoch_str_to_timestamp(epoch_str):
    return datetime.strptime(epoch_str, EPOCH_STR_FORMAT).timestamp()

def build_windowed_data(time_series, window_size):
    windows = []
    outputs = []
    step = 0
    while step + window_size < time_series.shape[0]:
        windows.append(time_series[step:step+window_size])
        outputs.append(time_series[step+window_size])
        step += 1
    return np.asarray(windows), np.asarray(outputs)


def main(csv_file, window_size, bias_column, epoch_column):
    x, y = read_data_from_csv(csv_file, epoch_column, bias_column)
    timeseries_length = y.shape[0] 
    # Reshaping x and y so it will look like result of data prepreocessing
    x = x.reshape(-1, 1)
    y = y.reshape(-1, 1)

    x, y = build_windowed_data(y, window_size)
    print(f'Input shape = {x.shape} Output shape = {y.shape}')
    print(f'Timeseriess length = {timeseries_length}')
    print(f'Batch size = {x.shape[0]}')
    print(f'Time steps = {x.shape[1]}')
    print(f'Number of features = {x.shape[2]}')
    

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--csv_file',
                        help='directory where training data is stored',
                        type=str,
                        required=True)
    parser.add_argument('-w', '--window_size',
                        help='Difference in minutes between two steps',
                        type=int,
                        default=32)
    parser.add_argument('-b', '--bias_column',
                        help='name of clock bias column in csv',
                        type=str,
                        default='Clock_bias')
    parser.add_argument('-e', '--epoch_column',
                        help='name of epoch column in csv output',
                        type=str,
                        default='Epoch')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    main(args.csv_file, args.window_size, args.bias_column, args.epoch_column)
