import neat
import gym
import matplotlib.pyplot as plt
import numpy as np

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

def plot_fitness(statistics, ylog=False, view=False, filename='local/avg_fitness.svg'):
    generation = range(len(statistics.most_fit_genomes))
    best_fitness = [c.fitness for c in statistics.most_fit_genomes]
    avg_fitness = np.array(statistics.get_fitness_mean())
    stdev_fitness = np.array(statistics.get_fitness_stdev())

    plt.plot(generation, avg_fitness, 'b-', label="average")
    plt.plot(generation, avg_fitness - stdev_fitness, 'g-.', label="-1 sd")
    plt.plot(generation, avg_fitness + stdev_fitness, 'g-.', label="+1 sd")
    plt.plot(generation, best_fitness, 'r-', label="best")

    plt.title("Population's average and best fitness")
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.grid()
    plt.legend(loc="best")
    if ylog:
        plt.gca().set_yscale('symlog')

    plt.savefig(filename)
    if view:
        plt.show()

    plt.close()
