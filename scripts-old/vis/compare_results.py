import argparse
import os
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from math import sqrt

def prepare_files(lstm_dir: str, igu_dir: str, ref_dir: str):
    references = {}
    igu_predictions = {}
    lstm_predictions = {}
    satellites = []
    networks = []
    
    for r, d, f in os.walk(ref_dir):
        for file in f:
            if '.csv' in file:
                satellite = file.split('.')[0]
                satellites.append(satellite)
                references[satellite]=(os.path.join(r, file))
                
    for r, d, f in os.walk(igu_dir):
        for file in f:
            if '.csv' in file:
                satellite = file.split('.')[0]
                igu_predictions[satellite]=(os.path.join(r, file))

    for r, d, f in os.walk(lstm_dir):
        for file in f:
            if '.csv' in file:
                filename = file.split('.')[0]
                satellite, network = filename.split('_')
                networks.append(network)
                try:
                    lstm_predictions[satellite][network]=(os.path.join(r, file))
                except KeyError:
                    lstm_predictions[satellite] = {}
                    lstm_predictions[satellite][network]=(os.path.join(r, file))
                    
    return references, igu_predictions, lstm_predictions, satellites, networks


def compare_results(lstm_dir: str, igu_dir: str, ref_dir: str, out_file:str):
    IGU_COLUMN = 'igu'
    
    references, igu_predictions, lstm_predictions, satellites, networks = prepare_files(lstm_dir, igu_dir, ref_dir)
    rows = []
    for satellite in references.keys():
        comparition = {}
        comparition['satellite'] = satellite
        ref_biases = pd.read_csv(references[satellite], sep=';', header=0,
                                 parse_dates=[0], index_col=0,
                                 squeeze=True).values
        igu_pred_biases = pd.read_csv(igu_predictions[satellite], sep=';',
                                      header=0, parse_dates=[0],
                                      index_col=0, squeeze=True).values
        igu_p_mae = mean_absolute_error(ref_biases, igu_pred_biases)
        igu_p_mse = mean_squared_error(ref_biases, igu_pred_biases)
        print("%10s => MAE = %.4f MSE = %.4f RMS = %.4f" % ('IGU-P', igu_p_mae, igu_p_mse, sqrt(igu_p_mse)))
        comparition[IGU_COLUMN] = igu_p_mae 

        for network in lstm_predictions[satellite].keys():
            lstm_pred_biases = pd.read_csv(lstm_predictions[satellite][network], sep=';',
                                           header=0, parse_dates=[0],
                                           index_col=0, squeeze=True).values
            lstm_mae = mean_absolute_error(ref_biases, lstm_pred_biases)
            lstm_mse = mean_squared_error(ref_biases, lstm_pred_biases)
            print("%10s => MAE = %.4f MSE = %.4f RMS = %.4f" % ('LSTM', lstm_mae, lstm_mse, sqrt(lstm_mse)))
            comparition[network] = lstm_mae
        print(comparition)
        rows.append(comparition)
    comparitions = pd.DataFrame(rows)
    comparitions['best'] = comparitions.loc[:, [IGU_COLUMN]+networks].idxmin(axis=1)
    comparitions.to_csv(out_file, sep=';', index=False)

def parse_arguments()-> argparse.ArgumentParser:
    desc = '''Script uses provided input data to teach a neural network'''
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-l', '--lstm_dir', help='directory with lstm predictions')
    parser.add_argument('-i', '--igu_dir', help='directory with igu predictions')
    parser.add_argument('-r', '--ref_dir', help='directory with reference')
    parser.add_argument('-o', '--out_file', help='output file')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    compare_results(args.lstm_dir, args.igu_dir, args.ref_dir, args.out_file)
