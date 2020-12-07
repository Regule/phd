import argparse
import os
import tensorflow as tf
import numpy as np
import pandas as pd
from data_preprocessing import DataPreprocessor, build_windowed_data
from io_utils import read_data_from_csv
from time_utils import build_epochs

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



def main(initializer_file, model_file, weights_file, preprocessor_file, prediction_depth, window_size, output_file,
         bias_column, epoch_column):
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
    #predicted = list(map(predicted, lambda x: x[0][0]))
    dataframe = pd.DataFrame(data={epoch_column: epochs, bias_column: predicted})
    sat_name = initializer_file.split('/')[-1]
    dataframe.to_csv(os.path.join(output_file, sat_name), sep=';', index=False)
    
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--initializer_file',
                        help='File that initializes prediction, in none given there will be no prediction',
                        type=str,
                        default=None)
    parser.add_argument('-m', '--model_file',
                        help='File that initializes prediction, in none given there will be no prediction',
                        type=str,
                        default=None)
    parser.add_argument('-w', '--weights_file',
                        help='File that initializes prediction, in none given there will be no prediction',
                        type=str,
                        default=None)
    parser.add_argument('-p', '--preprocessor_file',
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
    main(args.initializer_file, args.model_file, args.weights_file, args.preprocessor_file,
         args.prediction_depth, args.window_size, args.output_file,args.bias_column,
         args.epoch_column)
