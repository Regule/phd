'''
In this example a simple implementation of perceptron alongside with evolutionary
algorithm is used to solve simpliest Ai Gym problem.
This is just one of a first exercises before tackling a real issues.
'''
import argparse
from time import sleep
from random import choice
from copy import deepcopy
import gym
import numpy as np

class Perceptron:
    '''
    This class represents a simple perceptron like neuron.
    '''

    def __init__(self, weights, bias):
        '''
        A constructor for Perceptron object.

        :param weights: Weights for neuron input this should be a numpy array same size as
        neuron input
        :param bias: A single floating point value that will be substracted from weighted sum
        before activation
        '''
        self.weights = weights
        self.bias = bias
        self.score = 0

    def get_response(self, network_input):
        '''
        An actual neuron signal processing.
        :return Neuron response for given input
        '''
        return 1 if np.dot(self.weights, network_input) - self.bias > 0 else 0

    def mutate_weight(self):
        '''
        This function add a random value from range [-1,1] to a random weight of neuron.
        '''
        weight = choice(list(range(self.weights.shape[0])))
        diff = np.random.rand()
        self.weights[weight] += diff

    def mutate_bias(self):
        '''
        This function adds a random value from range [-1,1] to bias.
        '''
        self.bias += np.random.rand()

    @staticmethod
    def generate_random(input_size):
        '''
        This function generate random perceptron with weight vector of size fitting given
        input size. All weights as well as the bias will be set to a random value from range
        [-1,1].

        :param input_size: A size of input that neuron is expected to process

        :return A perceptron cabable of processing input of given size.
        '''
        return Perceptron(np.random.rand(input_size), np.random.rand())


def simulation_episode(environment, specimen, render=False, render_delay=0.1):
    '''
    This function runs a Ai Gym simulation episode for a single specimen and assign it
    score equal to total reward.

    :param environment: Gym environment that will be used for simulation
    :param specimen: Peceptron that will control agent in simulation, it will be modified by
    setting new score
    :param render: If set to true simualtion will be visualised and details will be printed
    to terminal
    :param render_delay: Time between steps during visualisation, if render is set to false
    it has no effect on execution.
    '''
    observation = environment.reset()
    if render:
        environment.render()
        sleep(render_delay)
    total_reward = 0
    finished = False
    while not finished:
        action = specimen.get_response(observation)
        observation, reward, finished, _ = environment.step(action)
        total_reward += reward
        if render:
            print(f'{observation} {action} -> {reward}')
            environment.render()
            sleep(render_delay)
    specimen.score = total_reward


def selection(environment, population, selection_factor=0.5):
    '''
    This function runs a tournament selection algorithm. In it a two random specimens from
    population are chosen an the one with lower score is removed. If scores are equal or
    firs specimen is removed and if both randoms return same object it will be removed.

    :param environment: Gym environment that will be used for simulation
    :param population: List containing all specimens
    :param selection_factor: How many specimens should survive selection, value should be set
    between 0 and 1

    :return A population with some specimens removed by a selection
    '''
    for specimen in population:
        simulation_episode(environment,specimen)
    target_size = int(len(population)*selection_factor)
    population = sorted(population, key=lambda perceptron: perceptron.score)
    print(f'TOP SCORE = {population[0].score}')
    elite = population[0]
    population.remove(elite)
    while len(population) > target_size:
        contender_a = choice(population)
        contender_b = choice(population)
        if contender_a.score > contender_b.score:
            population.remove(contender_b)
        else:
            population.remove(contender_a)
    population.append(elite)
    return population


def reproduction(population, target_size):
    '''
    This function implements asexual reproduction in which a random specimens from population
    are selected, then copied and mutated.

    :param population: All specimens
    :param target_size: Size of generated population

    :return New population that is a result of reproduction process.
    '''
    population = sorted(population, key=lambda perceptron: perceptron.score)
    new_population = [population[0]]
    for _ in range(target_size):
        new_specimen = deepcopy(choice(population))
        new_specimen.mutate_weight()
        new_population.append(new_specimen)
    return new_population


def main(args):
    '''
    This is main function, it runs a evalutionary algorithm

    :param args: aruments from command line
    '''
    environment = gym.make('CartPole-v0')
    population = []
    for _ in range(args.population_size):
        population.append(Perceptron.generate_random(environment.observation_space.shape[0]))
    for _ in range(args.epochs):
        population = selection(environment, population)
        population = reproduction(population, args.population_size)

def parse_arguments():
    '''
    This is function used for parsing command line arguments.

    :return Python namespace containing namespace with argumants.
    '''
    parser = argparse.ArgumentParser(description=('This script uses genetic algorithm to'
    'evolve a perceptron that will balance cart pole.'))
    parser.add_argument('-p',
            '--population_size',
            type=int,
            default=100,
            help='Number of specimens in a population')
    parser.add_argument('-e',
            '--epochs',
            type=int,
            default=100,
            help='Numbers of generations for which algorithm will be run')
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_arguments())
