'''
This script runs a neuroevolution for agumented topologies on csv data.
'''
import argparse
import neat
import pandas as pd

# Ugly solution with globals as we will not use this library in final
# product anyway.
observations = None
responses = None

def load_data(filename, observation_columns, response_columns):
    dataset = pd.read_csv(filename)

def main(args):
    load_data(args.input, args.observation_columns, args.response_columns)

def parse_column_list(list_str):
    return list(list_str.split(','))

def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--input', type=str, required=True,
            help='Path to csv file with observations and responses')
    parser.add_argument('-o', '--observation_columns', type=parse_column_list,
            required=True,
            help='List of comma separated column names for observations')
    parser.add_argument('-r', '--response_columns', type=parse_column_list,
            required=True,
            help='List of comma separated column names for responses')
    return parser.parse_args()

if __name__ == '__main__':
    main(parse_arguments())
