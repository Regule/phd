#include <iostream>
#include <fstream>
#include <string>

int main(){
	std::fstream pipe_in;
	pipe_in.open("/tmp/python_to_cpp_pipe", std::ios::in);
	if (pipe_in.is_open()){ 
		std::string tp;
		while(getline(pipe_in, tp)){  
			std::cout << tp << std::endl;
		}
		pipe_in.close();   
	}
}
