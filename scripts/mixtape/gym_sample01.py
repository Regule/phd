'''
This is a first attempt at creating Ai Gym based script.
'''
import argparse
from random import choice
from time import sleep
import gym


def main():
    '''
    Script main function, it runs single episode of Cart Pole simulation
    '''
    environment = gym.make('CartPole-v0')
    observation = environment.reset()
    environment.render()
    # img = environment.render(mode='rgb_array')
    print(environment.action_space)
    finished = False
    total_reward = 0
    while not finished:
        action = choice([0,1])
        observation, reward, finished, _ = environment.step(action) # last one is extra info
        total_reward += reward
        print(f'{observation} {action} -> {reward}')
        environment.render()
        sleep(0.2)
    print(f'finished, total reward is {total_reward}')


def parse_arguments():
    '''
    Parsing arguments, this time no arguments are used so it is only for a help
    functionality.
    '''
    parser = argparse.ArgumentParser(description='A simple attempt at AiGym')
    parser.parse_args()

if __name__ == '__main__':
    parse_arguments()
    main()
