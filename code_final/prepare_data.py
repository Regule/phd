#==================================================================================================
#                                           IMPORTS
#==================================================================================================
import argparse

import pandas as pd
import numpy as np
import os


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

def parse_single_sat(input_file, output_file, derivative_level):
    observation, reaction = data_from_csv(input_file)
    observation = build_input_with_derivatives(reaction, derivative_level)
    write_observation_dataset(observation, output_file)

#==================================================================================================
#                                       UTILITY FUNCTIONS
#==================================================================================================
def get_files_from_folder(folder, extension, satellites=None):
    files = {}
    extension = f'.{extension}'
    for r, d, f in os.walk(folder):
        for file in f:
            if extension in file:
                file_name = file.split('.')[0]
                if satellites is None or check_for_common_element(satellites, file_name.split('_')):
                    files[file_name.split('_')[0]] = os.path.join(r, file)
    return files

def build_output_file_path(output_dir, sat_name, ext):
    file_name = '{}.{}'.format(sat_name, ext)
    return os.path.join(output_dir, file_name)

def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--input_folder', type=str, default=None,
            help='File with training observations')
    parser.add_argument('-d', '--derivative_level', type=int, default=2,
            help='To what degree a derivative should be included in input')
    parser.add_argument('-o', '--output_folder', type=str, required=True,
            help='File to which output will be saved')
    return parser.parse_args()

#==================================================================================================
#                                       MAIN FUNCTION
#==================================================================================================

def main(args):
    input_files = get_files_from_folder(args.input_folder, 'csv')
    for sat, path in input_files.items():
        print(f'Parsing satellite {sat}')
        out_file = build_output_file_path(args.output_folder, sat, 'csv')
        parse_single_sat(path, out_file,args.derivative_level)


if __name__ == '__main__':
    main(parse_arguments())
