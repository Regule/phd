'''
This script takes train, test and validation csv files then either loads neural network or trains
a new one. If only validation set is given no training occures.
'''


#==================================================================================================
#                                           IMPORTS
#==================================================================================================

import argparse
import numpy as np

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def main(args):
    observations = pd.read_csv(args.observation_file, sep=';')
    print(observations.head())
    columns = list(observations)
    plt.plot(observations['2'])
    plt.show()

def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-o', '--observation_file', type=str, default=None,
            help='File with training observations')
    return parser.parse_args()

if __name__ == '__main__':
    main(parse_arguments())

