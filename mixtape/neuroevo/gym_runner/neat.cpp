/*
 * This is a first attempt at implementing NEAT in cpp. It is written with future goals in mind
 * so it uses templates. For this example a double floating point will be used as a numeric value
 * but code should be easily converted to target 23-bit fixed point implementation.
 */

//=================================================================================================
//                                          IMPORTS 
//=================================================================================================
#include <iostream>
#include <fstream>
#include <vector>
#include <exception>
#include <random>
#include <unistd.h>
#include <memory>

using std::cout;
using std::endl;
using std::cerr;
using std::fstream;
using std::string;
using std::vector;
using std::exception;
using std::max;
using std::shared_ptr;


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
struct EnvironmentMetadata{
	int cycle;
	double reward;
	int running;
	int error_code;
	string error_msg;
};

std::ostream & operator << (std::ostream &out, const EnvironmentMetadata &metadata){
	out << "Cycle=" << metadata.cycle << " Reward=" << metadata.reward << " Running=";
	out << (metadata.running?"true":"false") << " Error=" << metadata.error_code;
	out << " Message=" << metadata.error_msg;
	return out;
}


template<class Numeric> class Environment{
	virtual vector<Numeric> get_observation() const = 0;
	virtual void send_reaction(const vector<Numeric> &reaction) const = 0;
	virtual EnvironmentMetadata get_metadata() const = 0;

};



template<class Numeric> class AiGymAPI: public Environment<Numeric>{
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

	vector<Numeric> get_observation() const{
		std::fstream pipe;
		pipe.open(this->observation_pipe, std::ios::in);
		vector<Numeric> features;
		Numeric feature;
		while(pipe.peek()!= EOF){
			pipe >> feature;
			features.push_back(feature);
		}
		pipe.close();
		return features;
	}

	void send_reaction(const vector<Numeric> &reaction) const{
		std::fstream pipe;
		pipe.open(this->reaction_pipe, std::ios::out);
		for(auto feature: reaction){
			Numeric d = reaction[0];
			pipe << d << ' ';
		}
		pipe << endl;
		pipe.close();
	}

	EnvironmentMetadata get_metadata() const{
		std::fstream pipe;
		pipe.open(this->metadata_pipe, std::ios::in);
		EnvironmentMetadata metadata;
		pipe >> metadata.cycle >> metadata.reward >> metadata.running;
		pipe >> metadata.error_code >> metadata.error_msg;
		pipe.close();
		return metadata;
	}

};
//=================================================================================================
//                                              NEAT 
//=================================================================================================

template<class Numeric> class Link;
template<class Numeric> class Node;


enum AgregationType{
	SUM,
	PRODUCT,
	MIN,
	MAX
};

enum ActivationType{
	LINEAR,
	RECTIFIER,
	UNIPOLAR,
	BIPOLAR
};

enum NodeRole{
	INPUT,
	OUTPUT,
	HIDDEN
};

template<class Numeric> class Link{
private:
	long genetic_marker;
	Numeric weight;
	shared_ptr< Node<Numeric> > target;
	shared_ptr< Node<Numeric> > source;

	static long last_genetic_marker;

public:
	Link(Numeric weight, shared_ptr< Node<Numeric> > target, shared_ptr< Node<Numeric> > source);
	void pass_signal(Numeric signal, long cycle) const;
	void mutate(double factor);
	Numeric get_weight() const;
	shared_ptr< Node<Numeric> > get_target() const;
	shared_ptr< Node<Numeric> > get_source() const;

	bool operator==(const Link<Numeric> &other); 
	string to_string() const;
};

template <class Numeric> long Link<Numeric>::last_genetic_marker = 0;

template<class Numeric> class Node{
private:
	long genetic_marker;
	ActivationType activation;
	AgregationType argregation;
	NodeRole role;
	vector< shared_ptr<Numeric> > outbound;
	vector< shared_ptr<Numeric> > inbound;
	long cycle;
	Numeric activation_potential;
	Numeric bias;

	static long last_genetic_marker;

public:
	Node(ActivationType activation, AgregationType argregation, NodeRole role, Numeric bias);

	void add_signal(Numeric signal);
	void reset_activation_potential();
	Numeric activate() const;

	void increment_cycle();
	bool is_current_cycle(long current_cyce);
	void reset_cycle();

	void mutate_activation();
	void mutate_agregation();
	void mutate_bias(double factor);

	vector< shared_ptr<Numeric> > get_outbound_connections() const;
	void connect_outgoing(shared_ptr< Link<Numeric> > link);
	void connect_incoming(shared_ptr< Link<Numeric> > link);

	bool operator==(const Node<Numeric> &other); 
	string to_string() const;


};

template <class Numeric> long Node<Numeric>::last_genetic_marker = 0;

//=================================================================================================
//                                         MAIN 
//=================================================================================================

int main(int argc, char** argv){
	AiGymAPI<double> env("aa","bb", "cc", 12, 12);
	return 0; // For now so that we can test if it compiles
}
