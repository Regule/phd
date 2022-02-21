import argparse
import tensorflow as tf
import numpy as np
import pandas as pd
import os
import sys



#==================================================================================================
#                                     FILE PROCESSING 
#==================================================================================================

def read_data_from_csv(file_name, epoch_column, bias_column):
    data = pd.read_csv(file_name, sep=';')
    X = data.iloc[:,0].to_numpy()
    Y = data.iloc[:,1:].to_numpy()
    return X, Y

def save_to_csv(x, y, csv, epoch_column, bias_column):
    x = list(map(timestamp_to_epoch_str, x))
    data = {epoch_column:x, bias_column:y}
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(csv, sep=';', index=False)

    
def check_for_common_element(list_a, list_b):
    for element in list_a:
        if element in list_b:
            return True
    return False
    
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

def get_network_files(satellites, networks_folder):
    network_names = []
    network_topologies = {}
    network_weights = {}
    for r, d, f in os.walk(networks_folder):
        for file in f:
            file_name, extension = file.split('.')
            file_name = file_name.split('_')
            if 'history' in file_name:
                continue
            sat = file_name[0]
            net = '_'.join(file_name[1:])
            if sat in satellites:
                network_names.append(net)
                if extension == 'json':
                    try:
                        network_topologies[sat][net] = os.path.join(r, file)
                    except KeyError as e:
                        network_topologies[sat] = {}
                        network_topologies[sat][net] = os.path.join(r, file)
                if extension == 'h5':
                    try:
                        network_weights[sat][net] = os.path.join(r, file)
                    except KeyError as e:
                        network_weights[sat] = {}
                        network_weights[sat][net] = os.path.join(r, file)
    return network_names, network_topologies, network_weights


def build_output_file_path(output_dir, sat_name, model_name, ext):
    file_name = '{}_{}.{}'.format(sat_name, model_name, ext)
    return os.path.join(output_dir, file_name)


def build_windowed_data(time_series, window_size):
    windows = []
    outputs = []
    step = 0
    while step + window_size < time_series.shape[0]:
        windows.append(time_series[step:step+window_size])
        outputs.append(time_series[step+window_size])
        step += 1
    print(windows[0])
    return np.asarray(windows), np.asarray(outputs)

#==================================================================================================
#                                      NEURAL NETWORKS
#==================================================================================================


def predict(model, windowed_data, window_size, depth):
    predicted_data = []
    window_size = windowed_data.shape[1]
    feature_count = windowed_data.shape[2]
    print(windowed_data.shape)
    network_inputs = windowed_data.tolist()

    while depth > 0:
        print(f'Depth = {depth}')
        x = np.array(network_inputs.pop(0))
        y = model.predict(x.reshape(1, window_size, feature_count), verbose=0)
        print(f'network observation shape = {x.shape}')
        print(f'network response shape = {y.shape}')
        if len(network_inputs) == 0:
            print(f'Appending prediction')
            predicted_data.append(y[0][0])
            window = x
            print(f'Window size before first element removal = {window.shape}')
            window = np.delete(window, 0, 0)
            print(f'Window size after first element removal = {window.shape}')
            window= np.vstack([window, y])
            #window = window.reshape(window_size, feature_count)
            print(f'Window size after appending response= {window.shape}')
            network_inputs.append(window)
            depth -= 1
    return predicted_data
    

def process_single_satellite(sat_name, net_name, initializer_file, model_file,
                             weights_file, prediction_depth,
                             window_size, output_file, bias_column, epoch_column):
    print(f'Predicting for satellite {sat_name} with network {net_name}')
    network = None
    with open(model_file, 'r') as json_file:
        network = tf.keras.models.model_from_json(json_file.read())
    network.load_weights(weights_file)
    x, y = read_data_from_csv(initializer_file, epoch_column, bias_column)
    windowed_data, _ = build_windowed_data(y, window_size)
    predicted = predict(network, windowed_data, window_size, prediction_depth)
    epochs = build_epochs(preprocessor.timeframe_shifter.t_end, 15, prediction_depth)
    dataframe = pd.DataFrame(data={epoch_column: epochs, bias_column: predicted})
    dataframe.to_csv(os.path.join(output_file, f'{sat_name}_{net_name}.csv'), sep=';', index=False)



def main(satellites, initializer_folder, networks_folder, preprocessors_folder,
         prediction_depth, window_size, output_folder, bias_column, epoch_column):
    satellites = satellites.split(',')
    initializer_files = get_files_from_folder(initializer_folder, 'csv', satellites)
    networks, topologies_files , weights_files = get_network_files(satellites, networks_folder)
    weight_files = get_files_from_folder(networks_folder, 'h5', satellites)
    for satellite in satellites:
       for network in networks:
           print(initializer_files)
           print(topologies_files)
           print(weights_files)
           try:
               process_single_satellite(satellite, network,
                                        initializer_files[satellite],
                                        topologies_files[satellite][network],
                                        weights_files[satellite][network],
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
