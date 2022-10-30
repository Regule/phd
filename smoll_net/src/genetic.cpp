#include "genetic.h"

//=================================================================================================
//                                       PARSING FUNCTIONS
//=================================================================================================

int read_int(FILE *file){
	static char value[10];
	fscanf(file, "%s\n", value);
	return atoi(value);
}

float read_float(FILE *file){
	static char value[10];
	fscanf(file, "%s\n", value);
	return atof(value);
}

SelectionMode read_mode(FILE *file){
	static char value[10];
	fscanf(file, "%s\n", value);
	return value[0]=='r'?SELECTION_ROULETTE:SELECTION_TOURNAMENT;
}

bool read_bool(FILE* file){
	static char value[10];
	fscanf(file, "%s\n", value);
	return value[0]=='t';
}

//=================================================================================================
//                                     GENETIC CONFIGURATION
//=================================================================================================
GeneticConfiguration GeneticConfiguration::read_from_file(const char* filename){
	GeneticConfiguration config;
	FILE *file;
	int layer_count, input_size;

	file = fopen(filename, "r");
	if (NULL == file)
		return config;

	config.population.size = read_int(file);
	config.population.max_epochs = read_int(file);
	config.population.stagnation_treshold = read_int(file);
	config.selection.size = read_int(file);
	config.selection.elite = read_int(file);
	config.selection.mode = read_mode(file);
	config.mutation.probability = read_float(file);
	config.mutation.stagnant_probability = read_float(file);
	config.mutation.reroll_probability = read_float(file);
	config.crossover.enabled = read_bool(file);
	config.crossover.multipoint = read_bool(file);
	config.transfer.enabled = read_bool(file);

	int layer_size;
	fscanf(file, "%d %d", &(config.network.layer_count), &(config.network.input_size));
	config.network.layer_sizes = std::vector<int>(config.network.layer_count);
	for(int layer=0; layer<config.network.layer_count; layer++){
		fscanf(file, "%d", &layer_size);
		config.network.layer_sizes[layer] = layer_size;
	}

	return config;
}

void GeneticConfiguration::describe(FILE* file) const{
	fprintf(file,"GENETIC ALGORITHM CONFIGURATION :\n");
	fprintf(file,"  Population size = %d\n", population.size);
	fprintf(file,"  Max epochs = %d\n", population.max_epochs);
	fprintf(file,"  Epochs till stagnation = %d\n", population.stagnation_treshold);
	fprintf(file,"  Agent count after selection = %d\n", selection.size);
	fprintf(file,"  Elite size = %d\n", selection.elite);
	fprintf(file,"  Population size = %d\n", population.size);
	fprintf(file,"  Selection mode = %s\n", selection.mode==SELECTION_ROULETTE?"roulette":"tournament");
	fprintf(file,"  Mutation probability = %f\n", mutation.probability);
	fprintf(file,"  Mutation probability during stagnation = %f\n", mutation.stagnant_probability);
	fprintf(file,"  Complete reroll (mutation of all genes) probability = %f\n", mutation.reroll_probability);
	fprintf(file,"  Crossover enabled = %s\n", crossover.enabled?"true":"false");
	fprintf(file,"  Multipoint crossover = %s\n", crossover.multipoint?"true":"false");
	fprintf(file,"  Transfer enabled = %s\n", transfer.enabled?"true":"false");
	fprintf(file,"  Layer count = %d\n", network.layer_count);
	fprintf(file,"  Input size = %d\n", network.input_size);
	fprintf(file,"  Hidden layers sizes = ");
	for(int layer=0; layer<network.layer_count-1; layer++){
		fprintf(file, "%d ", network.layer_sizes[layer]);
	}
	fprintf(file,"\n  Output size = %d\n", network.layer_sizes[network.layer_count-1]);
}

//=================================================================================================
//                                       FITNESS INFO
//=================================================================================================

  FitnessInfo::FitnessInfo(){
  	this->min = 0.0;
  	this->avg = 0.0;
  	this->max = 0.0;
  	this->datapoint_count = 0;
  }

  void FitnessInfo::add_datapoint(float value){
  	min += value;
  	max += value;
  	avg += value;
  	datapoint_count++;
  }

  void FitnessInfo::calculate_avg(){
  	avg /= datapoint_count;
  }

//=================================================================================================
//                                        POPULATION
//=================================================================================================

PopulationNode::PopulationNode(NeuralAgent *agent){
	this->agent = agent;
	this->nxt = NULL;
}

Population::Population(){
	head = NULL;
	size = 0;
	ordered = true;
	fitness_updated = false;
}

Population::~Population(){
	PopulationNode *last;
	while(head != NULL){
		last = head;
		head = head->nxt;
		delete(last);
	}
}

Population *Population::copy_core(bool deep) const{
	PopulationNode *agent = this->head;
	Population *copy = new Population();
	while(agent != NULL){
		if(deep){
			copy->insert_copy_unordered(agent->agent);
		}else{
			copy->insert_unordered(agent->agent);
		}
		agent = agent->nxt;
	}
	copy->ordered = this->ordered;
	copy->fitness_updated = this->fitness_updated;
	return copy;
}

Population *Population::shallow_copy() const{
	return copy_core(false);
}

Population *Population::deep_copy() const{
	return copy_core(true);
}

void Population::insert_core(NeuralAgent *agent, bool ordered, bool copy){
	PopulationNode *last = NULL;
	PopulationNode *node = head;
	
	if(ordered){
		while(node!=NULL && node->agent->get_fitness()>agent->get_fitness()){
			last = node;
			node = node->nxt;
		}
	}else{
		this->ordered = false;
	}

	if(copy){
		agent = agent->copy();
	}

	PopulationNode *new_node = new PopulationNode(agent);
	if(last == NULL){
		head = new_node;
	}else{
		last->nxt = new_node;
	}
	new_node->nxt = node;
	size++;
	fitness_updated = false;
}

