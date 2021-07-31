import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import json
import argparse
from datetime import datetime
from keras import regularizers

EPOCH_STR_FORMAT = '%Y-%m-%d %H:%M:%S'

def epoch_str_to_timestamp(epoch_str):
    return datetime.strptime(epoch_str, EPOCH_STR_FORMAT).timestamp()

def read_data_from_csv(csv, epoch_column, bias_column):
    clock_data = pd.read_csv(csv, sep=';')
    clock_data[epoch_column] = clock_data[epoch_column].map(epoch_str_to_timestamp)
    x = clock_data.iloc[:][epoch_column].values
    y = clock_data.iloc[:][bias_column].values
    return x, y


def save_to_csv(x, y, csv, epoch_column, bias_column):
    x = list(map(timestamp_to_epoch_str, x))
    data = {epoch_column:x, bias_column:y}
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(csv, sep=';', index=False)

# NOT A PROPER SCIKIT-LEARN TRANSFORMER !!!
class Differentiator:

    def __init__(self, start_point=0.0, end_point=0.0):
        self.start_point = start_point
        self.end_point = end_point


    def fit(self, time_series):
        self.end_point = time_series[-1]
        self.start_point = time_series[0]

    def transform(self, time_series):
        return np.diff(time_series)

    def fit_transform(self, time_series):
        self.fit(time_series)
        return self.transform(time_series)

    def reverse_transform(self, time_series, append_mode=False):
        time_series = np.insert(time_series, 0,
                                self.end_point if append_mode else self.start_point,
                                axis=0)
        return np.cumsum(time_series)


# NOT A PROPER SCIKIT-LEARN TRANSFORMER !!!
class MeanShifter:

    def __init__(self, mean=0.0):
        self.mean = mean

    def fit(self, time_series):
        self.mean = np.mean(time_series)

    def transform(self, time_series):
        return time_series - self.mean

    def fit_transform(self, time_series):
        self.fit(time_series)
        return self.transform(time_series)

    def reverse_transform(self, time_series):
        return time_series + self.mean


# NOT A PROPER SCIKIT-LEARN TRANSFORMER !!!
class CustomScaler:

    def __init__(self, scale=1.0):
        self.scale = scale

    def fit(self, time_series):
        self.scale = self.scale = 1.0/max(np.max(time_series), 0.0-np.min(time_series))

    def transform(self, time_series):
        return time_series * self.scale

    def fit_transform(self, time_series):
        self.fit(time_series)
        return self.transform(time_series)

    def reverse_transform(self, time_series):
        return time_series / self.scale
    

# NOT A PROPER SCIKIT-LEARN TRANSFORMER !!!
class TimeReferenceShifter:

    def __init__(self, t_zero=0, delta_t=1):
        self.t_zero = t_zero
        self.delta_t = delta_t

    def fit(self, time_series):
        self.t_zero = time_series[0]
        self.delta_t = time_series[1]-time_series[0]

    def transform(self, time_series):
        return np.arange(time_series.shape[0])

    def fit_transform(self, time_series):
        self.fit(time_series)
        return self.transform(time_series)

    def reverse_transform(self, time_series):
        return time_series*self.delta_t+self.t_zero


# NOT A PROPER SCIKIT-LEARN TRANSFORMER !!!
# DIFFERENTIATOR MUST BE FITTED FOR NEW DATA
class DataPreprocessor:

    def __init__(self, t_zero=0, delta_t=1, mean=0.0, scale=1.0):
        self.timeframe_shifter = TimeReferenceShifter(t_zero, delta_t)
        self.mean_shifter = MeanShifter(mean)
        self.scaler = CustomScaler(scale)
        self.differentiator = Differentiator()


    def fit(self, x, y):
        self.timeframe_shifter.fit(x)
        y = self.differentiator.fit_transform(y)
        y = self.mean_shifter.fit_transform(y)
        self.scaler.fit(y)

    def fit_differentiator(self, y):
        self.differentiator.fit(y)

    def transform_timeframe(self, timeframe):
        timeframe = self.timeframe_shifter.transform(timeframe)
        return timeframe.reshape(-1,1)
        
    def transform(self, x, y):
        x = self.timeframe_shifter.transform(x)
        y = self.differentiator.transform(y)
        x = x[1:]
        y = self.mean_shifter.transform(y)
        y = self.scaler.transform(y)
        x = x.reshape(-1,1)
        y = y.reshape(-1,1)
        return x, y

    def reverse_transform(self, x, y):
        x = x.flatten()
        y = y.flatten()
        y = self.scaler.reverse_transform(y)
        y = self.mean_shifter.reverse_transform(y)
        x = np.insert(x, 0, 0, axis=0)
        y = self.differentiator.reverse_transform(y)
        x = self.timeframe_shifter.reverse_transform(x)
        return x, y

    def fit_transform(self, x, y):
        self.fit(x, y)
        return self.transform(x, y)

    def to_json(self, filename):
        params = {'t_zero':self.timeframe_shifter.t_zero,
                  'delta_t':self.timeframe_shifter.delta_t,
                  'mean':self.mean_shifter.mean,
                  'scale':self.scaler.scale}
        with open(filename, 'w') as json_file:
            json.dump(params, json_file)

    @staticmethod
    def load_json(filename):
        config = None
        with open(filename, 'r') as json_file:
            config = json.load(json_file)
        return DataPreprocessor(**config)    

    def __str__(self):
        params = {'t_zero':self.timeframe_shifter.t_zero,
                  'delta_t':self.timeframe_shifter.delta_t,
                  'mean':self.mean_shifter.mean,
                  'scale':self.scaler.scale,
                  'start_point': self.differentiator.start_point,
                  'end_point': self.differentiator.end_point}
        return str(params)


