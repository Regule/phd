'''
This module contains classes and functions that are required for running embedded neuroevolution
experiments but are not part of actual neuroevolution model.
Mainly those are interfaces between separate elements of project.
'''

import gym


def verify_neural_library(neural_library):
    '''
    This class checks if selected neural_library provides required level of compatibility 
    with PyNeat.

        :param neural_library: Module that handles neural network and neuroevolution functionality.
        :return: Tuple that contains (True,None) if module provides compatibility or tuple that contains
        (False, List) if it does not. Returned list contains elements that are not found in module.
    '''
    # TODO: Add actual body to this function if needed.
    return (True, None)



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
        if  isinstance(environment, str):
            self.environment = gym.make(environment)
        elif isinstance(environment, gym.Env)):
            self.environment = environment
        else:
            raise TypeError(f'Overseer expects environment as either string or gym.Env object, instead recieved {type(environment)}.')
        
        if not isinstance(signal_preprocessing_unit, SignalPerprocessingUnit):
            raise TypeError(f'Signal preprocessing unit must inherit SignalPerprocessingUnit class while {type(environment)} do not.')
        self.signal_preprocessing_unit = signal_preprocessing_unit
        
        library_ok, problem_list = verify_neural_library(neural_library)
        if not library_ok:
            raise ImportError(f'Module {neural_library} lacks following compatibilities with PyNeat {problem_list}')
        self.neural_library = neural_library






class SignalPerprocessingUnit:
    '''
    Objects of this class are responsible for translating between Gym environment signals and 
    those used by neural networks. This is important for two reasons, first one is that it is 
    undesirable to propagate simulation specific data structures into decision model. 
    Second reason is that some of experimental models represent data in unique ways that cannot
    be directly translated into data representation used by simulation.
    Default preprocessing unit returns unmodified inputs an an such can work only with specific
    environments and network models.
    '''

    def __init__(self):
        pass

    def process_observation(self, observation):
        '''
        This function transforms Gym observation into a format used by the neural network.

            :param observation: Observation returned by gym.env.step
            :return: Observation in format expected by neural network
        '''
        return observation

    def process_reaction(self, reaction):
        '''
        This function processes network reaction into format acceptable by Gym environment.

            :param reaction: Reaction returned by network.activate
            :return: Reaction in format expected by gym.env.step
        '''
        return reaction
