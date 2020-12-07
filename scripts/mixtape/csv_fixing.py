import argparse
from datetime import datetime, timedelta
import pandas as pd


def even_older_main(csv_file, bias_column, epoch_column, sampling_period):
    clock_data = pd.read_csv(csv_file, sep=';')
    clock_data.sort_values(epoch_column)
    for row in range(1, clock_data.shape[0]):
        pervious_timestamp = datetime.strptime(clock_data[epoch_column][row-1],'%Y-%m-%d %H:%M:%S')
        current_timestamp = datetime.strptime(clock_data[epoch_column][row],'%Y-%m-%d %H:%M:%S')
        if (current_timestamp - pervious_timestamp).seconds / 60 > sampling_period:
            fill_value = clock_data[bias_column][row]
            target_timestamp = pervious_timestamp + timedelta(minutes=sampling_period)
            if not row == clock_data.shape[0]-1:
                fill_value = (fill_value + clock_data[bias_column][row+1]) / 2
            print(f'Filling timestamp {target_timestamp} with value {fill_value}')


def old_main(csv_file, bias_column, epoch_column, sampling_period):
    clock_data = pd.read_csv(csv_file, sep=';')
    clock_data.sort_values(epoch_column)
    fillings = []
    pervious_timestamp = datetime.strptime(clock_data[epoch_column][0],'%Y-%m-%d %H:%M:%S')
    row = 1
    new_row = 1
    generated = 0
    while row < clock_data.shape[0]:
        current_timestamp = datetime.strptime(clock_data[epoch_column][row],'%Y-%m-%d %H:%M:%S')
        time_diff = (current_timestamp - pervious_timestamp).seconds / 60
        if time_diff > sampling_period:
            fill_value = clock_data[bias_column][row]
            target_timestamp = pervious_timestamp + timedelta(minutes=sampling_period)
            if not row == clock_data.shape[0]-1:
                fill_value = (fill_value + clock_data[bias_column][row+1]) / 2
            fillings.append({epoch_column: target_timestamp, bias_column: fill_value})
            pervious_timestamp = target_timestamp
            print(f'Filling timestamp {target_timestamp} with value {fill_value}')
            generated += 1
        else:
            row += 1
            pervious_timestamp = current_timestamp
        new_row += 1
    print(f'Generated {generated} rows when there is {clock_data.shape[0]} rows in original data')
    print(fillings)
    new_data = clock_data.to_dict('records') + fillings
    new_data = pd.DataFrame(new_data)
    new_data.sort_values(epoch_column)
    new_data.info()
    print(new_data.head())


def str_to_datetime(datetime_str):
    return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')


def main(csv_file, bias_column, epoch_column, sampling_period):
    clock_data = pd.read_csv(csv_file, sep=';')
    clock_data[epoch_column] = clock_data[epoch_column].map(str_to_datetime)
    clock_data.sort_values(epoch_column)
    fillings = []
    pervious_timestamp = clock_data[epoch_column][0]
    row = 1
    new_row = 1
    generated = 0
    while row < clock_data.shape[0]:
        current_timestamp = clock_data[epoch_column][row]
        time_diff = (current_timestamp - pervious_timestamp).seconds / 60
        if time_diff > sampling_period:
            fill_value = clock_data[bias_column][row]
            target_timestamp = pervious_timestamp + timedelta(minutes=sampling_period)
            if not row == clock_data.shape[0]-1:
                fill_value = (fill_value + clock_data[bias_column][row+1]) / 2
            fillings.append({epoch_column: target_timestamp, bias_column: fill_value})
            pervious_timestamp = target_timestamp
            print(f'Filling timestamp {target_timestamp} with value {fill_value}')
            generated += 1
        else:
            row += 1
            pervious_timestamp = current_timestamp
        new_row += 1
    print(f'Generated {generated} rows when there is {clock_data.shape[0]} rows in original data')
    print(fillings)
    new_data = clock_data.to_dict('records') + fillings
    new_data = pd.DataFrame(new_data)
    new_data.sort_values(epoch_column)
    new_data.info()
    print(new_data.head())


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--csv_file',
                        help='directory ',
                        type=str,
                        required=True)
    parser.add_argument('-b', '--bias_column',
                        help='name of clock bias column in csv',
                        type=str,
                        default='Clock_bias')
    parser.add_argument('-e', '--epoch_column',
                        help='name of epoch column in csv output',
                        type=str,
                        default='Epoch')
    parser.add_argument('-p', '--sampling_period',
                        help='time, in minutes, between two measurements or predictions',
                        type=int,
                        default=15)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    main(args.csv_file, args.bias_column, args.epoch_column, args.sampling_period)
