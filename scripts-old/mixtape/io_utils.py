import os
import pandas as pd
from time_utils import epoch_str_to_timestamp, timestamp_to_epoch_str


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

    
def get_files_from_folder(folder, extension):
    files = {}
    extension = f'.{extension}'
    for r, d, f in os.walk(folder):
        for file in f:
            if extension in file:
                file_name = file.split('.')[0]
                files[file_name] = os.path.join(r, file)
    return files


def build_output_file_path(output_dir, sat_name, model_name, ext):
    file_name = '{}_{}.{}'.format(sat_name, model_name, ext)
    return os.path.join(output_dir, file_name)
