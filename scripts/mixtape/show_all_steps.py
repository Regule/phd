import argparse
import pandas as pd
import numpy as np

from data_preprocessing import DataPreprocessor
from time_utils import epoch_str_to_timestamp

def main(prediction_file, reference_file, preprocessor_file,
         bias_column,epoch_column):
    preprocessor = DataPreprocessor.load_json(preprocessor_file)
    prediction = pd.read_csv(prediction_file, sep=';')
    reference = pd.read_csv(reference_file, sep=';')
    x_pred, y_pred = preprocessor.transform(np.asarray(list(map(epoch_str_to_timestamp, prediction[epoch_column]))), prediction[bias_column])
    x_ref, y_ref = preprocessor.transform(np.asarray(list(map(epoch_str_to_timestamp, reference[epoch_column]))), reference[bias_column])

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--prediction_file',
                        help='file with our predictions',
                        type=str,
                        required=True)
    parser.add_argument('-r', '--reference_file',
                        help='file with refrerence values',
                        type=str,
                        required=True)
    parser.add_argument('-s', '--preprocessor_file',
                        help='file with preprocessor data',
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
    main(args.prediction_file, args.reference_file, args.preprocessor_file,
         args.bias_column, args.epoch_column)
