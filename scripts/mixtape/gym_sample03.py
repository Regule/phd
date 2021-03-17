'''
This is a script that implements simple example of neuroevolution for solving inverse 
pendulim balancing problem.
'''
import argparse
from random import choice
from copy import deepcopy
from time import sleep
import numpy as np
import gym


class NeuralLayer:
    '''
    This is a class that represents a single, multi neuron, layer in a neural network.
    '''

    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias

    def get_response(self, x):
        u = np.matmul(self.weights, x)
        u_prim = u + self.bias
        y = 1/(1 + np.exp(-u_prim))
        return y

    def mutate(self, factor):
        weights_mutation = (np.random.rand(*(self.weights.shape))*2-1)*factor
        bias_mutation = (np.random.rand(*(self.bias.shape))*2-1)*factor
        self.weights += weights_mutation
        self.bias += bias_mutation

    @staticmethod
    def generate_random_layer(input_size, layer_size):
        weights = np.random.rand(layer_size, input_size)*2-1
        bias = np.random.rand(layer_size)*(-1)
        return NeuralLayer(weights, bias)


class Specimen:

    def __init__(self, layers):
        self.layers = layers
        self.score = 0

    def get_response(self, x):
        h = x
        for layer in self.layers:
            h = layer.get_response(h)
        return np.argmax(h)

    def mutate(self, factor):
        for layer in self.layers:
            layer.mutate(factor)

    def __lt__(self, other):
        return self.score < other.score

    @staticmethod
    def generate_random_specimen(input_size, layer_sizes):
        layers = []
        for layer_size in layer_sizes:
            layers.append(NeuralLayer.generate_random_layer(input_size, layer_size))
            input_size = layer_size
        return Specimen(layers) 


def test_gym(simulation_delay):
    '''
    This function runs a single simulation in OpenAI gym to see if everything
    is fine on that end.

    Parameters
    ----------
        simulation_delay: float
            Time between frames in simulation

    Returns
    -------
        None
    '''
    environment = gym.make('CartPole-v1')
    observation = environment.reset()
    total_reward = 0

    print(f'Observation space for environment is {environment.observation_space}')
    print(f'Action space for environment is {environment.action_space}')

    finshed = False
    environment.render()
    while not finshed:
        action = choice([0,1])
        observation, reward, finshed, _ = environment.step(action)
        total_reward += reward
        print(f'{observation} -> {action}')
        sleep(simulation_delay)
        environment.render()
    print(f'Total reward is {total_reward}')

def test_specimen():
    layer = NeuralLayer.generate_random_layer(3,5)
    print(layer.weights)
    print(layer.bias)
    test_input = np.array([0.3, 0.5, 1.0])
    print(f'Response is {layer.get_response(test_input)}')
    layer.mutate(0.5)
    specimen = Specimen.generate_random_specimen(3, [5,6,3,2])
    print(f'Response of multi layer network is {specimen.get_response(test_input)}')
    specimen.mutate(0.3)

def run_simulation(specimen, environment, assign_score=True, show=False, delay=0.2):
    observation = environment.reset()
    total_reward = 0
    finished = False
    if show:
        environment.render()
    
    while not finished:
        action = specimen.get_response(observation)
        observation, reward, finished , _ = environment.step(action)
        total_reward += reward
        if show:
            environment.render()
            sleep(delay)

    if assign_score:
        specimen.score = total_reward

def assign_scores(population, environment, show_best=True):
    for specimen in population:
        run_simulation(specimen,environment)
    population.sort()
    if show_best:
        print(f'Best score is {population[-1].score}')
        run_simulation(population[-1], environment, show=True, delay=0.1)


def selection(population, factor, elite=1):
    breeders = []
    population.sort()
    desired_breeders_count = int(len(population)*factor)

    for _ in range(elite):
        breeders.append(population.pop(-1))
    
    while len(breeders) < desired_breeders_count:
        specimen_a = choice(population)
        specimen_b = choice(population)
        if specimen_a < specimen_b:
            breeders.append(specimen_b)
        else:
            breeders.append(specimen_a)
        try:
            population.remove(specimen_a)
            population.remove(specimen_b)
        except ValueError:
            pass # Id speciman_a is same as b second remove will raise exception, this is ok.

    return breeders

def reproduction(breeding_base, population_size, elite=1, mutation_factor=0.5):
    population = []
    breeding_base.sort()

    for i in range(elite):
        population.append(breeding_base[0-(1+i)])

    while len(population) < population_size:
        new_specimen = deepcopy(choice(breeding_base))
        new_specimen.mutate(mutation_factor)
        population.append(new_specimen)

    return population


def create_initial_population(population_size, input_size, output_size, hidden_layers_sizes):
    population = []
    hidden_layers_sizes.append(output_size)
    for _ in range(population_size):
        population.append(Specimen.generate_random_specimen(input_size, hidden_layers_sizes))
    return population
    

def run_neuroevolution(population_size, generations, elite_size, selection_factor,
    mutation_factor, show_best=True):
    environment = gym.make('CartPole-v1')
    observation = environment.reset()
    input_size = observation.shape[0]
    output_size = 2 # FIXME: THIS SHOULD NOT BE A FIXED VALUE 

    population = create_initial_population(population_size, input_size, output_size, [7])
    for generation in range(generations):
        assign_scores(population, environment)
        breeding_base = selection(population, selection_factor, elite_size)
        population = reproduction(breeding_base, population_size, elite_size, mutation_factor)


def main(args):
    if args.test_gym:
        test_gym(args.simulation_step_delay)
    elif args.test_specimen:
        test_specimen()
    else:
        run_neuroevolution(200, 20, 1, 0.5, 0.3)

def parse_arguments():
    '''
    This function parses argumets from command line.

    Returns
    -------
        argparse.Namespace
        This is a namespace with attributes given by command line or their default 
        values.
    '''
    parser = argparse.ArgumentParser(description='A simple example of neuroevolution')
    parser.add_argument('--test_gym',
            action='store_true',
            help='If set then no neuroevolution will be ran, only gym ai env tested.')
    parser.add_argument('--test_specimen',
            action='store_true',
            help='If set then no neuroevolution will be ran, only specimen implementation test.')
    parser.add_argument('--simulation_step_delay',
            type=float,
            default=0.2,
            help='Time is seconds between steps of simulation')
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_arguments())
