import neat
import gym
import argparse

ALLOWED_ENVIRONMENTS = ['BipedalWalker-v3']


def verify_arguments(args):
    '''
    This function is used to check additionall restrictions on argument values. 
    It is done this way as just using verification functions within argparse limits ability
    to check and respond to errors.

    @param args Result of ArgumentParser.parse_args()
    @returns None
    '''
    if args.environment not in ALLOWED_ENVIRONMENTS:
        raise ValueError(f'Environment {args.environment} is not allowed, available environments are {ALLOWED_ENVIRONMENTS}')

def prepare_config(args):
    '''
    This is function that loads neat configuration file as well as adds additional fields to 
    it. This addition is a dirty hack but it was implemented due to time constrains.

    @param args Arguments from command line
    @return A congfiguration object
    '''
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         args.configuration)
    config.__dict__.update(args.__dict__) # An ugly hack that will add our fields to config object
    print('CONFIGURATION')
    for key, value in config.__dict__.items():
        print(f'{key} --> {value}')
    return config


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

def run_simulation(population, config):
    environment = gym.make(config.environment)
    top_genome = None

    for genome_id, genome in population:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = 0.0
        observation = environment.reset()
        finished = False
        for _ in range(config.max_cycles):
            reaction = net.activate(observation) 
            observation, reward, finished, _ = environment.step(reaction)
            genome.fitness += reward
            if finished:
                genome.fitness -= config.break_punishment 
                break
        if top_genome is None or genome.fitness > top_genome.fitness:
            top_genome = genome
    print(f'Best specimen fitness is {top_genome.fitness}')

def run_classic_neat(config):
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    winner = population.run(run_simulation, config.max_generations)
    show_agent_behaviour(winner, config)

def parser_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-c', '--configuration', type=str, required=True,
            help='Path to configuration file.')
    parser.add_argument('-e', '--environment', type=str, required=True,
            help='An AI Gym environment name.')
    parser.add_argument('--max_generations', type=int, default=100,
            help='Maximum number of generations for which algorithm will work.')
    parser.add_argument('--max_cycles', type=int, default=500,
            help='Maximum number of cycles for which simulation will be ran')
    parser.add_argument('--break_punishment', type=float, default=-100.0,
            help='Punishment for failure that causes simulation to stop early')
    return parser.parse_args()

def main():
    args = None
    try:
        args = parser_arguments()
        verify_arguments(args)
    except ValueError as e:
        print('Error occured when parisng command line arguments:')
        print(e)
        return
    config = prepare_config(args)
    run_classic_neat(config)

if __name__ == '__main__':
    main()
