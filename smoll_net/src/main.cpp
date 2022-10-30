#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <vector>
#include "agent.h"
#include "environment.h"
#include "genetic.h"

int main(int argc, char** argv){

    time_t t;
    srand((unsigned) time(&t));

    printf("========================== TESTING SAVING AND LOADING NETWORK  ==========================\n\n");
    printf("STARTING \n");
    srand(time(NULL));
    NeuralAgent *network = new NeuralAgent(3,10);
    network->configure_layer(0, 5, ACTIVATION_NONE, 0.3);
    network->configure_layer(1, 3, ACTIVATION_NONE, 0.3);
    network->configure_layer(2, 8, ACTIVATION_NONE, 0.3);
    network->save("test.txt");

    NeuralAgent *network_from_file = NeuralAgent::load("test.txt");
    if(*network!=*network_from_file){
        printf("WRITING AND READING FROM FILE DO NOT WORK CORRECTLY\n\n");
        printf("SOURCE NETWORK:\n");
        network->describe(stdout);
        printf("\nTARGET NETWORK:\n");
        network_from_file->describe(stdout);
    }else{
        printf("READING AND WRITING NETWORK WORKS OK.\n");
    }

    delete(network);
    delete(network_from_file);
    printf("DELETING NETWORKS WORKS FINE\n");

    network = NeuralAgent::load("test.txt");

    std::vector<Numeric> observation = std::vector<Numeric>(10);

    printf("========================== TESTING NETWORK BASIC FUNCTIONALITY ==========================\n\n");

    std::vector<Numeric> reaction = network->get_reaction(observation);

    printf("READING REACTION WORKS !\n");
    printf("reaction -> [");
    for(int i=0; i<10; i++){
	printf("%f",reaction[i]);
	if(i<9){
           printf(" ");
	}
	printf("]\n");
    }

    delete(network);
    printf("CLEANUP WORKS\n");

    NeuralAgent *network_a = new NeuralAgent(3,10);
    network_a->configure_layer(0, 5, ACTIVATION_IDENTITY, 0.3);
    network_a->configure_layer(1, 3, ACTIVATION_IDENTITY, 0.3);
    network_a->configure_layer(2, 8, ACTIVATION_IDENTITY, 0.3);

    NeuralAgent *network_b = new NeuralAgent(3,10);
    network_b->configure_layer(0, 5, ACTIVATION_IDENTITY, 0.3);
    network_b->configure_layer(1, 3, ACTIVATION_IDENTITY, 0.3);
    network_b->configure_layer(2, 8, ACTIVATION_IDENTITY, 0.3);

    NeuralAgent* offspring = network_a->crossover(network_b, true);
    int mutations = offspring->mutate(0.7, MUTATION_FULL);
    printf("Total of %d genes were mutated.\n", mutations);

    printf("=============================== TESTING CONTROL LOOP ==============================\n\n");

    NeuralAgent *test_network = new NeuralAgent(1,10);
    test_network->configure_layer(0, 8, ACTIVATION_IDENTITY, 0.01);
    test_network->describe(stdout);

    CsvRecordedEnvironment *env = CsvRecordedEnvironment::load_data("test_dataset.csv", 10, 8);
    printf("Observation size = %d Reaction size = %d\n", env->get_observation_size(), env->get_reaction_size());
    while(env->is_running()){
        test_network->update_fitness(env->send_reaction(test_network->get_reaction(env->get_observation())));
    }
    printf("Fitness after test run (%d cycles) = %f\n", env->get_cycle(), test_network->get_fitness());

    printf("========================== TESTING CONFIGURATION READING ==========================\n\n");
    GeneticConfiguration config = GeneticConfiguration::read_from_file("config.txt");
    config.describe(stdout);

    printf("============================ TESTING IF GENETIC STEPS ============================\n\n");
    GeneticAlgorightm algorithm(config);
    Population *test_population = algorithm.generate_initial_population();
    test_population->peek()->describe(stdout);
    FitnessInfo info = test_population->assign_fitness(env, 0);
    printf("Fitness min=%f avg=%f max=%f\n", info.min, info.avg, info.max);
    printf("Running selection.\n");
    Population *breeding_base = algorithm.run_selection(test_population);
    printf("Purging old population.\n");
    test_population->purge();
    printf("Purged population size is %d\n", test_population->get_size());
    printf("Breeding base size is %d\n", breeding_base->get_size());
    delete(test_population);
    printf("Example of breeder:\n");
    breeding_base->peek_random()->describe(stdout);
    Population *new_generation = algorithm.run_crossover(breeding_base);
    breeding_base->purge();
    delete(breeding_base);
    printf("New generation  size is %d\n", new_generation->get_size());
    
    info = new_generation->assign_fitness(env, 0);
    printf("Fitness before mutation min=%f avg=%f max=%f\n", info.min, info.avg, info.max);
    algorithm.run_mutation(new_generation);
    
    info = new_generation->assign_fitness(env, 0);
    printf("Fitness after mutation min=%f avg=%f max=%f\n", info.min, info.avg, info.max);
    algorithm.run_mutation(new_generation);
    info = new_generation->assign_fitness(env, 0);
    printf("Fitness after mutation min=%f avg=%f max=%f\n", info.min, info.avg, info.max);
    algorithm.run_mutation(new_generation);
    info = new_generation->assign_fitness(env, 0);
    printf("Fitness after mutation min=%f avg=%f max=%f\n", info.min, info.avg, info.max);

}

