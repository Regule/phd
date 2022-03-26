/*
 * This is a first attempt at implementing NEAT in cpp. It is written with future goals in mind
 * so it uses templates. For this example a double floating point will be used as a numeric value
 * but code should be easily converted to target 23-bit fixed point implementation.
 */

//=================================================================================================
//                                          IMPORTS 
//=================================================================================================
#include <iostream>
#include <vector>
#include <exception>
#include <random>

using std::cout;
using std::endl;
using std::cerr;
using std::fstream;
using std::string;
using std::vector;
using std::exception;
using std::max;

//=================================================================================================
//                                      UTILITIES 
//=================================================================================================

class Config{
public:
	string observation_pipe;
	string reaction_pipe;
	string metadata_pipe;
	int observation_size;
	int reaction_size;
	int hidden_size;
	double mutation_rate;
	double mutation_factor;
	int population_size;
	int simulations_per_agent;
	int epochs;

	Config(){
		this->observation_pipe = "/tmp/observation_pipe";
		this->reaction_pipe = "/tmp/reaction_pipe";
		this->metadata_pipe = "/tmp/metadata_pipe";
		this->observation_size = 24;
		this->reaction_size = 4;
		this->hidden_size = 20;
		this->mutation_rate = 0.2;
		this->mutation_factor = 0.4;
		this->population_size = 100;
		this->simulations_per_agent = 5;
		this->epochs = 10;
	}

	bool parse_args(int argc, char **argv){
		int argument_char;
		while ((argument_char = getopt (argc, argv, "o:r:m:O:R:S:M:F:P:A:E:hH")) != -1){
			switch(argument_char){
				case 'o':
					this->observation_pipe= string(optarg);
					break;
				case 'r':
					this->reaction_pipe = string(optarg);
					break;
				case 'm':
					this->metadata_pipe = string(optarg);
					break;
				case 'O':
					this->observation_size = atoi(optarg);
					break;
				case 'R':
					this->reaction_size = atoi(optarg);
					break;
				case 'S':
					this->hidden_size = atoi(optarg);
					break;
				case 'E':
					this->epochs = atoi(optarg);
					break;
				case 'M':
					this->mutation_rate = atof(optarg);
					break;
				case 'F':
					this->mutation_factor = atof(optarg);
					break;
				case 'P':
					this->population_size = atoi(optarg);
					break;
				case 'A':
					this->simulations_per_agent = atoi(optarg);
					break;
				case 'H':
				case 'h':
					print_help();
					return false;
				default:
					cerr << "Unknown argument - " << static_cast<char>(argument_char) << endl;
					return false;
			}
		}
		return true;
	}

	void print_config() const{
		for(int i=0; i<100; i++){
			cout<<'-';
		}
		cout<<endl;
		cout<<"CONFIGURATION :"<<endl;
		cout<<"Observation pipe = "<<this->observation_pipe<<endl;
		cout<<"Reaction pipe  = "<<this->reaction_pipe<<endl;
		cout<<"Metada pipe  = "<<this->metadata_pipe<<endl;
		cout<<"Observation size = "<<this->observation_size<<endl;
		cout<<"Reaction size = "<<this->reaction_size<<endl;
		cout<<"Hidden size = "<<this->hidden_size<<endl;
		cout<<"Mutation rate = "<<this->mutation_rate<<endl;
		cout<<"Mutation factor = "<<this->mutation_factor<<endl;
		for(int i=0; i<100; i++){
			cout<<'-';
		}
		cout << endl;	
	}

	void print_help(){
		cout << "This program executes neuroevolution algorithm and is prepared to work";
		cout << " with specific Open Ai gym wrapper" << endl;
	}
	
};

//=================================================================================================
//                                     EXCEPTIONS 
//=================================================================================================
class FileNotFoundException: public std::exception{
	private:
		string file_name;

	public:
		FileNotFoundException(const char* file_name){
			this->file_name = string(file_name);
		}

		string get_file_name() const{
			return this->file_name;
		}
};

class ArgumentParsingError: public std::exception{
	private:
		char argument;

	public:
		ArgumentParsingError(const char argument){
			this->argument = argument;
		}

		char get_argument_identifier() const{
			return this->argument;
		}
};

//=================================================================================================
//                                      AI GYM API 
//=================================================================================================
struct AiGymMetadata{
	int cycle;
	float reward;
	int running;
	int error_code;
	string error_msg;
};

std::ostream & operator << (std::ostream &out, const AiGymMetadata &metadata){
	out << "Cycle=" << metadata.cycle << " Reward=" << metadata.reward << " Running=";
	out << (metadata.running?"true":"false") << " Error=" << metadata.error_code;
	out << " Message=" << metadata.error_msg;
	return out;
}


class AiGymAPI{
private:
	string observation_pipe;
	string reaction_pipe;
	string metadata_pipe;
	int observation_size;
	int reaction_size;

public:
	AiGymAPI(const string& observation_pipe, const string& reaction_pipe,
		   	const string& metadata_pipe, int observation_size, int reaction_size){
		this->observation_pipe = observation_pipe;
		this->reaction_pipe = reaction_pipe;
		this->metadata_pipe = metadata_pipe;
		this->observation_size = observation_size;
		this->reaction_size = reaction_size;
	}

	vector<double> get_observation() const{
		std::fstream pipe;
		pipe.open(this->observation_pipe, std::ios::in);
		vector<double> features;
		double feature;
		while(pipe.peek()!= EOF){
			pipe >> feature;
			features.push_back(feature);
		}
		pipe.close();
		return features;
	}

	void send_reaction(const vector<double> &reaction) const{
		std::fstream pipe;
		pipe.open(this->reaction_pipe, std::ios::out);
		for(auto feature: reaction){
			double d = reaction[0];
			pipe << d << ' ';
		}
		pipe << endl;
		pipe.close();
	}

	AiGymMetadata get_metadata() const{
		std::fstream pipe;
		pipe.open(this->metadata_pipe, std::ios::in);
		AiGymMetadata metadata;
		pipe >> metadata.cycle >> metadata.reward >> metadata.running;
		pipe >> metadata.error_code >> metadata.error_msg;
		pipe.close();
		return metadata;
	}

};

