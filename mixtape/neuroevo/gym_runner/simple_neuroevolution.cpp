/*
 * This is an implementation of most simple neuroevolution. In this case a standard 64 bit 
 * floating point implementation with fixed topology will be used. Aim of this code is to test
 * if all interactions between neuroevolution and simulation work correctly before any attempts
 * at implementing experimental solutions.
 */


//=================================================================================================
//                                          IMPORTS 
//=================================================================================================
#include <iostream>
#include <armadillo>
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
using arma::Mat;

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

	Mat<double> get_observation() const{
		std::fstream pipe;
		pipe.open(this->observation_pipe, std::ios::in);
		vector<double> features;
		double feature;
		while(pipe.peek()!= EOF){
			pipe >> feature;
			features.push_back(feature);
		}
		pipe.close();
		return Mat<double>(features.data(), features.size(), 1);
	}

	void send_reaction(const Mat<double> &reaction) const{
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

//=================================================================================================
//                                    NEUROEVOLUTION 
//=================================================================================================
class NeuralNetwork{
	private:
		Mat<double> hidden;
		Mat<double> output;
		double fitness;

	public:

		NeuralNetwork(){
			fitness = 0.0;
		}

		NeuralNetwork(int input_size, int hidden_size, int output_size){
			this->initialize(input_size, hidden_size, output_size);
			fitness = 0.0;
		}

		NeuralNetwork(const Mat<double> &hidden, const Mat<double> &output){
			this->hidden = hidden;
			this->output = output;
			fitness = 0.0;
		}

		NeuralNetwork(const NeuralNetwork &network){
			this->hidden = Mat<double>(network.hidden);
			this-> output = Mat<double>(network.output);
			this->fitness = network.fitness;
		}

		void initialize(int input_size, int hidden_size, int output_size){
			hidden.randu(hidden_size, input_size+1) ;
			output.randu(output_size, hidden_size+1);
		}

		bool operator<(const NeuralNetwork &other) const{
			return this->fitness < other.fitness;
		}

		Mat<double> get_response(const Mat<double> &observations) const{
			try{
				Mat<double> tmp = arma::affmul(hidden,observations);
				tmp = arma::affmul(output, tmp);
				return tmp;
			}catch(std::logic_error error){
				cerr << error.what() << endl;
				cerr << "Hidden=" << hidden.n_rows << "," << hidden.n_cols;
				cerr << " Observation=" << observations.n_rows << "," << observations.n_cols << endl; 
				Mat<double> placeholder;
				placeholder.randu(output.n_cols);
				return placeholder;
			}
		}

		void mutate(double probability, double factor){
			try{
				Mat<double> mutation;
				mutation.randu(hidden.n_rows, hidden.n_cols)*2.0-1.0;
				mutation *= factor;
				hidden += hidden%mutation;
				mutation.randu(output.n_rows, output.n_cols)*2.0-1.0;
				mutation *= factor;
				output += output%mutation;
			}catch(std::logic_error error){
				cerr << "Unable to execute mutation due to an error." << endl;
				cerr << "Error info : " << error.what() << endl;
			}
		}

		NeuralNetwork crossover(const NeuralNetwork &other_network, bool avarage_mode) const{
			Mat<double> hidden = crossover_core(this->hidden, other_network.hidden, avarage_mode);
			Mat<double> output = crossover_core(this->output, other_network.output, avarage_mode);
			return NeuralNetwork(hidden, output);

		}

		void set_fitness(double fitness){
			this->fitness = fitness;
		}

		double get_fitness() const{
			return fitness;
		}

		static Mat<double> crossover_core(const Mat<double> &a, const Mat<double> &b,
			   	bool avarage_mode){	
			try{
				Mat<double> weights_a, weights_b, result;
				weights_a.randu(a.n_rows, a.n_cols);
				weights_b = 1 - weights_a;
				result = (a % weights_a + b % weights_b) / a.n_elem;
				return result;
			}catch(std::logic_error error){
				cerr << "Unable to execute crossover due to error." << endl;
				cerr << "Error info : " << error.what() << endl;
				cerr << "Returning clone on first parent instead" << endl;
				return Mat<double>(a);
			}
		}
};

struct History{
	vector<double> best;
	vector<double> avarage;
	vector<double> worst;

	void to_csv(const char* filename){
		fstream csv_file;
		csv_file.open(filename, std::ios::out);
		if(!csv_file.is_open()){
			cerr<<"Filed to open file "<< filename <<endl;
			return;
		}

		csv_file <<"best;avg;worst"<<endl;
		for(int i=0; i<best.size(); i++){
			csv_file<<best[i]<<";";
			csv_file<<avarage[i]<<";";
			csv_file<<worst[i]<<endl;
		}
		csv_file.close();
	}
};

struct NeuroevolutionResults{
	NeuralNetwork best_agent;
	History history;
};


vector<NeuralNetwork> generate_initial_population(const Config &cfg){
	vector<NeuralNetwork> population(cfg.population_size);
	vector<NeuralNetwork> tmp;
	for(auto specimen: population){
		specimen.initialize(cfg.observation_size, cfg.hidden_size, cfg.reaction_size);
		tmp.push_back(specimen);
	}
	return tmp;
}

vector<NeuralNetwork> run_simulation(const AiGymAPI &gym, vector<NeuralNetwork> &population, int runs_per_agent){
	vector<NeuralNetwork> graded;
	for(auto agent: population){
		double avg_fitness = 0.0;
		for(int run=0; run<runs_per_agent; run++){		
			Mat<double> observation = gym.get_observation();	
			AiGymMetadata metadata = gym.get_metadata();
			double fitness = 0.0;
			while(metadata.running){
				Mat<double> reaction = agent.get_response(observation);
				gym.send_reaction(reaction);
				observation = gym.get_observation();	
				metadata = gym.get_metadata();
				fitness += metadata.reward;
			}
			avg_fitness = (avg_fitness*run + fitness)/(run + 1);
		}
		agent.set_fitness(avg_fitness);
		graded.push_back(NeuralNetwork(agent));
	}
	std::sort(graded.begin(), graded.end());
	return graded;
}

// Elite size is hardcoded to 1 in this example, because of deadlines.
vector<NeuralNetwork> create_new_generation(vector<NeuralNetwork> population, const Config &cfg){
    std::random_device device;
    std::mt19937 generator(device());
    std::uniform_int_distribution<std::mt19937::result_type> random(0, population.size()-1);
	
	vector<NeuralNetwork> new_generation;
	new_generation.push_back(population[0]);
	while(new_generation.size() < population.size()){
		NeuralNetwork parent_a = population[random(generator)];
		NeuralNetwork parent_b = population[random(generator)];
		NeuralNetwork child = parent_a.crossover(parent_b, false);
		child.mutate(cfg.mutation_rate, cfg.mutation_factor);
		new_generation.push_back(NeuralNetwork(child));
	}
	return new_generation;
}

NeuroevolutionResults run_neuroevolution(const Config &cfg, const AiGymAPI &gym){
	vector<NeuralNetwork> population = generate_initial_population(cfg);
	History history;
	for(int generation = 0; generation<cfg.epochs; generation++){
		population = run_simulation(gym, population, cfg.simulations_per_agent);
		history.best.push_back(population[0].get_fitness());
		history.worst.push_back(population[population.size()-1].get_fitness());
		double avarage_fitness=0.0;
		for(auto agent: population){
			avarage_fitness += agent.get_fitness();
		}
		history.avarage.push_back(avarage_fitness/population.size());
		population = create_new_generation(population, cfg);
		cout << "Generation " << generation << " best agent fitness is ";
		cout << population[0].get_fitness() << endl;	
	}
	run_simulation(gym, population, cfg.simulations_per_agent);
	return NeuroevolutionResults{.best_agent=population[0], .history= history};
}



//=================================================================================================
//                                         MAIN 
//=================================================================================================

int main(int argc, char** argv){
	Config config;
	if(!config.parse_args(argc, argv)){
		return 0;
	}
	config.print_config();
	NeuralNetwork net = NeuralNetwork(config.observation_size, config.hidden_size, config.reaction_size);
	AiGymAPI gym(config.observation_pipe, config.reaction_pipe, config.metadata_pipe,
			config.observation_size, config.reaction_size);
	NeuroevolutionResults results = run_neuroevolution(config, gym);
	results.history.to_csv("local/history.csv");
}
