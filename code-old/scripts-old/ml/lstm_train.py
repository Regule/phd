import sys
import argparse
import tensorflow as tf
import pandas as pd
from keras import regularizers
from io_utils import read_data_from_csv, get_files_from_folder, build_output_file_path
from data_preprocessing import DataPreprocessor, build_windowed_data


def build_stage_zero_model(input_size, input_shape, hidden_factor):
    hidden_size = int(input_size*hidden_factor)
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.LSTM(input_size,
                                   dropout=0.2,
                                   recurrent_dropout=0.2,
                                   return_sequences=True,
                                   activation='relu',
                                   kernel_regularizer=regularizers.l2(0.001),
                                   stateful=False,
                                   input_shape=input_shape
                                   ))
    model.add(tf.keras.layers.LSTM(hidden_size,
                                   dropout=0.5,
                                   recurrent_dropout=0.5,
                                   activation='relu',
                                   kernel_regularizer=regularizers.l2(0.001),
                                   stateful=False
                                   ))
    model.add(tf.keras.layers.Dense(1,
                                    activation='linear'
                                    ))
    model.compile(loss='mse', optimizer='rmsprop')
    return model


def build_lstm(input_shape, hidden_factor, input_dropout, input_recurrent_dropout,
               hidden_dropout, hidden_recurrent_dropout, input_regularization,
               hidden_regularization, optimizer):
    input_size = input_shape[1]
    input_shape = (input_shape[1], input_shape[2])
    hidden_size = int(input_size*hidden_factor)
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.LSTM(input_size,
                                   dropout=input_dropout,
                                   recurrent_dropout=input_recurrent_dropout,
                                   return_sequences=True,
                                   activation='relu',
                                   kernel_regularizer=regularizers.l2(input_regularization),
                                   stateful=False,
                                   input_shape=input_shape
                                   ))
    model.add(tf.keras.layers.LSTM(hidden_size,
                                   dropout=hidden_dropout,
                                   recurrent_dropout=hidden_recurrent_dropout,
                                   activation='relu',
                                   kernel_regularizer=regularizers.l2(hidden_regularization),
                                   stateful=False
                                   ))
    model.add(tf.keras.layers.Dense(1,
                                    activation='linear'
                                    ))
    model.compile(loss='mse', optimizer=optimizer)
    return model


def build_network_models(input_shape, experiment_phase=4):
    models = {}
    if experiment_phase == 0:
        models['poc'] = build_stage_zero_model(input_shape[1], (input_shape[1], input_shape[2]), 2)
    elif experiment_phase == 4:
        models['2_low'] = build_lstm(input_shape, 2, 0.1, 0.01, 0.1, 0.01, 0.001, 0.001, 'rmsprop')
        models['2_high'] = build_lstm(input_shape, 2, 0.5, 0.1, 0.5, 0.1, 0.001, 0.001, 'rmsprop')
        models['2_no'] = build_lstm(input_shape, 2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'rmsprop')
        models['8_low'] = build_lstm(input_shape, 8, 0.1, 0.01, 0.1, 0.01, 0.001, 0.001, 'rmsprop')
        models['8_high'] = build_lstm(input_shape, 8, 0.5, 0.1, 0.5, 0.1, 0.001, 0.001, 'rmsprop')
        models['8_no'] = build_lstm(input_shape, 8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'rmsprop')
    else:
        print(f'Experiment phase {experiment_phase} unavailable in this implementation.')
        sys.exit()
    #models['1_low'] = build_lstm(input_shape, 1, 0.1, 0.01, 0.1, 0.01, 0.001, 0.001, 'rmsprop')
    #models['1_high'] = build_lstm(input_shape, 1, 0.5, 0.1, 0.5, 0.1, 0.001, 0.001, 'rmsprop')
    #models['1_no'] = build_lstm(input_shape, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'rmsprop')
    #models['4_low'] = build_lstm(input_shape, 4, 0.1, 0.01, 0.1, 0.01, 0.001, 0.001, 'rmsprop')
    #models['4_high'] = build_lstm(input_shape, 4, 0.5, 0.1, 0.5, 0.1, 0.001, 0.001, 'rmsprop')
    #models['4_no'] = build_lstm(input_shape, 4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'rmsprop')
    return models