#==============================================================================================================
#==============================================================================================================
#==============================================================================================================

def build_windowed_data(time_series, window_size):
    windows = []
    outputs = []
    step = 0
    while step + window_size < time_series.shape[0]:
        windows.append(time_series[step:step+window_size])
        outputs.append(time_series[step+window_size])
        step += 1
    return np.asarray(windows), np.asarray(outputs)


def build_lstm(input_shape, hidden_factor, input_dropout, input_recurrent_dropout,
               hidden_dropout, hidden_recurrent_dropout, input_regularization,
               hidden_regularization, optimizer):
    input_size = input_shape[1]
    input_shape = (input_shape[1], input_shape[2])
    HIDDEN_FACTOR_FROM_PHASE_3 = 2
    hidden_size = int(input_size*HIDDEN_FACTOR_FROM_PHASE_3)
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


def build_network_models(input_shape, variants):
    models = {}
    models['1_low_rmsprop'] = build_lstm(input_shape, 1, 0.1, 0.01, 0.1, 0.01, 0.001, 0.001, 'rmsprop')
    models['1_high_rmsprop'] = build_lstm(input_shape, 1, 0.5, 0.1, 0.5, 0.1, 0.001, 0.001, 'rmsprop')
    models['1_no_rmsprop'] = build_lstm(input_shape, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'rmsprop')
    models['2_low_rmsprop'] = build_lstm(input_shape, 2, 0.1, 0.01, 0.1, 0.01, 0.001, 0.001, 'rmsprop')
    models['2_high_rmsprop'] = build_lstm(input_shape, 2, 0.5, 0.1, 0.5, 0.1, 0.001, 0.001, 'rmsprop')
    models['2_no_rmsprop'] = build_lstm(input_shape, 2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'rmsprop')
    models['4_low_rmsprop'] = build_lstm(input_shape, 4, 0.1, 0.01, 0.1, 0.01, 0.001, 0.001, 'rmsprop')
    models['4_high_rmsprop'] = build_lstm(input_shape, 4, 0.5, 0.1, 0.5, 0.1, 0.001, 0.001, 'rmsprop')
    models['4_no_rmsprop'] = build_lstm(input_shape, 4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'rmsprop')
    models['8_low_rmsprop'] = build_lstm(input_shape, 8, 0.1, 0.01, 0.1, 0.01, 0.001, 0.001, 'rmsprop')
    models['8_high_rmsprop'] = build_lstm(input_shape, 8, 0.5, 0.1, 0.5, 0.1, 0.001, 0.001, 'rmsprop')
    models['8_no_rmsprop'] = build_lstm(input_shape, 8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'rmsprop')
    return models

#===========================================================================
def main(training_file, initializer_file, prediction_depth, window_size, weights_file,
         topology_file, output_file, bias_column, epoch_column, validation_file):
    preprocessor = DataPreprocessor()
    
    x, y = read_data_from_csv(training_file, epoch_column, bias_column)
    x, y = preprocessor.fit_transform(x, y)
    
    x_tr, y_tr = build_windowed_data(y, window_size)
    
    x, y = read_data_from_csv(validation_file, epoch_column, bias_column)
    x, y = preprocessor.transform(x, y)
    x_val, y_val = build_windowed_data(y, window_size)

    network = build_network_models(x_tr.shape,None)['2_no_rmsprop']
    history = network.fit(x_tr, y_tr, epochs=5, batch_size=32,
                          validation_data=(x_val, y_val), shuffle=False)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--training_file',
                        help='File that will be used to train network, omit this parameter tu use pretrained models',
                        type=str,
                        default=None)
    parser.add_argument('-i', '--initializer_file',
                        help='File that initializes prediction, in none given there will be no prediction',
                        type=str,
                        default=None)
    parser.add_argument('-v', '--validation_file',
                        help='File that initializes prediction, in none given there will be no prediction',
                        type=str,
                        default=None)
    parser.add_argument('-d', '--prediction_depth',
                        help='How many steps should be predicted',
                        type=int,
                        default=15)
    parser.add_argument('-s', '--window_size',
                        help='Sliding window size',
                        type=int,
                        default=32)
    parser.add_argument('-w', '--weights_file',
                        help='File that contains weights of neural network',
                        type=str,
                        required=True)
    parser.add_argument('-p', '--topology_file',
                        help='File that contains topology of neural network',
                        type=str,
                        required=True)
    parser.add_argument('-o', '--output_file',
                        help='File containing prediction output, if none given no prediction',
                        type=str,
                        default=None)
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
    main(args.training_file, args.initializer_file, args.prediction_depth, args.window_size, args.weights_file,
         args.topology_file, args.output_file, args.bias_column, args.epoch_column, args.validation_file)
