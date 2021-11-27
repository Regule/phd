'''
This script can be used for training a neural network with NEAT algorithm for any
CSV file that contains numeric data.
'''

import argparse
import sys

import neat
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import graphviz


observations = None
responses = None

def panic(msg: str):
    print(msg)
    sys.exit()

def read_data_from_csv(csv_file_name: str, observation_columns,
        response_columns, csv_separator_character, sample_count):
    try:
        dataset = pd.read_csv(csv_file_name, sep=csv_separator_character)
        if sample_count is not None:
            dataset = dataset.sample(n=sample_count)
        observations = dataset[observation_columns].to_numpy(dtype=float)
        responses = dataset[response_columns].to_numpy(dtype=float)
        return observations, responses
    except FileNotFoundError:
        panic(f'File {csv_file_name} do not exist.')
    except KeyError as err:
        panic(err)
    except ValueError as err:
        panic(f'One of selected columns contains non numerical data {err.args[0].split()[-1]}')

def plot_stats(statistics, ylog=False, view=False, filename='avg_fitness.svg'):
    """ Plots the population's average and best fitness. """
    if plt is None:
        warnings.warn("This display is not available due to a missing optional dependency (matplotlib)")
        return

    generation = range(len(statistics.most_fit_genomes))
    best_fitness = [c.fitness for c in statistics.most_fit_genomes]
    avg_fitness = np.array(statistics.get_fitness_mean())
    stdev_fitness = np.array(statistics.get_fitness_stdev())

    plt.plot(generation, avg_fitness, 'b-', label="average")
    plt.plot(generation, avg_fitness - stdev_fitness, 'g-.', label="-1 sd")
    plt.plot(generation, avg_fitness + stdev_fitness, 'g-.', label="+1 sd")
    plt.plot(generation, best_fitness, 'r-', label="best")

    plt.title("Population's average and best fitness")
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.grid()
    plt.legend(loc="best")
    if ylog:
        plt.gca().set_yscale('symlog')

    plt.savefig(filename)
    if view:
        plt.show()

    plt.close()


def plot_spikes(spikes, view=False, filename=None, title=None):
    """ Plots the trains for a single spiking neuron. """
    t_values = [t for t, I, v, u, f in spikes]
    v_values = [v for t, I, v, u, f in spikes]
    u_values = [u for t, I, v, u, f in spikes]
    I_values = [I for t, I, v, u, f in spikes]
    f_values = [f for t, I, v, u, f in spikes]

    fig = plt.figure()
    plt.subplot(4, 1, 1)
    plt.ylabel("Potential (mv)")
    plt.xlabel("Time (in ms)")
    plt.grid()
    plt.plot(t_values, v_values, "g-")

    if title is None:
        plt.title("Izhikevich's spiking neuron model")
    else:
        plt.title("Izhikevich's spiking neuron model ({0!s})".format(title))

    plt.subplot(4, 1, 2)
    plt.ylabel("Fired")
    plt.xlabel("Time (in ms)")
    plt.grid()
    plt.plot(t_values, f_values, "r-")

    plt.subplot(4, 1, 3)
    plt.ylabel("Recovery (u)")
    plt.xlabel("Time (in ms)")
    plt.grid()
    plt.plot(t_values, u_values, "r-")

    plt.subplot(4, 1, 4)
    plt.ylabel("Current (I)")
    plt.xlabel("Time (in ms)")
    plt.grid()
    plt.plot(t_values, I_values, "r-o")

    if filename is not None:
        plt.savefig(filename)

    if view:
        plt.show()
        plt.close()
        fig = None

    return fig


def plot_species(statistics, view=False, filename='speciation.svg'):
    """ Visualizes speciation throughout evolution. """
    if plt is None:
        warnings.warn("This display is not available due to a missing optional dependency (matplotlib)")
        return

    species_sizes = statistics.get_species_sizes()
    num_generations = len(species_sizes)
    curves = np.array(species_sizes).T

    fig, ax = plt.subplots()
    ax.stackplot(range(num_generations), *curves)

    plt.title("Speciation")
    plt.ylabel("Size per Species")
    plt.xlabel("Generations")

    plt.savefig(filename)

    if view:
        plt.show()

    plt.close()


