import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures

def epoch_str_to_timestamp(epoch_str):
    return datetime.strptime(epoch_str,'%Y-%m-%d %H:%M:%S').timestamp()

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

def old_main(csv_file, bias_column, epoch_column):
    clock_data = pd.read_csv(csv_file, sep=';')
    clock_data[epoch_column] = clock_data[epoch_column].map(epoch_str_to_timestamp)
    
    x = clock_data.iloc[:][epoch_column].values
    y = clock_data.iloc[:][bias_column].values
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=1/5, random_state=0)
    
    linear_regressor = LinearRegression()
    linear_regressor.fit(np.array(x_train.reshape(-1, 1)), y_train.reshape(-1, 1))
    y_predict = linear_regressor.predict(x_test.reshape(-1, 1))

    plt.scatter(x_train, y_train, color='teal', edgecolors='black', label='Training-set observation points')
    plt.plot(x_train.reshape(-1, 1), linear_regressor.predict(x_train.reshape(-1, 1)), color='grey', label='Fit Regression Line')
    plt.title('Differentiated clock bias')
    plt.xlabel('Time (with UNIX)')
    plt.ylabel('Bias in nanoseconds')

    # plot scatter points and line for test data
    plt.scatter(x_test, y_test, color='red', edgecolors='black', label='Test-set observation points')
    plt.legend()
    plt.show()

def main(csv_file, bias_column, epoch_column):
    clock_data = pd.read_csv(csv_file, sep=';')
    clock_data[epoch_column] = clock_data[epoch_column].map(epoch_str_to_timestamp)
    
    x = clock_data.iloc[:][epoch_column].values
    y = clock_data.iloc[:][bias_column].values
    diff = Differentiator()
    y = diff.fit_transform(y)
    x = x[1:]

    x = x.reshape(-1,1)
    poly_reg = PolynomialFeatures(degree = 2)
    x_poly = poly_reg.fit_transform(x)
    # linear regression model
    linear_reg_model = LinearRegression()
    linear_reg_model.fit(x, y)

    # polynomial regression model
    poly_reg_model = LinearRegression()
    poly_reg_model.fit(x_poly, y)

    plt.scatter(x, y, color='red', label='Actual observation points')
    plt.plot(x, linear_reg_model.predict(x), label='Linear regressor fit curve')
    plt.plot(x, poly_reg_model.predict(poly_reg.fit_transform(x)), label='Polynmial regressor fit line')
    plt.title('Truth or bluff (Linear Regression)')
    plt.xlabel('Position Level')
    plt.ylabel('Salary')

    plt.legend()
    plt.show()

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--csv_file',
                        help='csv file',
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
    main(args.csv_file, args.bias_column, args.epoch_column)
