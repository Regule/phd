'''
Final script with custom visualisation and full use of configuration object before starting
work on final version of code.
'''
import neat
import gym
import argparse




def main(args):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         args.configuration)
    config.__dict__.update(args.__dict__) # An ugly hack that will add our fields to config object
    print('CONFIGURATION')
    for key, value in config.__dict__.items():
        print(f'{key} --> {value}')


def parser_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-c', '--configuration', type=str, required=True,
            help='Path to configuration file.')
    parser.add_argument('-e', '--environment', type=str, required=True,
            help='An AI Gym environment name.')
    return parser.parse_args()


if __name__ == '__main__':
    main(parser_arguments())
