import neat
import gym
import argparse
import numpy as np
import sys

def show_agent_behaviour(genome, config):
    environment = gym.make(config.environment)
    observation = environment.reset()
    for _ in range(config.max_cycles):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        environment.render() 
        reaction = net.activate(observation) 
        observation, _, finished, _ = environment.step(reaction)
        if finished:
            break

def print_observation(observation):
    print(f'{observation.size} ', end='')
    for feature in observation:
        print(f'{feature} ',end='')
    print()

def read_reaction():
    reaction_str = input()
    reaction = list(map(float, reaction_str.split(' ')[1:]))
    return np.array(reaction)

def main(args):
    environment = gym.make(args.environment)
    observation = environment.reset()
    finished = False
    for _ in range(args.max_cycles):
        print('Printing observation',file=sys.stderr)
        print_observation(observation)
        print('Rendering environment',file=sys.stderr)
        environment.render()
        print('Reading reaction',file=sys.stderr)
        reaction = read_reaction() 
        print('Running simulation step',file=sys.stderr)
        observation, reward, finished, _ = environment.step(reaction)
        if finished:
            break


def parser_arguments():
    print('Parsing command line parameters',file=sys.stderr)
    parser = argparse.ArgumentParser(description='smth')
    parser.add_argument('-e', '--environment', type=str, required=True,
            help='An AI Gym environment name.')
    parser.add_argument('--max_cycles', type=int, default=500,
            help='Maximum number of cycles for which simulation will be ran')
    return parser.parse_args()


if __name__ == '__main__':
    print('HMM')
    main(parser_arguments())
