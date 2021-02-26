import sys
import os
import argparse
import pandas as pd
import datetime

measured_data = {}
predicted_data = {}


def convinient_conversion_sp3_line(txt):
    try:
        return int(txt)
    except Exception:
        try:
            return float(txt)
        except Exception:
            return txt


def update_entries(satellites, sp3_file_name: str, epoch_column: str, bias_column: str):
    print(f'Processing file {sp3_file_name}')
    with open(sp3_file_name, 'r') as sp3_file:
        epoch = 0.0
        epoch_set = False
        for line in sp3_file:
            if line[0] in '#+%/':
                continue # Those lines do not interest us
            elif line == 'EOF':
                break # This line indicates end of sp3 file
            elif line[0] == '*':
                line = line[1:].split()
                line = line[:-1]+line[-1].split('.')
                line = list(map(int,line))
                line[-1] = line[-1]*10
                epoch = datetime.datetime(line[0], line[1], line[2], line[3], line[4], line[5])
                if not epoch_set:
                    epoch_set = True
                    print(f'Epochs starts at {epoch}')
            else:
                line = list(map(convinient_conversion_sp3_line,line.split()))
                try:
                    sat_name = line[0][1:]
                    clock_bias = line[4]
                    epoch_str = str(epoch)
                    data = predicted_data if 'P' in line else measured_data
                    if sat_name in satellites:
                        if sat_name not in data:
                            print(f'Creating new dataframe for satellite {sat_name}')
                            data[sat_name] = {epoch_column:[], bias_column:[]}
                        data[sat_name][epoch_column].append(epoch_str)
                        data[sat_name][bias_column].append(clock_bias)
                except Exception as e:
                    print(f'Encountered exception {e} for line {line}.')
        print(f'Epochs ends at {epoch}')

def main(satellites, sp3_dir, measured_dir, predicted_dir, epoch_column, bias_column):
    for r, d, f in os.walk(sp3_dir):
        for file in f:
            if '.sp3' in file:
                update_entries(satellites.split(','), os.path.join(r, file),
                               epoch_column, bias_column)
    for sat, data in measured_data.items():
        dataframe = pd.DataFrame(data)
        dataframe.to_csv(os.path.join(measured_dir,f'{sat}.csv'), sep=';', index=False)
    for sat, dataframe in predicted_data.items():
        dataframe = pd.DataFrame(data)
        dataframe.to_csv(os.path.join(predicted_dir,f'{sat}.csv'),  sep=';', index=False)



def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sp3_dir',
                        help='directory containing sp3 files',
                        type=str,
                        required=True)
    parser.add_argument('-a', '--satellites',
                        help='List of satellites for which networks will be generated',
                        type=str,
                        default='G01,G05,G07,G08,G12,G16,G19,G20,G23,G24,G26,G28,G30,G02,G03,G06,G09,G10,G13,G15,G25,G27,G29,G31,G11,G14,G17,G21,G22,G32')
    parser.add_argument('-m', '--measured_dir',
                        help='directory to which csv files with measured data will be saved',
                        type=str,
                        required=True)
    parser.add_argument('-p', '--predicted_dir',
                        help='directory to which csv files with measured data will be saved',
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

    return parser.parse_args()



if __name__ == '__main__':
    args = parse_arguments()
    main(args.satellites, args.sp3_dir, args.measured_dir, args.predicted_dir, args.epoch_column, args.bias_column)
