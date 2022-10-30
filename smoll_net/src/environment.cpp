#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "environment.h"

using std::vector;

CsvRecordedEnvironment::CsvRecordedEnvironment(){
    this->datapoint_count = 0;
    this->observation_size = 0;
    this->reaction_size = 0;
}


CsvRecordedEnvironment::CsvRecordedEnvironment(int datapoint_count, int observation_size, int reaction_size){
	this->datapoint_count = datapoint_count;
    this->observation_size = observation_size;
    this->reaction_size = reaction_size;
    
	this->observations = vector< vector<Numeric> >(datapoint_count);
	this->reactions = vector< vector<Numeric> >(datapoint_count);

	for (int datapoint = 0; datapoint < datapoint_count; datapoint++) {
		this->observations[datapoint] = vector<Numeric>(observation_size);
        this->reactions[datapoint] = vector<Numeric>(reaction_size);
	}
}

void CsvRecordedEnvironment::parse(char *line, int datapoint){
    for (int feature = 0; feature < (this->observation_size + this->reaction_size); feature++) {
        Numeric val = atof(strtok(feature == 0 ? line : NULL, ","));
        if (feature < this->observation_size){
            this->observations[datapoint][feature] = val;
        }else{
            this->reactions[datapoint][feature - this->observation_size] = val;
        }
    }
}

int CsvRecordedEnvironment::datapoint_count_in_file(FILE *file){
    int lines = 0;
	int c = EOF;
	int previous_c = '\n';

	while ((c = getc(file)) != EOF) {
		if (c == '\n')
			lines++;
		previous_c = c;
	}
	if (previous_c != '\n')
		lines++;
	rewind(file);
	return lines;
}
    
CsvRecordedEnvironment *CsvRecordedEnvironment::load_data(const char *path, int observation_size, int reaction_size){
	FILE *file;
	int datapoint_count;

	file = fopen(path, "r");
	if (file == NULL) {
		fprintf(stderr, "ERROR - Could not open %s\n", path);
		return NULL;
	}
	
	datapoint_count = datapoint_count_in_file(file);
	CsvRecordedEnvironment *data = new CsvRecordedEnvironment(datapoint_count, observation_size, reaction_size);

	int datapoint = 0;
    char *line = NULL;
	size_t len = 0;
	while (getline(&line, &len, file) != -1){
		data->parse(line, datapoint);
        datapoint++;
    }
    
	free(line);
	fclose(file);
	return data;
}
 
    
int CsvRecordedEnvironment::get_datapoint_count() const{
    return this->datapoint_count;
}
	
int CsvRecordedEnvironment::get_observation_size() const{
    return this->observation_size;
}
	
int CsvRecordedEnvironment::get_reaction_size() const{
    return this->reaction_size;
}
    
bool CsvRecordedEnvironment::is_initialized() const{
    return true;
}
    
CsvRecordedEnvironment::operator bool() const{
    return this->is_initialized();
}
    
const std::vector<Numeric> &CsvRecordedEnvironment::get_observation(int datapoint) const{
    return this->observations[datapoint];
    
}

const std::vector<Numeric> &CsvRecordedEnvironment::get_reaction ( int datapoint ) const
{
    return this->reactions[datapoint];
}

const std::vector<Numeric> &CsvRecordedEnvironment::get_observation(){
	return this->observations[cycle];
}

float CsvRecordedEnvironment::send_reaction(const std::vector<Numeric> &reaction){
	float sqared_error_punishment = 0.0;
	for(int feature=0; feature<reaction.size(); feature++){
		sqared_error_punishment -= (this->reactions[cycle][feature]-reaction[feature])*(this->reactions[cycle][feature]-reaction[feature]);
	}
	last_reward = sqared_error_punishment; 
	cycle++;
	return sqared_error_punishment;
}

int CsvRecordedEnvironment::get_cycle() const{
	return cycle;
}

float CsvRecordedEnvironment::get_last_reward() const{
	return last_reward;
}

bool CsvRecordedEnvironment::is_running() const{
	return cycle<get_datapoint_count()-1;
}

bool CsvRecordedEnvironment::reset(){
	cycle=0;
	return true;
}


