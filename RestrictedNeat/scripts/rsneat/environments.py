import gym

AVAILABLE_ENVIRONMENTS = None

class EnvironmentManager:

    def __init__(self):
        pass

    def get_environment_by_name(self, name, restricted_model_compatibile=False):
        if name not in AVAILABLE_ENVIRONMENTS.keys():
            raise KeyError(f'{name} is not valid environment name. Valid names are {AVAILABLE_ENVIRONMENTS,keys}')
        environment_class, initializer_parameters = AVAILABLE_ENVIRONMENTS[name]
        initializer_parameters['restricted_model_compatibile'] = restricted_model_compatibile
        return environment_class(**initializer_parameters)


class BipedalWalker(gym.envs.BipedalWalker):

    def __init__(self, hardcore=False, restricted_model_compatibile=False):
        super.__init__()
        self.hardcore = hardcore
        self.restricted_model_compatibile = restricted_model_compatibile


AVAILABLE_ENVIRONMENTS = {
        'BipedalWalker-v3': (BipedalWalker, {'hardcore':False})
        }
