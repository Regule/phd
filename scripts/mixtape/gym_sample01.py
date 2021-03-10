'''
This is a first attempt at creating Ai Gym based script.
'''
import argparse
import gym
from random import choice
from time import sleep


def main(args):
    environment = gym.make('CartPole-v0')
    observation = environment.reset()
    environment.render()
    # img = environment.render(mode='rgb_array')
    print(environment.action_space)
    finished = False
    total_reward = 0
    while not finished:
        action = choice([0,1])
        observation, reward, finished, extra_info = environment.step(action)
        total_reward += reward
        print(f'{action} -> {reward}')
        environment.render()
        sleep(0.2)
    print(f'finished, total reward is {total_reward}')


def parse_arguments():
    parser = argparse.ArgumentParser(description='A simple attempt at AiGym')
    return parser.parse_args()

if __name__ == '__main__':
    main(parse_arguments())
