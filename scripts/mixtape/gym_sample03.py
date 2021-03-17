'''
This is a script that implements simple example of neuroevolution for solving inverse 
pendulim balancing problem.
'''
import argparse
from random import choice
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


def test_neuroevolution():
    layer = NeuralLayer.generate_random_layer(3,5)
    print(layer.weights)
    print(layer.bias)
    test_input = np.array([0.3, 0.5, 1.0])
    print(f'Response is {layer.get_response(test_input)}')
    layer.mutate(0.5)
    specimen = Specimen.generate_random_specimen(3, [5,6,3,2])
    print(f'Response of multi layer network is {specimen.get_response(test_input)}')
    specimen.mutate(0.3)

def main(args):
    if args.test_gym:
        test_gym(args.simulation_step_delay)
    else:
        test_neuroevolution()

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
    parser.add_argument('--simulation_step_delay',
            type=float,
            default=0.2,
            help='Time is seconds between steps of simulation')
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_arguments())
