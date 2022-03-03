#include <iostream>
#include <armadillo>
#include <vector>
#include <exception>

using std::cout;
using std::endl;
using std::cerr;
using std::fstream;
using std::string;
using std::vector;
using std::exception;
using arma::Mat;

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

};

string get_pipe_path(int argc, char** argv){
	if(argc != 2){
		throw ArgumentParsingError();
	}
	return string(argv[1]);
}

Mat<double> read_observation_from_pipe(const char* pipe_file_path){
	fstream input_pipe;
	input_pipe.open(pipe_file_path, std::ios::in);
	string line;
	if(!input_pipe.is_open()){
		throw FileNotFoundException(pipe_file_path);
	}
	Mat<double> mat;
	mat.load(input_pipe, arma::raw_ascii);
	input_pipe.close();
	return mat;
}

Mat<double> read_observation_alternative(const char* pipe_file_path){
	fstream input_pipe;
	input_pipe.open(pipe_file_path, std::ios::in);
    vector<double> features;
	double feature;
	while(input_pipe.peek()!=EOF){
		input_pipe >> feature;
		features.push_back(feature);
	}
	return Mat<double>(features.data(), features.size(), 1);
}

int main(int argc, char** argv){
	try{
		arma::arma_rng::set_seed_random();
		string input_pipe_path = get_pipe_path(argc, argv);
		//Mat<double> observation = read_observation_from_pipe(input_pipe_path.c_str());	
		Mat<double> observation = read_observation_alternative(input_pipe_path.c_str());	
		cout << observation.t() << endl;
	}catch(const FileNotFoundException& e){
		cerr << "Unable to open file "<< e.get_file_name() << endl;
	}catch(const ArgumentParsingError& e){
		cout << "No pipe path given" << endl;
	}

}
