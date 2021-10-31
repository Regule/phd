'''
This module contains classes required for running AI Gym environments as a part
of neuroevolution process.
It is not concerned with implementation of neural network and only require it to
be delivered in a class that provides "activate" function.

Running this module from command line executes a simple test in which in place of a 
network a dummy class that returns random reaponses is used.
'''
import argparse
import gym

from typing import Callable

class NeuroGymEnvironment:
    '''
    Objects of this class can run individual simulation with AiGym for given 
    description of neural network. When creating such an object a function that
    transforms network representation into a functioning network must be provided.
    '''
    def __init__(self, environment_name: str, network_builder: Callable):
        '''
        Constructor 

        :param environment_name: Name of AiGym environment for example 'BipedalWalkerHardcore-v3'
        :param network_builder: Function that takes a network representation and returns a 
        network object. Such object must provide a activate(observation)-> np.ndarray function. 
        '''
        self.environment = gym.make(environment_name)
        self.network_builder = network_builder



def main(args):
    pass


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_arguments())

