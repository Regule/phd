import argparse
import pandas as pd
import os


def main(csv_dir, output_dir, log_dir, bias_column, epoch_column, sampling_period):
    pass

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--masured_dir',
                        help='directory with measured readouts',
                        type=str,
                        required=True)
    parser.add_argument('-p', '--predicted_dir',
                        help='directory with predicted readouts',
                        type=str,
                        required=True)
    parser.add_argument('-M', '--masured_fixed_dir',
                        help='directory with fixed measured readouts',
                        type=str,
                        required=True)
    parser.add_argument('-P', '--predicted_fixed_dir',
                        help='directory with fixed predicted readouts',
                        type=str,
                        required=True)
    parser.add_argument('-o', '--output_root',
                        help='Root of output directory tree',
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
    main(args.measured_dir, args.predicted_dir, args.mesured_fixed_dir, args.predicted_fixed_dir,
         args.output_root, args.bias_column, args.epoch_column)
