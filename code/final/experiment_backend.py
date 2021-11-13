'''
This module contains classes and functions that are required for running embedded neuroevolution
experiments but are not part of actual neuroevolution model.
Mainly those are interfaces between separate elements of project.
'''

import gym

class Overseer:
    '''
    This is experiment main class, it role is to prepare all environments and oversee 
    execution of neuroevolutuion. What is important is that this class is agnostic toward 
    implementation of neural network.
    '''

    def __init__(self, environment, signal_preprocessing_unit, neural_library):
        '''
        Initializer for Overseer class. It can either recieve a custom Gym environment or 
        name of one of default ones. In second case it will attempt to load given environment
        from Gym.

            :param environment: Name of default Gym environment or a object that is custom one.
            :param signal_preprocessing_unit: Object that relay signals between Gym environment 
            and neural network
            :param neural_library: Module responsible for handling networks and neuroevolution
            :return: Returns nothing
        '''
        if not (isinstance(environment, str) or isinstance(environment, gym.Env)):
                raise TypeError(f'Overseer expects environment as either string or gym.Env object, instead recieved {type(environment)}')
        self.environment = environment
