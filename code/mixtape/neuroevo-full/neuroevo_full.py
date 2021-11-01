'''
Final script with custom visualisation and full use of configuration object before starting
work on final version of code.
'''
import neat
import gym
import argparse


def run_simulation(population, config):
    environment = gym.make(config.environment)
    top_genome = None

    for genome_id, genome in population:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = 0.0
        observation = environment.reset()
        finished = False
        for _ in range(500):
            reaction = net.activate(observation) 
            observation, reward, finished, _ = environment.step(reaction)
            genome.fitness += reward
            if finished:
                genome.fitness = -1000.0
                break
        if top_genome is None or genome.fitness > top_genome.fitness:
            top_genome = genome
    print(f'Best specimen fitness is {top_genome.fitness}')

def main(args):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         args.configuration)
    config.__dict__.update(args.__dict__) # An ugly hack that will add our fields to config object
    print('CONFIGURATION')
    for key, value in config.__dict__.items():
        print(f'{key} --> {value}')
    population = neat.Population(config)
    winner = population.run(run_simulation, 100)
    #show_agent_behaviour(winner, 500, config)
    #draw_net(config, winner, True)


def parser_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-c', '--configuration', type=str, required=True,
            help='Path to configuration file.')
    parser.add_argument('-e', '--environment', type=str, required=True,
            help='An AI Gym environment name.')
    return parser.parse_args()


if __name__ == '__main__':
    main(parser_arguments())
