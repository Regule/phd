'''
This is an example in which we can use multiple environments.
'''
import sys
import argparse
from time import sleep
from random import choice
from copy import deepcopy
import gym
import numpy as np
from gym import envs, spaces

#--------------------------------------------------------------------------------------------------
#                                        NEURAL NETWORK
#--------------------------------------------------------------------------------------------------

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

    def __init__(self, layers, discrete):
        self.layers = layers
        self.score = 0
        self.discrete = discrete

    def get_response(self, x):
        h = x
        for layer in self.layers:
            h = layer.get_response(h)
        if self.discrete:
            return np.argmax(h)
        return h

    def mutate(self, factor):
        for layer in self.layers:
            layer.mutate(factor)

    def __lt__(self, other):
        return self.score < other.score

    @staticmethod
    def generate_random_specimen(input_size, layer_sizes, discrete):
        layers = []
        for layer_size in layer_sizes:
            layers.append(NeuralLayer.generate_random_layer(input_size, layer_size))
            input_size = layer_size
        return Specimen(layers, discrete) 


#--------------------------------------------------------------------------------------------------
#                                          HELPERS 
#--------------------------------------------------------------------------------------------------


def print_all_envs():
    environments = envs.registry.all()
    for env in environments:
        print(env)

def get_input_and_output_size(env):
    if len(env.observation_space.shape) != 1:
        print('Unable to work with multidimensional inputs.')
        sys.exit()
    input_size = env.observation_space.shape[0]
    output_size = 0
    discrete = False
    if type(env.action_space) == spaces.Discrete:
        output_size = env.action_space.n
        discrete = True
    elif type(env.action_space) == spaces.Box:
        output_size = env.action_space.shape[0]
    else:
        print('Unsuported action space')
        sys.exit()
    return input_size, output_size, discrete


def test_env(env_name):
    try:
        env = gym.make(env_name)
        env.reset()
        in_size, out_size, discrete = get_input_and_output_size(env)
        print(f'Input size = {in_size}, Output size = {out_size}')
        print('Output is discrete' if discrete else 'Output is continous')
        for _ in range(1000):
            env.render()
            observation, reward, finished , _ = env.step(env.action_space.sample())
            if finished:
                break
    except Exception as e:
        print(f'Problems with environment {env_name}')
        print(e)

def parse_layer_list(layer_list):
    return list(map(int,layer_list.split(',')))

#--------------------------------------------------------------------------------------------------
#                                    GENETIC ALGORITHM
#--------------------------------------------------------------------------------------------------

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
        run_simulation(population[-1], environment, show=True, delay=0.01)


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


def create_initial_population(population_size, input_size, output_size, hidden_layers_sizes,
        discrete):
    population = []
    hidden_layers_sizes.append(output_size)
    for _ in range(population_size):
        population.append(Specimen.generate_random_specimen(input_size, hidden_layers_sizes,
            discrete))
    return population
    

def run_neuroevolution(environment_name, population_size, generations, 
        elite_size, selection_factor, mutation_factor, hidden_size, show_best=True):
    environment = gym.make(environment_name)
    observation = environment.reset()
    input_size, output_size, discrete = get_input_and_output_size(environment)

    population = create_initial_population(population_size, input_size, output_size, hidden_size,
            discrete)
    for generation in range(generations):
        assign_scores(population, environment)
        breeding_base = selection(population, selection_factor, elite_size)
        population = reproduction(breeding_base, population_size, elite_size, mutation_factor)


#--------------------------------------------------------------------------------------------------
#                                          MAIN FUNCTION 
#--------------------------------------------------------------------------------------------------

def parse_arguments():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('-l', '--list_envs', action='store_true')
    parser.add_argument('--test_env', default=None)
    parser.add_argument('-e', '--env_name', required=True)
    parser.add_argument('-g', '--generations', default=5, type=int)
    parser.add_argument('--hidden', default=[5], type=parse_layer_list)
    parser.add_argument('--mutation_factor', default=0.5, type=float)
    parser.add_argument('--selection_factor', default=0.5, type=float)
    parser.add_argument('--population_size', default=100, type=int)
    parser.add_argument('--elite_size', default=1, type=int)
    parser.add_argument('--simulation_step_delay', type=float, default=0.2)
    return parser.parse_args()

def main(args):
    if args.list_envs:
        print_all_envs()
    elif args.test_env is not None:
        test_env(args.test_env)
    else:
        run_neuroevolution(args.env_name, args.population_size, args.generations, args.elite_size, 
                args.selection_factor, args.mutation_factor, args.hidden)


if __name__ == '__main__':
    main(parse_arguments())
