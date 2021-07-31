import argparse
import os
from datetime import datetime, timedelta
import pandas as pd

EPOCH_STR_FORMAT = '%Y-%m-%d %H:%M:%S'

def epoch_str_to_timestamp(epoch_str):
    if epoch_str is None: return None
    return datetime.strptime(epoch_str, EPOCH_STR_FORMAT).timestamp()


def main(csv_file, output_file, first_timestamp, last_timestamp,
         bias_column, epoch_column):
    clock_data = pd.read_csv(csv_file, sep=';')
    clock_data[epoch_column] = clock_data[epoch_column].map(epoch_str_to_timestamp)
    print(f'Before filtering -> {clock_data.shape}')
    print(f'First timestamp = {first_timestamp}')
    print(f'Last timestamp = {last_timestamp}')
    if first_timestamp is not None:
        print(f'Removing entries from before {datetime.utcfromtimestamp(first_timestamp).strftime(EPOCH_STR_FORMAT)}')
        clock_data = clock_data[clock_data[epoch_column] >= first_timestamp]
    if last_timestamp is not None:
        print(f'Removing entries from after {datetime.utcfromtimestamp(last_timestamp).strftime(EPOCH_STR_FORMAT)}')
        clock_data = clock_data[clock_data[epoch_column] <= last_timestamp]
    print(f'After filtering -> {clock_data.shape}')
    clock_data[epoch_column] = clock_data[epoch_column].map(lambda x: datetime.fromtimestamp(x).strftime(EPOCH_STR_FORMAT))
    clock_data.to_csv(output_file, sep=';', index=False)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--csv_file',
                        help='directory ',
                        type=str,
                        required=True)
    parser.add_argument('-o', '--output_file',
                        help='directory ',
                        type=str,
                        required=True)
    parser.add_argument('-f', '--first_timestamp',
                        help='time, in minutes, between two measurements or predictions',
                        type=epoch_str_to_timestamp,
                        default=None)
    parser.add_argument('-l', '--last_timestamp',
                        help='time, in minutes, between two measurements or predictions',
                        type=epoch_str_to_timestamp,
                        default=None)
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
    main(args.csv_file, args.output_file, args.first_timestamp, args.last_timestamp,
         args.bias_column, args.epoch_column)
