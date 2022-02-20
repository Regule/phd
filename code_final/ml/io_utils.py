import os
import pandas as pd
from time_utils import epoch_str_to_timestamp, timestamp_to_epoch_str


def read_data_from_csv(csv, epoch_column, bias_column):
    clock_data = pd.read_csv(csv, sep=';')
    if type(clock_data[epoch_column][0]) == str:
        clock_data[epoch_column] = clock_data[epoch_column].map(epoch_str_to_timestamp)
    x = clock_data.iloc[:][epoch_column].values
    y = clock_data.iloc[:][bias_column].values
    return x, y


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
