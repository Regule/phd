'''
This module contains classes required for running AI Gym environments as a part
of neuroevolution process.
It is not concerned with implementation of neural network and only require it to
be delivered in a class that provides 'activate' function.

Running this module from command line executes a simple test in which in place of a 
network a dummy class that returns random reaponses is used.
'''
import argparse
import gym


class NeuroGymEnvironment:

    def __init__(self, environment_name, network_builder):
        self.environment = gym.make(environment_name)
        self.network_builder = network_builder



def main(args):
    pass


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_arguments())

