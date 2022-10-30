#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <stdbool.h>
#include "agent.h"

using std::vector;

typedef Numeric (*activation_function_t)(Numeric a);


//=================================================================================================
//                                    ACTIVATION FUNCTIONS
//=================================================================================================

// Null activation function
static Numeric activation_function_none(Numeric a){
	return 0;
}

// Identity activation function
static Numeric activation_function_identity(Numeric a){
	return a;
}

// Linear activation function
static Numeric activation_function_linear(Numeric a){
	return a;
}

// Rectified Linear Unit (ReLU) activation function
static Numeric activation_function_relu(Numeric a){
    return a>=0?a:0;
	
}

// Leaky Rectified Linear Unit (Leaky ReLU) activation function
static Numeric activation_function_leaky_relu(Numeric a){
    return a>0?a:a*0.01;
}

// Threshold activation function
static Numeric activation_function_threshold(Numeric a){
    return a > 0;
}

// Sigmoid activation function using a lookup table
static Numeric activation_function_sigmoid(Numeric a){
	// Sigmoid outputs
	const Numeric s[] = {0.0,0.000045,0.000123,0.000335,0.000911,0.002473,0.006693,0.017986,0.047426,0.119203,0.268941,0.500000,0.731059,0.880797,0.952574,0.982014,0.993307,0.997527,0.999089,0.999665,0.999877,0.999955,1.0};
		int index;
	Numeric fraction = 0;

	index = floor(a) + 11;
	if (index < 0)
		index = 0;
	else if (index > 21)
		index = 21;
	else
		fraction = a - floor(a);
	return s[index] + (s[index + 1] - s[index]) * fraction;
}


// Fast Tanh activation function
static Numeric activation_function_tanh(Numeric a){
	return a / (1.0f + abs(a));
}

// These must be in the same order as the enum activation_function_type
static activation_function_t activation_function[] = {
	activation_function_none,
	activation_function_identity,
	activation_function_linear,
	activation_function_relu,
	activation_function_leaky_relu,
	activation_function_threshold,
	activation_function_sigmoid,
	activation_function_tanh
};

//=================================================================================================
//                                    OTHER MATH FUNCTIONS
//=================================================================================================

// Returns Numericing point random number between 0 and 1
static Numeric frand(void)
{
	return rand() / (Numeric)RAND_MAX;
}

// Computes the error given a cost function
static Numeric error(Numeric a, Numeric b)
{
	return 0.5f * (a - b) * (a - b);
}

// Computes derivative of the error through the derivative of the cost function
static Numeric error_derivative(Numeric a, Numeric b)
{
	return a - b;
}

Numeric random_weight(){
    float random_value = static_cast<float>(rand())/static_cast<float>(RAND_MAX);
    return Numeric(random_value);
}

//=================================================================================================
//                                       NEURAL AGENT
//=================================================================================================

NeuralAgent::NeuralAgent(int layer_count, int input_size){
    this->layer_count = layer_count;
    this->input_size = input_size;
    this->layer_sizes = vector<int>(layer_count, 0);
    this->activation_functions = vector<ActivationType>(layer_count, ACTIVATION_NONE);
    this->layer_biases = vector<Numeric>(layer_count, 0);
    this->neuron_responses = vector< vector<Numeric> >(layer_count);
    this->neuron_weights = vector< vector< vector<Numeric> > >(layer_count);
    this->fitness = 0.0;
}


bool NeuralAgent::configure_layer(int layer, int layer_size, ActivationType activation, Numeric bias){
    if(layer>=layer_count||layer_sizes[layer]!=0){
        return false;
    }
    
    int layer_input_size = layer==0?input_size:layer_sizes[layer-1];
    layer_sizes[layer]=layer_size;
    activation_functions[layer] = activation;
    layer_biases[layer] = bias;
    neuron_responses[layer] = vector<Numeric>(layer_size, 0);
    neuron_weights[layer] = vector< vector<Numeric> >(layer_size);
    for(int neuron=0; neuron<layer_size; neuron++){
        neuron_weights[layer][neuron] = vector<Numeric>(layer_input_size);
        for(int weight=0; weight<layer_input_size; weight++){
            neuron_weights[layer][neuron][weight] = random_weight();
        }
    }
    return true;
}

NeuralAgent *NeuralAgent::copy(){
    NeuralAgent *agent = new NeuralAgent(this->layer_count, this->input_size);
    agent->layer_sizes = this->layer_sizes;
    agent->activation_functions = this->activation_functions;
    agent->layer_biases = this->layer_biases;
    agent->neuron_responses = this->neuron_responses;
    agent->neuron_weights = this->neuron_weights;
    agent->fitness = this->fitness;
    return agent;
}
    
