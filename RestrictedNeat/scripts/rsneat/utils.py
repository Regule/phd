import neat


def print_fields_recursively(name, obj, depth=1):
    tabulation = ' '*(depth-1)
    print(f'{tabulation}{name}:')
    tabulation = ' '*(depth)
    for field, value in obj.__dict__.items():
        if value.__str__ is not object.__str__:
            print(f'{tabulation}{field} --> {value}')
        else:
            print_fields_recursively(field, value, depth+1)

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
    print_fields_recursively('Configuration', config)
    return config
