#ifndef AGENT_H
#define AGENT_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <vector>
#include "numeric.h"




enum ActivationType {
	ACTIVATION_NONE = 0,
	ACTIVATION_IDENTITY,
	ACTIVATION_LINEAR,
	ACTIVATION_RELU,
	ACTIVATION_LEAKY_RELU,
	ACTIVATION_THRESHOLD,
	ACTIVATION_SIGMOID,
	ACTIVATION_TANH,
};

enum MutationMode{
    MUTATION_SINGLE,
    MUTATION_CHAINGED,
    MUTATION_FULL
};



class NeuralAgent{
private:
    int layer_count;
    int input_size;
	std::vector<int> layer_sizes;
	std::vector<ActivationType> activation_functions;
	std::vector<Numeric> layer_biases;
	std::vector< std::vector< std::vector<Numeric> > > neuron_weights;
	std::vector< std::vector<Numeric> > neuron_responses;
	
    float fitness;

public:
    NeuralAgent(int layer_count, int input_size);
    bool configure_layer(int layer, int layer_size, ActivationType activation, Numeric bias);
    NeuralAgent *copy();

    void save(const char *path);
    static NeuralAgent *load(const char *path);

    int get_layer_count() const;
    int get_layer_size(int layer_id) const;
    bool operator==(const NeuralAgent &other) const;
    bool operator!=(const NeuralAgent &other) const;
    
    std::vector<Numeric> get_reaction(const std::vector<Numeric> &observation);
    
    NeuralAgent *crossover(NeuralAgent *other, bool multipoint);
    int mutate(float probability, MutationMode mode);
    void reroll();

    void update_fitness(float reward);
    void reset_fitness();
    float get_fitness() const;
    
    void describe(FILE* file) const;
};

#endif /* AGENT_H */

