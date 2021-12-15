import neat
import gym


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
