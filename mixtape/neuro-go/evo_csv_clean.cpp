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

class NumericVector: public std::vector<float>{
public:
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

int main(int agrc, char** argv){
	NumericVector v(5);
	cout<<v<<endl;
	cout<<"Enter custom vector"<<endl;
	cin>>v;
	cout<<"--------------------------"<<endl;
	cout<<v<<endl;

}
