'''
In this example a simple implementation of perceptron alongside with evolutionary
algorithm is used to solve simpliest Ai Gym problem.
This is just one of a first exercises before tackling a real issues.
'''
import argparse
from time import sleep
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
        weight = int((np.random.rand()+1)*self.weights.shape[0])
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
        action = perceptron.get_response(observation)
        observation, reward, finished, _ = environment.step(action)
        total_reward += reward
        if render:
            print(f'{observation} {action} -> {reward}')
            environment.render()
            sleep(render_delay)
    perceptron.score = total_reward
    return perceptron


def main(args):
    environment = gym.make('CartPole-v0')
    observation = environment.reset()
    environment.render()
    finished = False
    total_reward = 0
    perceptron = Perceptron.generate_random(environment.observation_space.shape[0])
    print(f'Weights = {perceptron.weights}, bias = {perceptron.bias}')
    while not finished:
        action = perceptron.get_response(observation)
        observation, reward, finished, _ = environment.step(action) # last one is extra info
        total_reward += reward
        print(f'{observation} {action} -> {reward}')
        environment.render()
        sleep(0.2)
    print(f'finished, total reward is {total_reward}')

def parse_arguments():
    parser = argparse.ArgumentParser(description=('This script uses genetic algorithm to' 
    'evolve a perceptron that will balance cart pole.'))
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_arguments())
