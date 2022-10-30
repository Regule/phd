#ifndef ENVIRONMENT_H
#define ENVIRONMENT_H

#include<vector>
#include "numeric.h"

class Environment{
public:
    virtual int get_observation_size() const = 0;
    virtual int get_reaction_size() const = 0;

    virtual const std::vector<Numeric> &get_observation() = 0;
    virtual float send_reaction(const std::vector<Numeric> &reaction) = 0;

    virtual int get_cycle() const = 0;
    virtual float get_last_reward() const = 0;
    virtual bool is_running() const = 0;
    virtual bool reset() = 0;

};


class CsvRecordedEnvironment: public Environment{
private:
    int datapoint_count;		// Number of rows of data
	int observation_size;		// Number of inputs to neural network
	int reaction_size;	// Number of outputs from neural network
	std::vector< std::vector<Numeric> > observations;		// 2D array of inputs
	std::vector< std::vector<Numeric> > reactions;		// 2D array of targets

    int cycle;
    float last_reward;

	CsvRecordedEnvironment(int datapoint_count, int observation_size, int reaction_size);
    void parse(char *line, int datapoint);
    static int datapoint_count_in_file(FILE *file);

public:
    
    CsvRecordedEnvironment();
    ~CsvRecordedEnvironment();
    static CsvRecordedEnvironment *load_data(const char *path, int observation_size, int reaction_size);
    
    int get_datapoint_count() const;
	int get_observation_size() const;
	int get_reaction_size() const;
    bool is_initialized() const;
    explicit operator bool() const;
    
    const std::vector<Numeric> &get_observation(int datapoint) const;
    const std::vector<Numeric> &get_reaction(int datapoint) const;

    const std::vector<Numeric> &get_observation();
    float send_reaction(const std::vector<Numeric> &reaction);

    int get_cycle() const;
    float get_last_reward() const;
    bool is_running() const;
    bool reset();
    
};


#endif