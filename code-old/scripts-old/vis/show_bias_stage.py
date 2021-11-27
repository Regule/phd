import argparse
from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from io_utils import read_data_from_csv
from time_utils import date_str_to_datetime, epoch_str_to_timestamp
from data_preprocessing import Differentiator, MeanShifter, CustomScaler, TimeReferenceShifter


def main(csv_file, forced_scale, start_timestamp, end_timestamp,
         plot_output, log_output, epoch_column, bias_column, log_scale):
    clock_data = pd.read_csv(csv_file, sep=';')
    clock_data[epoch_column] = clock_data[epoch_column].map(epoch_str_to_timestamp)
    print(f'Number of entries = {clock_data.shape[0]}')
    print(f'First timestamp = {datetime.fromtimestamp(clock_data[epoch_column].min())} ({clock_data[epoch_column].min()})')
    print(f'Last timestamp = {datetime.fromtimestamp(clock_data[epoch_column].max())} ({clock_data[epoch_column].max()})')
    
    if start_timestamp is not None:
        start_timestamp = start_timestamp.timestamp()
        clock_data = clock_data[clock_data[epoch_column] >= start_timestamp]
    if end_timestamp is not None:
        end_timestamp = end_timestamp.timestamp()
        clock_data = clock_data[clock_data[epoch_column] <= end_timestamp]

    sat_name = csv_file.split('/')[-1].split('.')[0]
    x = clock_data.iloc[:][epoch_column].values
    y = clock_data.iloc[:][bias_column].values
    timeframe_shifter = TimeReferenceShifter()
    x = timeframe_shifter.fit_transform(x)

    fig = plt.figure()
    ax_raw = fig.add_subplot(2, 2, 1)
    ax_diffed = fig.add_subplot(2, 2, 2)
    ax_shifted = fig.add_subplot(2, 2, 3)
    ax_normalized = fig.add_subplot(2, 2, 4)
        
    ax_raw.plot(x, y)
    ax_raw.set_xlabel('Measurement')
    ax_raw.set_ylabel('Bias in [ns]')
 
    diff = Differentiator()
    y = diff.fit_transform(y)
    x = x[1:]
    ax_diffed.plot(x, y)
    ax_diffed.set_xlabel('Measurement')
    ax_diffed.set_ylabel('Bias [ns]')
    
    mean_shifter = MeanShifter()
    y = mean_shifter.fit_transform(y)
    ax_shifted.plot(x, y)
    ax_shifted.set_xlabel('Measurement')
    ax_shifted.set_ylabel('Bias [ns]')
    
    scaler = CustomScaler()
    if forced_scale is not None:
        y = CustomScaler(forced_scale).transform(y)
    else:
        y = CustomScaler().fit_transform(y)
    ax_normalized.plot(x, y)
    ax_normalized.set_xlabel('Measurement')
    ax_normalized.set_ylabel('Bias (scaled)')

    plt.suptitle(f'Clock bias in different preprocessing stages for satellite {sat_name}')
    plt.show()

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--csv_file',
                        help='directory where training data is stored',
                        type=str,
                        required=True)
    parser.add_argument('-p', '--plot_output',
                        help='directory where training data is stored',
                        type=str,
                        default=None)
    parser.add_argument('-l', '--log_output',
                        help='directory where training data is stored',
                        type=str,
                        default=None)
    parser.add_argument('-f', '--forced_scale',
                        help='directory where training data is stored',
                        type=float,
                        default=None)
    parser.add_argument('-s', '--start_timestamp',
                        help='directory where igu predictions are stored',
                        type=date_str_to_datetime,
                        default=None)
    parser.add_argument('-n', '--end_timestamp',
                        help='End date for after which prediction will end',
                        type=date_str_to_datetime,
                        default=None)
    parser.add_argument('-b', '--bias_column',
                        help='name of clock bias column in csv',
                        type=str,
                        default='Clock_bias')
    parser.add_argument('-e', '--epoch_column',
                        help='name of epoch column in csv output',
                        type=str,
                        default='Epoch')
    parser.add_argument('--log_scale',
                        help='directory where training data is stored',
                        action='store_true')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    main(args.csv_file, args.forced_scale, args.start_timestamp, args.end_timestamp,
         args.plot_output, args.log_output, args.epoch_column, args.bias_column, args.log_scale)
