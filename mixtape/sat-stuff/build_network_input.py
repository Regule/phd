'''
This script takes a clock bias csv and turns it into and observation set for prediction
algorithm.
'''


#==================================================================================================
#                                           IMPORTS
#==================================================================================================
import argparse

import pandas as pd
import numpy as np


#==================================================================================================
#                                        DATA PROCESSING
#==================================================================================================


def data_from_csv(file_name):
    data = pd.read_csv(file_name, sep=';')
    observation = data.iloc[:,0].to_numpy()
    reaction = data.iloc[:,1:].to_numpy()
    return observation, reaction

def build_input_with_derivatives(timeseries, derivative_level):
    derivative = timeseries
    derivatives = [derivative.reshape(derivative.shape[0]), ]
    for level in range(derivative_level):
        derivative = np.diff(derivative, axis=0)
        padding = np.zeros(level+1)
        derivatives.append(np.hstack([padding,derivative.reshape(derivative.shape[0])]))
    return np.array(derivatives).T


def write_observation_dataset(observation, file_name):
    dataset = pd.DataFrame(observation)
    dataset.to_csv(file_name, sep=';')

#==================================================================================================
#                                       UTILITY FUNCTIONS
#==================================================================================================


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--input_file', type=str, default=None,
            help='File with training observations')
    parser.add_argument('-d', '--derivative_level', type=int, default=2,
            help='To what degree a derivative should be included in input')
    parser.add_argument('-o', '--output_file', type=str, required=True,
            help='File to which output will be saved')
    return parser.parse_args()


#==================================================================================================
#                                       MAIN FUNCTION
#==================================================================================================

def main(args):
    observation, reaction = data_from_csv(args.input_file)
    observation = build_input_with_derivatives(reaction, args.derivative_level)
    write_observation_dataset(observation,args.output_file)

if __name__ == '__main__':
    main(parse_arguments())
