'''
This module contains all classes and functions related to signal processing alongside used 
machine learning models.
'''

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

            @param observation Observation returned by gym.env.step
            @return Observation in format expected by neural network
        '''
        return observation

    def process_reaction(self, reaction):
        '''
        This function processes network reaction into format acceptable by Gym environment.

            @param reaction Reaction returned by network.activate
            @return Reaction in format expected by gym.env.step
        '''
        return reaction
