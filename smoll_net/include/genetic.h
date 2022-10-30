#ifndef GENETIC_H
#define GENETIC_H

#include <vector>
#include <list>
#include "agent.h"
#include "environment.h"


enum SelectionMode{
    SELECTION_ROULETTE,
    SELECTION_TOURNAMENT
};


struct MutationConfig{
    float probability;
    float stagnant_probability;
    float reroll_probability;
    MutationMode mode;
};


struct PopulationConfig{
    int size;
    int max_epochs;
    int stagnation_treshold;
};


struct SelectionConfig{
    int elite;
    int size;
    SelectionMode mode;
};

struct CrossoverConfig{
    bool enabled;
    bool multipoint;
};

struct TransferConfig{
  bool enabled;  
};

struct NetworkConfig{
  int layer_count;
  int input_size;
  std::vector<int> layer_sizes;
};

class GeneticConfiguration{
public:
    PopulationConfig population;
    SelectionConfig selection;
    MutationConfig mutation;
    CrossoverConfig crossover;
    TransferConfig transfer;
    NetworkConfig network;

    static GeneticConfiguration read_from_file(const char* filename);

    void describe(FILE* file) const;
};

struct FitnessInfo{
  float min;
  float avg;
  float max;
  int datapoint_count;

  FitnessInfo();
  void add_datapoint(float value);
  void calculate_avg();
};

struct PopulationNode{
    NeuralAgent *agent;
    PopulationNode *nxt;

    PopulationNode(NeuralAgent *agent);
};

class Population{
private:
    PopulationNode *head;
    int size;
    FitnessInfo fitness;

    bool ordered;
    bool fitness_updated;

    void insert_core(NeuralAgent *agent, bool ordered, bool copy);
    Population *copy_core(bool deep) const;

public:
    Population();
    ~Population();

    Population *shallow_copy() const;
    Population *deep_copy() const;

    void insert(NeuralAgent *agent);
    void insert_copy(NeuralAgent *agent);
    void insert_unordered(NeuralAgent *agent);
    void insert_copy_unordered(NeuralAgent *agent);

    NeuralAgent *pop();
    NeuralAgent *pop_random();
    NeuralAgent *peek() const;
    NeuralAgent *peek_random() const;

    void sort();
    FitnessInfo assign_fitness(Environment *env, int max_cycles);
    void purge();

    int get_size() const;
    FitnessInfo get_fitness() const;
    bool is_empty() const;
    bool is_sorted() const;
    bool is_fitness_updated() const;
};

class GeneticAlgorightm{

private:
    GeneticConfiguration config;
    Population *population;
    int epoch;
    std::list<FitnessInfo> history;

public:
    GeneticAlgorightm(GeneticConfiguration config);
    FitnessInfo step();
    std::list<FitnessInfo> run();
    std::list<FitnessInfo> run(int epochs);
    std::list<FitnessInfo> get_history() const;
    

    FitnessInfo assign_fitness(Environment *env, Population *population);
    Population *generate_initial_population() const;
    Population *run_selection(Population *base_population) const;
    Population *run_crossover(Population *breeding_pool) const;
    void run_mutation(Population *pure_agents) const;
    void run_transfer(Population *pure_agents) const;

};

#endif
