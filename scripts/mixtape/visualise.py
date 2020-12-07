import argparse
import sys
from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from io_utils import read_data_from_csv
from time_utils import date_str_to_datetime, epoch_str_to_timestamp
from data_preprocessing import Differentiator, MeanShifter, CustomScaler, TimeReferenceShifter


def removeOutliers(x, y, outlierConstant):
    y_hist = np.histogram(y, bins=20)
    
    

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
    plt.rcParams.update({'font.size': 20})
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    
    x = clock_data.iloc[:][epoch_column].values
    y = clock_data.iloc[:][bias_column].values


    timeframe_shifter = TimeReferenceShifter()
    plt_x = timeframe_shifter.fit_transform(x)
    ax.plot(plt_x, y, color='red')
    plt.title(f'Raw clock bias for satellite {sat_name}')
    plt.xlabel('Measurement')
    plt.ylabel('Bias in nanoseconds')
    plt.show()


    diff = Differentiator()
    y = diff.fit_transform(y)
    x = x[1:]

    timeframe_shifter = TimeReferenceShifter()
    x = timeframe_shifter.fit_transform(x)

    ax.plot(x, y, color='red')
    plt.title(f'Differentiated clock bias for satellite {sat_name}')
    plt.xlabel('Measurement')
    plt.ylabel('Bias in nanoseconds')
    plt.show()


    mean_shifter = MeanShifter()
    y = mean_shifter.fit_transform(y)

    plt.hist(y, bins=100, log=True, histtype='stepfilled')
    plt.show()

    
    scaler = CustomScaler()
    if forced_scale is not None:
        y = CustomScaler(forced_scale).transform(y)
    else:
        y = CustomScaler().fit_transform(y)

    z_scores = stats.zscore(y)

    processed = pd.DataFrame({epoch_column:x, bias_column:y, 'z_score':z_scores})
    print(f'Number of entries = {clock_data.shape[0]}')
    print(f'First timestamp = {processed[epoch_column].min()}')
    print(f'Last timestamp = {processed[epoch_column].max()}')
    #x = clock_data.iloc[:][epoch_column].values
    
    #x = x[(np.abs(stats.zscore(y)) < 10).all()]
    #y = y[(np.abs(stats.zscore(y)) < 10).all()]
    

    x = x.reshape(-1,1)
    y = y.reshape(-1,1)


    if log_scale:
        ax.set_yscale('log')
    ax.plot(x, y, color='red', label='Satellite readouts')
    plt.title(f'Readout for satellite {sat_name}')
    plt.xlabel('Time (UNIX timestamp)')
    plt.ylabel('Bias in nanoseconds')
    plt.legend()
    plt.show()


    plt.hist(y, bins=100, log=True, histtype='stepfilled')
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
