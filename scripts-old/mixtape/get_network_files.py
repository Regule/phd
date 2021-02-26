import argparse
import os

def get_networks(satellites, networks_folder):
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


def main(satellites, networks_folder):
    satellites = satellites.split(',')
    names, top, wgh = get_networks(satellites, networks_folder)
    for sat in satellites:
        for net in names:
            try:
                print(f'Sat = {sat} Net = {net} top = {top[sat][net]} wgh = {wgh[sat][net]}')
            except KeyError as e:
                print(f'Key error -> {e}')

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--satellites',
                        help='List of satellites for which networks will be generated',
                        type=str,
                        default='G01,G05,G07,G08,G12,G16,G19,G20,G23,G24,G26,G28,G30,G02,G03,G06,G09,G10,G13,G15,G25,G27,G29,G31,G11,G14,G17,G21,G22,G32')
    parser.add_argument('-c', '--csv_directory',
                        help='File that will be used to train network, omit this parameter tu use pretrained models',
                        type=str,
                        default='local/training')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    main(args.satellites, args.csv_directory)
