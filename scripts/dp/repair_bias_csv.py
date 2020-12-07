import argparse
import os
import pandas as pd
from datetime import datetime, timedelta

MSG_SAT_INFO = 'Attempting to fix csv for satellite {}.'
MSG_FIX_SUMMARY = 'For satellite {} generated {} entries for {} original entries. {}'
MSG_NO_FIX = 'No fixing reqired.'
MSG_FIX = 'Fixing broken csv.'

def fix_csv(csv_file, output_file, log_file, bias_column, epoch_column, sampling_period):
    sat_name = csv_file.split('.')[0].split('/')[-1]
    print(MSG_SAT_INFO.format(sat_name))
    clock_data = pd.read_csv(csv_file, sep=';')
    clock_data[epoch_column] = clock_data[epoch_column].map(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
    clock_data.sort_values(epoch_column)
    
    generated_entries = []
    idx = 0
    last_timestamp = clock_data[epoch_column][0]
    while idx < clock_data.shape[0]:
        timestamp = clock_data[epoch_column][idx]
        time_diff = (timestamp - last_timestamp).seconds / 60
        if time_diff > sampling_period:
            generated_bias = clock_data[bias_column][idx]
            generated_timestamp = last_timestamp + timedelta(minutes=sampling_period)
            if not idx == clock_data.shape[0]-1:
                generated_bias = (generated_bias + clock_data[bias_column][idx+1]) / 2
            generated_entries.append({epoch_column: generated_timestamp, bias_column: generated_bias})
            last_timestamp = generated_timestamp
        else:
            last_timestamp = timestamp
            idx += 1
    summary = MSG_FIX_SUMMARY.format(sat_name, len(generated_entries), clock_data.shape[0],
                                     MSG_FIX if len(generated_entries)>0 else MSG_NO_FIX)
    print(summary)
    
    if len(generated_entries) != 0:
        fixed_data = clock_data.to_dict('records') + generated_entries
        fixed_data = pd.DataFrame(fixed_data)
        fixed_data.sort_values(epoch_column)
        fixed_data.to_csv(output_file, sep=';', index=False)
        with open(log_file, 'w') as log:
            log.write(summary)
            log.write('\n')
            log.write('Added entries : ')
            log.write('\n')
            for entry in generated_entries:
                log.write(f'{entry}\n')
        


def main(csv_dir, output_dir, log_dir, bias_column, epoch_column, sampling_period):
    for r, d, f in os.walk(csv_dir):
        for file in f:
            if '.csv' in file:
                log_file = '{}.txt'.format(file.split('.')[0])
                fix_csv(os.path.join(r,file),os.path.join(output_dir,file),
                        os.path.join(log_dir,log_file), bias_column,
                        epoch_column, sampling_period)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--csv_dir',
                        help='directory ',
                        type=str,
                        required=True)
    parser.add_argument('-l', '--log_dir',
                        help='directory to which logs will be saved',
                        type=str,
                        required=True)
    parser.add_argument('-o', '--output_dir',
                        help='Directory to which fixed csv will be saved',
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
    main(args.csv_dir, args.output_dir, args.log_dir, args.bias_column, args.epoch_column,
         args.sampling_period)
