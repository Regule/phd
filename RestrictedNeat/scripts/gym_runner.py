'''
This script runs selected Open AI Gym environment and presents a pipe based interface for 
other programs to communicate with. Thanks to that it is possible to easily write code that
interacts with Gym in other languages.
'''

#==================================================================================================
#                                           IMPORTS
#==================================================================================================
import logging
import argparse
import gym
import numpy as np

#==================================================================================================
#                                            GLOBALS
#==================================================================================================

DEFAULT_LOGGER_LEVEL = logging.INFO
LOGGER_NAME = 'gym-runner'
LOGGER_FORMAT = '%(name)s %(levelname)s %(asctime)s:%(message)s'

logger = None # Global logger for this script

#==================================================================================================
#                                         PIPE INTERFACE 
#==================================================================================================

def float_to_acceptable_str(numeric):
    return f'{numeric:.4f}'

def write_observation(pipe_path, observation):
    out_pipe = open(pipe_path, 'w')
    features = list(map(float_to_acceptable_str,observation.tolist()))
    features = ' '.join(features)
    out_pipe.write(features)
    out_pipe.close()

def read_reaction(pipe_path):
    in_pipe = open(pipe_path, 'r')
    line = in_pipe.readline()
    in_pipe.close()
    numeric_values = list(map(float,line.split()))
    return np.array(numeric_values)

def write_metadata(metadata_pipe, cycle, reward, running, error_code, error_msg):
    pipe = open(metadata_pipe, 'w')
    pipe.write(f'{cycle} {reward} {1 if running else 0} {error_code} {error_msg}')
    pipe.close()

#==================================================================================================
#                                         GYM FUNCTIONS 
#==================================================================================================

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


def run_simulation(config):
    environment = gym.make(config.environment)
    while True:
        observation = environment.reset()
        reward = 0.0
        error_code = 0
        error_msg = 'OK'
        finished = False
        for cycle in range(config.max_cycles):
            write_observation(config.observation_pipe, observation)
            write_metadata(config.metadata_pipe, cycle, reward, not finished, error_code, error_msg)
            reaction = read_reaction(config.reaction_pipe)
            observation, reward, finished, _ = environment.step(reaction)
            if finished:
                logger.info(f'Finished simulation after {cycle} cycles.')
                write_observation(config.observation_pipe, observation)
                write_metadata(config.metadata_pipe, cycle, reward, not finished, error_code, error_msg)
                break

#==================================================================================================
#                                       UTILITY FUNCTIONS
#==================================================================================================

def setup_logger(logging_level=logging.INFO, log_file=None):
    global logger
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging_level)
    formatter = logging.Formatter(LOGGER_FORMAT)
    
    # Logging to stdout
    ch = logging.StreamHandler()
    ch.setLevel(logging_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    # Logging to file
    if log_file is not None:
        fileHandler = logging.FileHandler(log_file)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)

    logger.info("Started Logger")


def string_to_log_level(level_str):
    level_map = {
            'critical': logging.CRITICAL,
            'error': logging.ERROR,
            'warining': logging.WARNING,
            'info': logging.INFO,
            'debug': logging.DEBUG,
            'silent': logging.CRITICAL
            }
    try:
        return level_map[level_str]
    except KeyError:
        return logging.INFO


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-e', '--environment', type=str, required=True,
            help='An AI Gym environment name.')
    parser.add_argument('--max_generations', type=int, default=100,
            help='Maximum number of generations for which algorithm will work.')
    parser.add_argument('--max_cycles', type=int, default=500,
            help='Maximum number of cycles for which simulation will be ran')
    parser.add_argument('--break_punishment', type=float, default=-100.0,
            help='Punishment for failure that causes simulation to stop early')
    parser.add_argument('--log_level', type=string_to_log_level, default=DEFAULT_LOGGER_LEVEL,
            help='Logging level, valid values: silent, critical, error, warning, info, debug')
    parser.add_argument('--log_file', type=str, default=None,
            help='If set logs will be written to this file.')
    parser.add_argument('--observation_pipe', type=str, default='/tmp/observation_pipe',
            help='File name of pipe to which runner will send observations')
    parser.add_argument('--reaction_pipe', type=str, default='/tmp/reaction_pipe',
            help='File name of pipe from which runner will read reactions')
    parser.add_argument('--metadata_pipe', type=str, default='/tmp/metadata_pipe',
            help='File name of pipe from which runner will read reactions')
    return parser.parse_args()


#==================================================================================================
#                                       MAIN FUNCTION
#==================================================================================================

def main(args):
    setup_logger(args.log_level, args.log_file)
    try:
        run_simulation(args)
    except KeyboardInterrupt:
        logger.info('Manually stopped program execution.')

if __name__ == '__main__':
    main(parse_arguments())

if logger is None:
    setup_logger()