void NeuralAgent::save(const char *path){
	FILE *file;

	file = fopen(path, "w");
	if (NULL == file)
		return;
	fprintf(file, "%d %d\n", layer_count, input_size);
	for(int layer = 0; layer < layer_count; layer++){
		fprintf(file, "%d %d %f\n", layer_sizes[layer], activation_functions[layer], layer_biases[layer]);
    }
    
	for(int layer = 0; layer < layer_count; layer++){
		for(int neuron = 0; neuron < layer_sizes[layer]; neuron++){
            int layer_input_size = layer==0?input_size:layer_sizes[layer-1];
            for (int weight = 0; weight < layer_input_size; weight++){
				fprintf(file, "%f\n", neuron_weights[layer][neuron][weight]);
            }
        }
    }
	fclose(file);
}

NeuralAgent *NeuralAgent::load(const char *path){
    FILE *file;
    int layer_count, input_size; 

	file = fopen(path, "r");
	if (NULL == file)
		return NULL;
    
	fscanf(file, "%d %d\n", &layer_count, &input_size);
	NeuralAgent *network = new NeuralAgent(layer_count, input_size);
    
    for (int layer = 0; layer < layer_count; layer++) {
        int layer_size, activation;
        float bias;
		fscanf(file, "%d %d %f\n", &layer_size, &activation, &bias);
        network->configure_layer(layer, layer_size, static_cast<ActivationType>(activation), Numeric(bias));
	}
	// Read in the weights
	for (int layer = 0; layer < layer_count; layer++){
		for (int neuron = 0; layer < network->layer_sizes[layer]; layer++){
            int layer_input_size = layer==0?input_size:network->layer_sizes[layer-1];
			for (int weight = 0; weight < layer_input_size; weight++){
				float weight_value;
                fscanf(file, "%f\n", &weight_value);
                network->neuron_weights[layer][neuron][weight] = Numeric(weight_value);
            }
        }
    }
	fclose(file);
	return network;
}

    
int NeuralAgent::get_layer_count() const{
    return this->layer_count;
}
    
int NeuralAgent::get_layer_size(int layer_id) const{
    return this->layer_sizes[layer_id];
}

vector<Numeric> NeuralAgent::get_reaction(const std::vector<Numeric> &observation){
    if(observation.size()!=input_size){
        fprintf(stderr,"Expected observation size %d got %lu\n", input_size, observation.size());
        return vector<Numeric>(1,0);
    }

    for (int neuron = 0; neuron < layer_sizes[0]; neuron++) {
			Numeric aggregation = 0;
			for (int weight = 0; weight < input_size; weight++){
				aggregation += observation[weight] * neuron_weights[0][neuron][weight];
            }
			aggregation += layer_biases[0];
			neuron_responses[0][neuron] = activation_function[activation_functions[0]](aggregation);
    }

    
    for(int layer=1; layer<layer_count; layer++){
         for (int neuron = 0; neuron < layer_sizes[layer]; neuron++) {
			Numeric aggregation = 0;
			for (int weight = 0; weight < input_size; weight++){
				aggregation += neuron_responses[layer-1][weight] * neuron_weights[layer][neuron][weight];
            }
			aggregation += layer_biases[layer];
			neuron_responses[layer][neuron] = 0;//activation_function[activation_functions[layer]](aggregation);
        }
    }
    
    
    vector<Numeric> reaction = neuron_responses[layer_count-1];
    return reaction;

}

void NeuralAgent::describe(FILE* file) const{
    fprintf(file, "Neural network containst %d layers.\n", layer_count);
    for(int layer=0; layer<layer_count; layer++){
        int layer_input_size = layer==0?input_size:layer_sizes[layer-1];
        fprintf(file, "Layer %d, bias=%f activation_id=%d ", layer, layer_biases[layer], activation_functions[layer]);
        fprintf(file, "input_size=%d layer_size=%d\n", layer_input_size, layer_sizes[layer]);
        for(int neuron=0; neuron<layer_sizes[layer]; neuron++){
            fprintf(file, "  [");
            for(int weight=0; weight<layer_input_size; weight++){
                fprintf(file, "%f", neuron_weights[layer][neuron][weight]);
                if(weight<layer_input_size-1){
                    fprintf(file, " ");
                }
            }
            fprintf(file, "]\n");
        }
    }
}

