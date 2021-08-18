'''
This is an example in which we can use multiple environments.
'''
import sys
import argparse
from time import sleep
from random import choice
from copy import deepcopy
import gym
import numpy as np
from gym import envs, spaces


#--------------------------------------------------------------------------------------------------
#                                        NEURAL NETWORK
#--------------------------------------------------------------------------------------------------

#-----------ACTIVATION FUNCTIONS-----------------

def unipolar(u):
    return 1/(1 + np.exp(-u))

def bipolar(u):
    return np.tanh(u)

def linear(u):
    return u

def relu(u):
    return np.maxmum.reduce(0,u)


ACTIVATION_FUNCTIONS = [unipolar, bipolar, linear, relu]

class NeuralLayer:
    '''
    This is a class that represents a single, multi neuron, layer in a neural network.
    '''

    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias

    def get_response(self, x):
        u = np.matmul(self.weights, x)
        u_prim = u + self.bias
        y = 1/(1 + np.exp(-u_prim))
        return y

    def mutate(self, factor):
        weights_mutation = (np.random.rand(*(self.weights.shape))*2-1)*factor
        bias_mutation = (np.random.rand(*(self.bias.shape))*2-1)*factor
        self.weights += weights_mutation
        self.bias += bias_mutation

    @staticmethod
    def generate_random_layer(input_size, layer_size):
        weights = np.random.rand(layer_size, input_size)*2-1
        bias = np.random.rand(layer_size)*(-1)
        return NeuralLayer(weights, bias)
