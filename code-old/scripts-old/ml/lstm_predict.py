import argparse
import tensorflow as tf
import numpy as np
import pandas as pd
import os
from io_utils import get_files_from_folder, get_network_files, read_data_from_csv
from time_utils import build_epochs
from data_preprocessing import DataPreprocessor, build_windowed_data

def predict(model, windowed_data, window_size, depth):
    predicted_data = []
    network_inputs = windowed_data.tolist()

    while depth > 0:
        x = np.array(network_inputs.pop(0))
        y = model.predict(x.reshape(1, window_size, 1), verbose=0)

        if len(network_inputs) == 0:
            predicted_data.append(y[0][0])
            window = np.delete(x, 0, 0)
            window= np.append(window, y)
            network_inputs.append(window)
            depth -= 1
    return predicted_data
    

def process_single_satellite(sat_name, net_name, initializer_file, model_file,
                             weights_file, preprocessor_file, prediction_depth,
                             window_size, output_file, bias_column, epoch_column):
    print(f'Predicting for satellite {sat_name} with network {net_name}')
    preprocessor = DataPreprocessor.load_json(preprocessor_file)
    network = None
    with open(model_file, 'r') as json_file:
        network = tf.keras.models.model_from_json(json_file.read())
    network.load_weights(weights_file)
    x, y = read_data_from_csv(initializer_file, epoch_column, bias_column)
    preprocessor.fit_differentiator(y)
    x, y = preprocessor.transform(x, y)
    windowed_data, _ = build_windowed_data(y, window_size)
    predicted = predict(network, windowed_data, window_size, prediction_depth)
    epochs = build_epochs(preprocessor.timeframe_shifter.t_end, 15, prediction_depth)
    dataframe = pd.DataFrame(data={epoch_column: epochs, bias_column: predicted})
    dataframe.to_csv(os.path.join(output_file, f'{sat_name}_{net_name}.csv'), sep=';', index=False)



def main(satellites, initializer_folder, networks_folder, preprocessors_folder,
         prediction_depth, window_size, output_folder, bias_column, epoch_column):
    satellites = satellites.split(',')
    initializer_files = get_files_from_folder(initializer_folder, 'csv', satellites)
    preprocessor_files = get_files_from_folder(preprocessors_folder, 'json', satellites)
    print(preprocessor_files)
    networks, topologies_files , weights_files = get_network_files(satellites, networks_folder)
    weight_files = get_files_from_folder(networks_folder, 'h5', satellites)
    for satellite in satellites:
       for network in networks:
           try:
               process_single_satellite(satellite, network,
                                        initializer_files[satellite],
                                        topologies_files[satellite][network],
                                        weights_files[satellite][network],
                                        preprocessor_files[satellite],
                                        prediction_depth, window_size, output_folder,
                                        bias_column, epoch_column)
           except KeyError as e:
               print(f'Key error ---> {e}')

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--satellites',
                        help='List of satellites for which networks will be generated',
                        type=str,
                        default='G01,G05,G07,G08,G12,G16,G19,G20,G23,G24,G26,G28,G30,G02,G03,G06,G09,G10,G13,G15,G25,G27,G29,G31,G11,G14,G17,G21,G22,G32')
    parser.add_argument('-i', '--initializers_folder',
                        help='Folder that contains initializers for network',
                        type=str,
                        default='local/initializers')
    parser.add_argument('-n', '--networks_folder',
                        help='File that contains topology, weights and training history of neural network',
                        type=str,
                        default='local/networks')
    parser.add_argument('-r', '--preprocessors_folder',
                        help='File that contains preprocessors configuration',
                        type=str,
                        default='local/preprocessors')
    parser.add_argument('-d', '--prediction_depth',
                        help='How many steps should be predicted',
                        type=int,
                        default=15)
    parser.add_argument('-w', '--window_size',
                        help='Sliding window size',
                        type=int,
                        default=32)
    parser.add_argument('-o', '--output_folder',
                        help='Folder to which prediction outputs will be saved',
                        type=str,
                        default='local/lstm_predicted')
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
    main(args.satellites, args.initializers_folder, args.networks_folder, args.preprocessors_folder,
         args.prediction_depth, args.window_size, args.output_folder, args.bias_column,
         args.epoch_column)