def train_single_network(sat_name, training_file, validation_file, networks_folder,
                         preprocessors_folder, window_size, epochs, bias_column,
                         epoch_column, experiment_phase):
    preprocessor = DataPreprocessor()
    
    x_tr, y_tr = read_data_from_csv(training_file, epoch_column, bias_column)
    x_tr, y_tr = preprocessor.fit_transform(x_tr, y_tr)   
    x_tr, y_tr = build_windowed_data(y_tr, window_size)
    x_val, y_val = read_data_from_csv(validation_file, epoch_column, bias_column)
    x_val, y_val = preprocessor.transform(x_val, y_val)
    x_val, y_val = build_windowed_data(y_val , window_size)
    preprocessor.to_json(build_output_file_path(preprocessors_folder, sat_name, 'preprocessor', 'json'))
    
    networks = build_network_models(x_tr.shape, experiment_phase)
    for net_name, network in networks.items():
        history = network.fit(x_tr, y_tr, epochs=epochs, batch_size=32,
                              validation_data=(x_val, y_val), shuffle=False)
        model_json = network.to_json()
        with open(build_output_file_path(networks_folder, sat_name, net_name, 'json'), "w") as json_file:
            json_file.write(model_json)
        network.save_weights(build_output_file_path(networks_folder, sat_name, net_name, 'h5'))
        history = pd.DataFrame(history.history)
        history.to_csv(build_output_file_path(networks_folder, sat_name, f'{net_name}_history', 'csv'),
                       sep=';', index=False)
    
    
    

def main(satellites, training_directory, validation_directory, window_size, epochs,
         networks_folder, preprocessors_folder, bias_column, epoch_column, experiment_phase):
    satellite_data_training = get_files_from_folder(training_directory, 'csv')
    satellite_data_validation = get_files_from_folder(validation_directory, 'csv')
    for sat_name in satellites.split(','):
        try:
            training_file = satellite_data_training[sat_name]
            validation_file = satellite_data_validation[sat_name]
            train_single_network(sat_name, training_file, validation_file, networks_folder,
                                 preprocessors_folder, window_size, epochs, bias_column,
                                 epoch_column, experiment_phase)
        except KeyError as e:
            print(f'Unable to find data for satellite {sat_name}')


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--satellites',
                        help='List of satellites for which networks will be generated',
                        type=str,
                        default='G01,G05,G07,G08,G12,G16,G19,G20,G23,G24,G26,G28,G30,G02,G03,G06,G09,G10,G13,G15,G25,G27,G29,G31,G11,G14,G17,G21,G22,G32')
    parser.add_argument('-t', '--training_directory',
                        help='File that will be used to train network, omit this parameter tu use pretrained models',
                        type=str,
                        default='local/training')
    parser.add_argument('-v', '--validation_directory',
                        help='File that initializes prediction, in none given there will be no prediction',
                        type=str,
                        default='local/validation')
    parser.add_argument('-n', '--networks_folder',
                        help='File that contains topology, weights and training history of neural network',
                        type=str,
                        default='local/networks')
    parser.add_argument('-r', '--preprocessors_folder',
                        help='File that contains preprocessors configuration',
                        type=str,
                        default='local/preprocessors')
    parser.add_argument('-w', '--window_size',
                        help='Sliding window size',
                        type=int,
                        default=32)
    parser.add_argument('-p', '--epochs',
                        help='Number of epochs for which network will be trained',
                        type=int,
                        default=10)
    parser.add_argument('-b', '--bias_column',
                        help='name of clock bias column in csv',
                        type=str,
                        default='Clock_bias')
    parser.add_argument('-e', '--epoch_column',
                        help='name of epoch column in csv output',
                        type=str,
                        default='Epoch')
    parser.add_argument('-x', '--experiment_phase',
                        help='Number of epochs for which network will be trained',
                        type=int,
                        default=10)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    main(args.satellites, args.training_directory, args.validation_directory, args.window_size,
         args.epochs, args.networks_folder, args.preprocessors_folder, args.bias_column,
         args.epoch_column, args.experiment_phase)
