import argparse
import os
from datetime import datetime, timedelta
from time_utils import epoch_str_to_timestamp, EPOCH_STR_FORMAT, date_str_to_timestamp
import pandas as pd



def filter_satellite_data(sat_name, sat_file, output_directory, first_timestamp,
                          last_timestamp, bias_column, epoch_column):
    clock_data = pd.read_csv(sat_file, sep=';')
    clock_data[epoch_column] = clock_data[epoch_column].map(epoch_str_to_timestamp)
    if first_timestamp is not None:
        clock_data = clock_data[clock_data[epoch_column] >= first_timestamp]
    if last_timestamp is not None:
        clock_data = clock_data[clock_data[epoch_column] <= last_timestamp]
    clock_data[epoch_column] = clock_data[epoch_column].map(lambda x: datetime.fromtimestamp(x).strftime(EPOCH_STR_FORMAT))
    clock_data.to_csv(os.path.join(output_directory, f'{sat_name}.csv'), sep=';', index=False)


def main(satellites, csv_dir, output_directory, first_timestamp,
         last_timestamp, bias_column, epoch_column):
    satellites = satellites.split(',')
    for r, d, f in os.walk(csv_dir):
        for file in f:
            if '.csv' in file:
                sat_name = file.split('.')[0]
                if sat_name in satellites:
                    filter_satellite_data(sat_name, os.path.join(r, file), output_directory,
                                          first_timestamp, last_timestamp, bias_column,
                                          epoch_column)



def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--satellites',
                        help='List of satellites for which networks will be generated',
                        type=str,
                        default='G01,G05,G07,G08,G12,G16,G19,G20,G24,G26,G28,G30,G02,G03,G06,G09,G10,G13,G15,G25,G27,G29,G31,G11,G14,G17,G21,G22,G32')
    parser.add_argument('-c', '--csv_dir',
                        help='directory ',
                        type=str,
                        required=True)
    parser.add_argument('-o', '--output_directory',
                        help='directory ',
                        type=str,
                        required=True)
    parser.add_argument('-f', '--first_timestamp',
                        help='time, in minutes, between two measurements or predictions',
                        type=date_str_to_timestamp,
                        default=None)
    parser.add_argument('-l', '--last_timestamp',
                        help='time, in minutes, between two measurements or predictions',
                        type=date_str_to_timestamp,
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
    main(args.satellites, args.csv_dir, args.output_directory, args.first_timestamp,
         args.last_timestamp, args.bias_column, args.epoch_column)
