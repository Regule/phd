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

//-------------------------------------------------------------------------------------------------
//                                      DATA SET 
//-------------------------------------------------------------------------------------------------
class Dataset : public std::vector<NumericVector>{
private:
	std::vector<string> feature_names;

public:
	Dataset(int observation_count, int feature_count) : std::vector<NumericVector>(observation_count){
		feature_names = std::vector<string>(feature_count, "UNKNOWN");
		for(int i=0; i<this->size(); i++){
			this->at(i) = NumericVector(feature_count);
		}
	}

	Dataset(const Dataset& src) : std::vector<NumericVector>(src){
		feature_names = src.feature_names;
	}

	int get_feature_count() const{
		return feature_names.size();
	}

	string get_feature_name(int i) const{
		return feature_names[i];
	}
};

std::ostream &operator<<(std::ostream &os, Dataset const &dataset){
	os << dataset.size() << ' ' << dataset.get_feature_count() << endl;	
	for(int i=0; i<dataset.get_feature_count(); i++){
		os << dataset.get_feature_name(i) << ' ';
	}
	os << endl;
	for(size_t i=0;  i<dataset.size(); i++){
		os << dataset[i] << endl;
	}	   
    return os;
}

//-------------------------------------------------------------------------------------------------
//                                  MAIN FUNCTION 
//-------------------------------------------------------------------------------------------------

int main(int agrc, char** argv){
	NumericVector v(5);
	cout<<v<<endl;
	cout<<"Enter custom vector"<<endl;
	cin>>v;
	cout<<"--------------------------"<<endl;
	cout<<v<<endl;
	cout<<"--------------------------"<<endl;
	Dataset ds(10,4);
	cout<<ds;
}
