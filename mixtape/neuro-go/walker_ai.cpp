#include<cstddef>
#include<string>
#include<fstream>
#include<iostream>
#include<algorithm>
#include<sstream>
#include<vector>

using std::string;
using std::fstream;
using std::endl;
using std::cout;
using std::cin;
using std::cerr;


//-------------------------------------------------------------------------------------------------
//                                   NUMERICAL VECTOR
//-------------------------------------------------------------------------------------------------

class NumericVector: public std::vector<float>{
public:

	NumericVector() : std::vector<float>(){
	}

	NumericVector(int size) : std::vector<float>(size,0){
	}

	NumericVector(const NumericVector& src) : std::vector<float>(src){
	}	

	friend std::istream &operator>>(std::istream  &input, NumericVector &v) {
		int size;
		input >> size;
		NumericVector tmp(size);
		for(int i=0; i<size; i++){
			input >> tmp[i];
		}
		v=tmp;
		return input;
	}
};

std::ostream &operator<<(std::ostream &os, NumericVector const &num_vec){
	os << num_vec.size();
	for(size_t i=0;  i<num_vec.size(); i++){
		os << ' ' << num_vec[i];
	}	   
    return os;
}

int main(int argc, char**argv){
	NumericVector observation;
	NumericVector reaction(4);
	string s;
	cin>>s;
	cerr<<"Recieved : "<<s<<endl;
	cout<<s<<endl;
	//cin>>observation;
	//cout<<reaction<<endl;
	//cerr<<reaction<<endl;
}
