import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

import sys

def epoch_str_to_timestamp(epoch_str):
    return datetime.strptime(epoch_str,'%Y-%m-%d %H:%M:%S').timestamp()

def date_str_to_datetime(date_str):
    return datetime.strptime(date_str,'%Y-%m-%d')

def build_timestamps(start, end, delta):
    timestamps = []
    timestamp = start
    delta = timedelta(minutes=delta)
    while timestamp < end:
        timestamps.append(timestamp)
        timestamp += delta
    timestamps = np.asarray(list(map(lambda x: x.timestamp(), timestamps)))
    return timestamps


# NOT A PROPER SCIKIT-LEARN TRANSFORMER !!!
class Differentiator:

    def __init__(self, start_point=0.0, append_mode=False):
        self.start_point = start_point
        self.append_mode = append_mode

    def fit(self, time_series):
        if self.append_mode:
            self.start_point = time_series[-1]
        else:
            self.start_point = time_series[0]

    def transform(self, time_series):
        return np.diff(time_series)

    def fit_transform(self, time_series):
        self.fit(time_series)
        return self.transform(time_series)


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




def plot_results(x, y, x_pred, y_pred, deg):
    plt.plot(x, y, color='green', label='Observed values')
    plt.plot(x_pred, y_pred, color='red', label='Observed values')
    plt.title(f'Predictions with level {deg} plynomial')
    plt.xlabel('Time (with UNIX)')
    plt.ylabel('Bias in nanoseconds')
    plt.legend()
    plt.show()


def main(training_file, start, end, delta, degrees, epoch_column,
         bias_column):
    clock_data = pd.read_csv(training_file, sep=';')
    clock_data[epoch_column] = clock_data[epoch_column].map(epoch_str_to_timestamp)
    
    x = clock_data.iloc[:][epoch_column].values
    y = clock_data.iloc[:][bias_column].values
    x_for_prediction = build_timestamps(start, end, delta)

    timeframe_shifter = TimeReferenceShifter()
    x = timeframe_shifter.fit_transform(x)
    x_for_prediction = timeframe_shifter.transform(x_for_prediction)
    
    diff = Differentiator()
    y = diff.fit_transform(y)
    x = x[1:]

    mean_shifter = MeanShifter()
    y = mean_shifter.fit_transform(y)

    scaler = CustomScaler()
    y = scaler.fit_transform(y)
    
    x = x.reshape(-1,1)
    x_for_prediction = x_for_prediction.reshape(-1,1)
    y = y.reshape(-1,1)


    linear_regressor = LinearRegression()
    linear_regressor.fit(x, y)
    y_predicted = linear_regressor.predict(x_for_prediction)
    plot_results(x,y,x_for_prediction,y_predicted,1)

    degrees = list(map(int,degrees.split(',')))
    for deg in degrees:
        poly_features = PolynomialFeatures(deg)
        x_poly = poly_features.fit_transform(x)
        
        polynomial_regressor = LinearRegression()
        polynomial_regressor.fit(x_poly, y)
        x_poly_pred = poly_features.fit_transform(x_for_prediction)
        print(x_poly_pred.shape)
        y_predicted = polynomial_regressor.predict(x_poly_pred)
        plot_results(x,y,x_for_prediction,y_predicted,deg)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--training_file',
                        help='directory where training data is stored',
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
    parser.add_argument('-m', '--minutes_step',
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
    main(args.training_file, args.start_timestamp, args.end_timestamp, args.minutes_step, args.degrees,
         args.epoch_column, args.bias_column)
