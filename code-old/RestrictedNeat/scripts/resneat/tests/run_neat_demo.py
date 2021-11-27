'''
This scripts allows a execution of a simple run of Pyneat with our libraries as a 
overseer.
It should be ran to manually test results generated.
'''

import neat
from resneat.backend.signal_processing import SignalPreprocessingUnit
from resneat.backend.overseer import Overseer
from resneat.utils.visualisations import plot_statistics, plot_speciation 

def main():
    o = Overseer('BipedalWalker-v3', SignalPreprocessingUnit(), neat, 400)
    stats = neat.StatisticsReporter()
    o.run_neuroevolution('configs/walker.txt', 10, [neat.StdOutReporter(True), stats])
    plot_statistics(stats, 'Name', True, 'local/test.png', 'local/test.csv')
    plot_speciation(stats, 'Name', True, 'local/spec.png', 'local/spec_.csv')

if __name__ == '__main__':
    main()
