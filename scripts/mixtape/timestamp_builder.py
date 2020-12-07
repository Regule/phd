import argparse
import numpy as np
from datetime import datetime, timedelta

def date_str_to_timestamp(epoch_str):
    return datetime.strptime(epoch_str,'%Y-%m-%d')


def main(start, end, delta):
    timestamps = []
    timestamp = start
    delta = timedelta(minutes=delta)
    while timestamp < end:
        timestamps.append(timestamp)
        timestamp += delta
    timestamps = np.asarray(list(map(lambda x: x.timestamp(), timestamps)))
    print(timestamps)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start',
                        help='csv file',
                        type=date_str_to_timestamp,
                        required=True)
    parser.add_argument('-e', '--end',
                        help='name of clock bias column in csv',
                        type=date_str_to_timestamp,
                        default='Clock_bias')
    parser.add_argument('-d', '--delta',
                        help='name of epoch column in csv output',
                        type=int,
                        default=15)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    main(args.start, args.end, args.delta)
