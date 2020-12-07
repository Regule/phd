import os
import argparse
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from time_utils import date_str_to_datetime, build_timestamps
from io_utils import read_data_from_csv, save_to_csv, get_files_from_folder
from data_preprocessing import DataPreprocessor


def run_regression(sat_name, training_file, start_timestamp, end_timestamp,
                   time_delta, degrees, epoch_column, bias_column,
                   output_folder):
    print(f'Running regression for satellite {sat_name}')
    x, y = read_data_from_csv(training_file, epoch_column, bias_column)
    x_for_prediction = build_timestamps(start_timestamp, end_timestamp, time_delta)
    
    preprocessor = DataPreprocessor()
    x, y = preprocessor.fit_transform(x, y)
    x_for_prediction = preprocessor.transform_timeframe(x_for_prediction)

    linear_regressor = LinearRegression()
    linear_regressor.fit(x, y)
    y_predicted = linear_regressor.predict(x_for_prediction)

    x_predicted, y_predicted = preprocessor.reverse_transform(x_for_prediction, y_predicted)
    save_to_csv(x_predicted, y_predicted, os.path.join(output_folder, f'{sat_name}_D01.csv'),
                epoch_column, bias_column)

    degrees = list(map(int,degrees.split(',')))
    for deg in degrees:
        poly_features = PolynomialFeatures(deg)
        x_poly = poly_features.fit_transform(x)
        
        polynomial_regressor = LinearRegression()
        polynomial_regressor.fit(x_poly, y)
        
        x_poly_pred = poly_features.fit_transform(x_for_prediction)
        y_predicted = polynomial_regressor.predict(x_poly_pred)
        x_predicted, y_predicted = preprocessor.reverse_transform(x_for_prediction, y_predicted)
        file_name = '{}_D{:02d}.csv'.format(sat_name, deg)
        save_to_csv(x_predicted, y_predicted, os.path.join(output_folder, file_name),
                    epoch_column, bias_column)


    

def main(training_dir, start, end, delta, degrees, epoch_column,
         bias_column, output_folder):
    sat_files = get_files_from_folder(training_dir, 'csv')
    for sat_name, sat_file in sat_files.items():
        run_regression(sat_name, sat_file, start, end, delta,
                       degrees, epoch_column, bias_column,
                       output_folder)



def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--training_dir',
                        help='directory where training data is stored',
                        type=str,
                        required=True)
    parser.add_argument('-o', '--output_dir',
                        help='directory where predictions will be saved',
                        type=str,
                        required=True)
    parser.add_argument('-s', '--start_timestamp',
                        help='directory where igu predictions are stored',
                        type=date_str_to_datetime,
                        required=True)
    parser.add_argument('-n', '--end_timestamp',
                        help='End date for after which prediction will end',
                        type=date_str_to_datetime,
                        required=True)
    parser.add_argument('-m', '--minute_step',
                        help='Difference in minutes between two steps',
                        type=int,
                        default=15)
    parser.add_argument('-d', '--degrees',
                        help='Degrees at which polynomial regression will be applied',
                        type=str,
                        default='2,3,6,12,23')
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
    main(args.training_dir, args.start_timestamp, args.end_timestamp,
         args.minute_step, args.degrees, args.epoch_column,
         args.bias_column, args.output_dir)
