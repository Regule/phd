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

    def get_response(self, x):
        #print(f'{np.dot(self.weights, x)}')
        return 1 if np.dot(self.weights, x) - self.bias > 0 else 0

    def mutate_weight(self):
        weight = choice(list(range(self.weights.shape[0]))) 
        diff = np.random.rand()
        self.weights[weight] += diff

    def mutate_bias(self):
        self.bias += np.random.rand()

    @staticmethod
    def generate_random(input_size):
        return Perceptron(np.random.rand(input_size), np.random.rand())


def simulation_episode(environment, specimen, render=False, render_delay=0.1):
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
    population = sorted(population, key=lambda perceptron: perceptron.score)
    new_population = [population[0]]
    for _ in range(target_size):
        new_specimen = deepcopy(choice(population))
        new_specimen.mutate_weight()
        new_population.append(new_specimen)
    return new_population

POPULATION_SIZE = 50
EPOCHS = 50

def main(args):
    environment = gym.make('CartPole-v0')
    population = []
    for _ in range(POPULATION_SIZE):
        population.append(Perceptron.generate_random(environment.observation_space.shape[0]))
    for _ in range(EPOCHS):
        population = selection(environment, population)
        population = reproduction(population, POPULATION_SIZE)

def parse_arguments():
    parser = argparse.ArgumentParser(description=('This script uses genetic algorithm to' 
    'evolve a perceptron that will balance cart pole.'))
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_arguments())