void Population::insert(NeuralAgent *agent){
	insert_core(agent, true, false);
}

void Population::insert_copy(NeuralAgent *agent){
	insert_core(agent, true, true);
}

void Population::insert_unordered(NeuralAgent *agent){
	insert_core(agent, false, false);
}

void Population::insert_copy_unordered(NeuralAgent *agent){
	insert_core(agent, false, true);
}

NeuralAgent *Population::pop(){
	if(head == NULL){
		return NULL;
	}

	NeuralAgent *agent = head->agent;
	PopulationNode *removed_node = head;
	head = head->nxt;
	delete(removed_node);
	size--;
	return agent;
}

NeuralAgent *Population::pop_random(){
	if(size==0){
		return NULL;
	}
	int index = rand()%size;
	//fprintf(stderr,"Poping index %d of %d\n", index, size);
	PopulationNode *node=head;
	PopulationNode *last=NULL;
	while(index>0){
		//fprintf(stderr,"Node=%p  nxt=%p\n", node, node->nxt);
		last=node;
		node = node->nxt;
		index--;
	}

	//fprintf(stderr,"Removing popped node\n");
	if(last!=NULL){
		//fprintf(stderr,"Last is not null.\n");
		last->nxt = node->nxt;
	}else{
		head = node->nxt;
	}

	NeuralAgent *agent = node->agent;
	delete(node);
	size--;
	//fprintf(stderr,"Reurning popped element.\n");
	return agent;
}

NeuralAgent *Population::peek() const{
	return head==NULL?NULL:head->agent;
}

NeuralAgent *Population::peek_random() const{
	if(size==0){
		return NULL;
	}
	int index = rand()%size;
	PopulationNode *node=head;
	PopulationNode *last=NULL;
	while(index>0){
		node = node->nxt;
		index--;
	}
	return node->agent;
}

void Population::sort(){
	PopulationNode *node = head;
	PopulationNode *last = NULL;
	size = 0;
	head = NULL;
	ordered = true;
	while(node!=NULL){
		last = node;
		insert(node->agent);
		node = node->nxt;
		delete(last);
	}
}

FitnessInfo Population::assign_fitness(Environment *env, int max_cycles){
	FitnessInfo info;
	info.min=0.0;
	info.avg=0.0;
	info.max=0.0;
	PopulationNode *node = head;
	while(node != NULL){
		NeuralAgent *agent = node->agent;
		env->reset();
		int cycle = 0;
		agent->reset_fitness();
		while(env->is_running() && (max_cycles==0||cycle<=max_cycles)){
			agent->update_fitness(env->send_reaction(agent->get_reaction(env->get_observation())));
			cycle++;
		}
		info.add_datapoint(agent->get_fitness());
		node = node->nxt;
	}
	info.calculate_avg();
	this->fitness = info;
	return info;
}

int Population::get_size() const{
	return size;
}

FitnessInfo Population::get_fitness() const{
	return fitness;
}

bool Population::is_empty() const{
	return size == 0;
}

bool Population::is_sorted() const{
	return ordered;
}

bool Population::is_fitness_updated() const{
	return fitness_updated;
}

void Population::purge(){
	PopulationNode *last;
	while(head != NULL){
		delete(head->agent);
		last = head;
		head = head->nxt;
		delete(last);
	}
	size = 0;
	ordered = true;
	fitness_updated = false;
}




//=================================================================================================
//                                     GENETIC ALGORITHM
//=================================================================================================


GeneticAlgorightm::GeneticAlgorightm(GeneticConfiguration config){
	this->config = config;
	this->population = NULL;
	this->epoch = 0;
}


Population *GeneticAlgorightm::generate_initial_population() const{
	Population *initial_generation = new Population();
	for(int agent_number=0; agent_number<config.population.size; agent_number++){
		NeuralAgent *agent = new NeuralAgent(config.network.layer_count, config.network.input_size);
		for(int layer=0; layer<config.network.layer_count; layer++){
			agent->configure_layer(layer, config.network.layer_sizes[layer], ACTIVATION_IDENTITY, 0.0);
		}
		initial_generation->insert_unordered(agent);
	}
	return initial_generation; 
}


Population *GeneticAlgorightm::run_selection(Population *base_population) const{
	Population *selection_pool = base_population->shallow_copy();
	Population *breeding_pool = new Population();
	while(!selection_pool->is_empty()){
		NeuralAgent *contestant1, *contestant2, *winner;
		contestant1 = selection_pool->pop_random();
		if(selection_pool->is_empty()){
			winner = contestant1;
		}else{
			contestant2 = selection_pool->pop_random();
			winner = contestant1->get_fitness()>contestant2->get_fitness()?contestant1:contestant2;
		}
		breeding_pool->insert_copy(winner);
	}
	delete(selection_pool);
	return breeding_pool;
}

Population *GeneticAlgorightm::run_crossover(Population *breeding_pool) const{
	Population *new_generation = new Population();
	while(new_generation->get_size()<config.population.size){
		NeuralAgent *parentA = breeding_pool->peek_random();
		NeuralAgent *parentB = breeding_pool->peek_random();
		new_generation->insert_unordered(parentA->crossover(parentB, config.crossover.multipoint));
	}
	return new_generation;
}

void GeneticAlgorightm::run_mutation(Population *pure_agents) const{
	Population *mutants = pure_agents->shallow_copy();
	while(!mutants->is_empty()){
		NeuralAgent *agent = mutants->pop();
		agent->mutate(config.mutation.probability, config.mutation.mode);
	}
	delete(mutants);
}

void GeneticAlgorightm::run_transfer(Population *pure_agents) const{
}

