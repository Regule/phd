'''
This module contains an Overseer class that is central element of experiment.
'''

import gym
import neat
from resneat.backend.signal_processing import SignalPreprocessingUnit

def verify_neural_library(neural_library):
    '''
    This class checks if selected neural_library provides required level of compatibility 
    with PyNeat.

        @param neural_library Module that handles neural network and neuroevolution functionality.
        @return Tuple that contains (True,None) if module provides compatibility or tuple that
                contains (False, List) if it does not. Returned list contains elements that are 
                not found in module.
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

            @param environment Name of default Gym environment or a object that is custom one.
            @param signal_preprocessing_unit Object that relay signals between Gym environment 
                                             and neural network.
            @param neural_library Module responsible for handling networks and neuroevolution
            @return Returns nothing
        '''
        if  isinstance(environment, str):
            self.environment = gym.make(environment)
        elif isinstance(environment, gym.Env):
            self.environment = environment
        else:
            raise TypeError(f'Overseer expects environment as either string or gym.Env object, instead recieved {type(environment)}.')
        
        if not isinstance(signal_preprocessing_unit, SignalPreprocessingUnit):
            raise TypeError(f'Signal preprocessing unit must inherit SignalPerprocessingUnit class while {type(environment)} do not.')
        self.signal_preprocessing_unit = signal_preprocessing_unit
        
        library_ok, problem_list = verify_neural_library(neural_library)
        if not library_ok:
            raise ImportError(f'Module {neural_library} lacks following compatibilities with PyNeat {problem_list}')
        self.neural_library = neural_library

        self.best_specimen = None
        self.population = None

    
