import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

EPOCH_STR_FORMAT = '%Y-%m-%d %H:%M:%S'

def epoch_str_to_timestamp(epoch_str):
    if epoch_str is None: return None
    return datetime.strptime(epoch_str, EPOCH_STR_FORMAT).timestamp()

def first_plot(csv_file, epoch_column, bias_column, first_timestamp, last_timestamp):
    first_timestamp = epoch_str_to_timestamp(first_timestamp)
    last_timestamp = epoch_str_to_timestamp(last_timestamp)
    clock_data = pd.read_csv(csv_file, sep=';')
    y = clock_data[bias_column]
    x = np.asarray(list(range(y.shape[0])))
    plt.title('Raw clock bias')
    plt.yscale('symlog')
    plt.plot(x,y)
    plt.xlabel('Measurement number')
    plt.ylabel('Clock bias [nanoseconds]')
    plt.show()

def second_plot(csv_file, epoch_column, bias_column, first_timestamp, last_timestamp):
    first_timestamp = epoch_str_to_timestamp(first_timestamp)
    last_timestamp = epoch_str_to_timestamp(last_timestamp)
    clock_data = pd.read_csv(csv_file, sep=';')
    y = clock_data[bias_column].diff()    
    x = np.asarray(list(range(1, y.shape[0]+1)))
    plt.title('Differentiated clock bias')
    plt.plot(x,y)
    plt.xlabel('Measurement number')
    plt.ylabel('Clock bias [nanoseconds]')
    plt.show()

def third_plot(csv_file, epoch_column, bias_column, first_timestamp, last_timestamp):
    first_timestamp = epoch_str_to_timestamp(first_timestamp)
    last_timestamp = epoch_str_to_timestamp(last_timestamp)
    clock_data = pd.read_csv(csv_file, sep=';')
    y = clock_data[bias_column].diff()    
    y = y - y.mean()
    factor = abs(max(y.min(), y.max(), key=abs))
    y = y / factor
    x = np.asarray(list(range(1, y.shape[0]+1)))
    plt.title('Normalized clock bias')
    plt.plot(x,y)
    plt.xlabel('Measurement number')
    plt.ylabel('Normalized bias')
    plt.show()

if __name__ == '__main__':
    first_plot('local/G01.csv', 'Epoch','Clock_bias','2018-07-22 00:00:00','2018-07-22 23:59:59')
    second_plot('local/G01.csv', 'Epoch','Clock_bias','2018-07-22 00:00:00','2018-07-22 23:59:59')
    third_plot('local/G01.csv', 'Epoch','Clock_bias','2018-07-22 00:00:00','2018-07-22 23:59:59')