def draw_net(config, genome, view=False, filename=None, node_names=None, show_disabled=True, prune_unused=False,
             node_colors=None, fmt='svg'):
    """ Receives a genome and draws a neural network with arbitrary topology. """
    # Attributes for network nodes.
    if graphviz is None:
        warnings.warn("This display is not available due to a missing optional dependency (graphviz)")
        return

    if node_names is None:
        node_names = {}

    assert type(node_names) is dict

    if node_colors is None:
        node_colors = {}

    assert type(node_colors) is dict

    node_attrs = {
        'shape': 'circle',
        'fontsize': '9',
        'height': '0.2',
        'width': '0.2'}

    dot = graphviz.Digraph(format=fmt, node_attr=node_attrs)

    inputs = set()
    for k in config.genome_config.input_keys:
        inputs.add(k)
        name = node_names.get(k, str(k))
        input_attrs = {'style': 'filled', 'shape': 'box', 'fillcolor': node_colors.get(k, 'lightgray')}
        dot.node(name, _attributes=input_attrs)

    outputs = set()
    for k in config.genome_config.output_keys:
        outputs.add(k)
        name = node_names.get(k, str(k))
        node_attrs = {'style': 'filled', 'fillcolor': node_colors.get(k, 'lightblue')}

        dot.node(name, _attributes=node_attrs)

    if prune_unused:
        connections = set()
        for cg in genome.connections.values():
            if cg.enabled or show_disabled:
                connections.add((cg.in_node_id, cg.out_node_id))

        used_nodes = copy.copy(outputs)
        pending = copy.copy(outputs)
        while pending:
            new_pending = set()
            for a, b in connections:
                if b in pending and a not in used_nodes:
                    new_pending.add(a)
                    used_nodes.add(a)
            pending = new_pending
    else:
        used_nodes = set(genome.nodes.keys())

    for n in used_nodes:
        if n in inputs or n in outputs:
            continue

        attrs = {'style': 'filled',
                 'fillcolor': node_colors.get(n, 'white')}
        dot.node(str(n), _attributes=attrs)

    for cg in genome.connections.values():
        if cg.enabled or show_disabled:
            #if cg.input not in used_nodes or cg.output not in used_nodes:
            #    continue
            input, output = cg.key
            a = node_names.get(input, str(input))
            b = node_names.get(output, str(output))
            style = 'solid' if cg.enabled else 'dotted'
            color = 'green' if cg.weight > 0 else 'red'
            width = str(0.1 + abs(cg.weight / 5.0))
            dot.edge(a, b, _attributes={'style': style, 'color': color, 'penwidth': width})

    dot.render(filename, view=view)

    return dot

def build_neat_algorithm(network_configuration_file):
    try:
        network_configuration = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                neat.DefaultSpeciesSet, neat.DefaultStagnation, network_configuration_file)

        population = neat.Population(network_configuration)

        population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)
        #population.add_reporter(neat.Checkpointer(5))
        return network_configuration, population, stats
    except Exception as err:
        panic(f'An error occured when build NEAT environment: {err}')


def evaluate_network(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 0 
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        for observation, expected_response in zip(observations, responses):
            response = net.activate(observation)
            genome.fitness -= np.sum((response-expected_response) ** 2)


def run_network(population, evaluation_function, generations):
    try:
        winner = population.run(evaluation_function, generations)
        return winner
    except RuntimeError as err:
        panic(f'A following error occured when running NEAT: {err}')


def visualise_network(genome, configuration, stats):
    winner_net = neat.nn.FeedForwardNetwork.create(genome, configuration)
    draw_net(configuration, genome, view=False)
    plot_stats(stats, ylog=False, view=False)
    plot_species(stats, view=False)


def main(args: argparse.Namespace):
    global observations, responses
    observations, responses  = read_data_from_csv(args.data_file, args.observation_columns, 
            args.response_columns, args.csv_separator_character, args.sample_size)
    network_configuration, population, stats = build_neat_algorithm(
            args.network_configuration_file)
    winner = run_network(population, evaluate_network, args.generations)
    visualise_network(winner, network_configuration, stats)


def build_column_list(list_str):
    return list_str.split(',')

def parse_arguments()-> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-d', '--data_file', type=str, required=True,
            help='CSV file in which observation-reaction pairs are stored')
    parser.add_argument('-o', '--observation_columns', type=build_column_list, required=True,
            help='List of columns containing observation data (network input) separated by colon.')
    parser.add_argument('-r', '--response_columns', type=build_column_list, required=True,
            help='List of columns containing response data (network output) separated by colon.')
    parser.add_argument('-c', '--network_configuration_file', type=str, required=True,
            help='File containing configuration for NEAT algorithm')
    parser.add_argument('-g', '--generations', type=int, default=100,
            help='Number of generations for which genetic algorithm will be run')
    parser.add_argument('--csv_separator_character', type=str, default=';',
            help='Character used in CSV file for separating columns')
    parser.add_argument('-s', '--sample_size', type=int, default=None,
            help='Number of samples to take from dataset, if not set whole dataset will be used')
    return parser.parse_args()



if __name__ == '__main__':
    main(parse_arguments())