bool NeuralAgent::operator==(const NeuralAgent &other) const{
    if(layer_count!=other.layer_count || input_size!=other.input_size) return false;
    for(int layer=0; layer<layer_count; layer++){
        if(layer_sizes[layer]!=other.layer_sizes[layer]) return false;
    }
    for(int layer=0; layer<layer_count; layer++){
         int layer_input_size = layer==0?input_size:layer_sizes[layer-1];
         for(int neuron=0; neuron<layer_sizes[layer]; neuron++){
            for(int weight=0; weight<layer_input_size; weight++){
                if(neuron_weights[layer][neuron][weight]-neuron_weights[layer][neuron][weight]>EPSILON||
                    neuron_weights[layer][neuron][weight]-neuron_weights[layer][neuron][weight]<0-EPSILON)
                    return false;
            }
        }
    }
    return true;
}

bool NeuralAgent::operator!=(const NeuralAgent &other) const{
    return !(*this==other);
}

void NeuralAgent::reroll(){
    for(int layer=0; layer<layer_count; layer++){
        int layer_input_size = layer==0?input_size:layer_sizes[layer-1];
        for(int neuron=0; neuron<layer_sizes[layer]; neuron++){
            neuron_weights[layer][neuron] = vector<Numeric>(layer_input_size);
            for(int weight=0; weight<layer_input_size; weight++){
                neuron_weights[layer][neuron][weight] = random_weight();
            }
        }
    }
}

NeuralAgent *NeuralAgent::crossover(NeuralAgent *other, bool multipoint){
    NeuralAgent *offspring = new NeuralAgent(*this);
    
    if(this->layer_count != other->layer_count){
        fprintf(stderr, "Incompatibile layer count between parents (%d, %d). \n", this->layer_count, other->layer_count);
        return NULL;
    }
    
    if(this->input_size != other->input_size){
        fprintf(stderr, "Incompatibile input sizes between parents (%d, %d). \n", this->input_size, other->input_size);
        return NULL;
    }
    

    for(int layer=0; layer<layer_count; layer++){
        
        if(this->layer_sizes[layer] != other->layer_sizes[layer]){
            fprintf(stderr, "Incompatibile layer sizes between parents (%d, %d) for layer %d. \n", this->layer_sizes[layer], other->layer_sizes[layer], layer);
            return NULL;
        }
        
        int layer_input_size = layer==0?input_size:layer_sizes[layer-1];
        int total_genes_in_layer = layer_sizes[layer]*layer_input_size;
        int crossover_point = rand()%total_genes_in_layer;
        
        for(int neuron=0; neuron<layer_sizes[layer]; neuron++){
            neuron_weights[layer][neuron] = vector<Numeric>(layer_input_size);
            for(int weight=0; weight<layer_input_size; weight++){
                if(multipoint){
                    if(static_cast<float>(rand())/static_cast<float>(RAND_MAX)<0.5){
                        offspring->neuron_weights[layer][neuron][weight] = neuron_weights[layer][neuron][weight];
                    }else{;
                        offspring->neuron_weights[layer][neuron][weight] = other->neuron_weights[layer][neuron][weight];
                    }
                }else{
                    if(neuron+weight<crossover_point){
                        offspring->neuron_weights[layer][neuron][weight] = neuron_weights[layer][neuron][weight];
                    }else{
                        offspring->neuron_weights[layer][neuron][weight] = other->neuron_weights[layer][neuron][weight];
                    }
                }
            }
        }
    }
    return offspring;
}

int NeuralAgent::mutate(float probability, MutationMode mode){
    int mutation_count = 0;
    if(mode==MUTATION_FULL){
        for(int layer=0; layer<layer_count; layer++){
            int layer_input_size = layer==0?input_size:layer_sizes[layer-1];
            for(int neuron=0; neuron<layer_sizes[layer]; neuron++){
                for(int weight=0; weight<layer_input_size; weight++){
                    if(static_cast<float>(rand())/static_cast<float>(RAND_MAX)<0.5){
                        neuron_weights[layer][neuron][weight] = random_weight();
                        mutation_count++;
                    }
                }
            }
        }
    }else{
        while(static_cast<float>(rand())/static_cast<float>(RAND_MAX)<0.5){
            mutation_count++;
            int layer = rand()%layer_count;
            int neuron = rand()%layer_sizes[layer];
            int layer_input_size = layer==0?input_size:layer_sizes[layer-1];
            int weight = rand()%layer_input_size;
            neuron_weights[layer][neuron][weight] = random_weight();
            if(mode==MUTATION_SINGLE) break;
        }
    }
    return mutation_count;
}



void NeuralAgent::update_fitness(float reward){
	fitness += reward;
}

void NeuralAgent::reset_fitness(){
	fitness = 0;
}

float NeuralAgent::get_fitness() const{
	return fitness;
}


