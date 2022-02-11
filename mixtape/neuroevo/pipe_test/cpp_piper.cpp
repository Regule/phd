#include <iostream>
#include <fstream>
#include <string>

int main(){
	std::fstream pipe_in, pipe_out;
	pipe_in.open("/tmp/python_to_cpp_pipe", std::ios::in);
	if (pipe_in.is_open()){ 
		std::string tp;
		getline(pipe_in, tp); 
		std::cout << tp << std::endl;
	}
	pipe_in.close();
	pipe_out.open("/tmp/cpp_to_python_pipe", std::ios::out);
	if(pipe_out.is_open()){
		pipe_out << "This is from cpp" << std::endl;
	}
	pipe_out.close();
}
