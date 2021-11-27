import argparse
import pandas as pd
import datetime


def convinient_conversion_sp3_line(txt):
    try:
        return int(txt)
    except Exception:
        try:
            return float(txt)
        except Exception:
            return txt


def main(sp3_file_name, bias_column, epoch_column):
    data = {}
    with open(sp3_file_name, 'r') as sp3_file:
        epoch = 0
        for line in sp3_file:
            if line[0] in '#+%/':
                continue
            elif line[0] == '*':
                line = line[1:].split()
                line = line[:-1]+line[-1].split('.')
                line = list(map(int,line))
                line[-1] = line[-1]*10
                epoch = datetime.datetime(line[0], line[1], line[2], line[3], line[4], line[5])#.replace(tzinfo=datetime.timezone.utc).timestamp()
                print(f'Updating epoch to {epoch}')
            else:
                try:
                    line = list(map(convinient_conversion_sp3_line,line.split()))
                    sat_name = line[0][1:]
                    clock_bias = line[4]
                    if sat_name not in data:
                        print(f'Creating new dataframe for satellite {sat_name}')
                        dataframe = pd.DataFrame(data={epoch_column: [epoch], bias_column: [clock_bias]})
                        data[sat_name] = dataframe
                    else:
                        data[sat_name] = data[sat_name].append({epoch_column: epoch, bias_column: clock_bias}, ignore_index=True)
                except Exception as e:
                    print(f'Encountered exception {e} for line {line}.')
    print(f'Loaded data for {len(data.keys())} satellites')
    data['G01'].info()
    print(data['G01'].head())
    

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sp3_file',
                        help='sp3 file name',
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
    main(args.sp3_file, args.bias_column, args.epoch_column)
