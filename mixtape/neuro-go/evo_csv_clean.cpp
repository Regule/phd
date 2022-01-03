#include<cstddef>
#include<string>
#include<fstream>
#include<iostream>
#include<algorithm>
#include<sstream>


using std::string;
using std::fstream;
using std::endl;
using std::cout;

class NumericVector: public std::vector<float>{

};

std::ostream &operator<<(std::ostream &os, NumericVector const &num_vec){
	os << num_vec.size();
	for(size_t i=0;  i<num_vec.size(); i++){
		os << ' ' << num_vec[i];
	}	   
    return os;
}

int main(int agrc, char** argv){

}
