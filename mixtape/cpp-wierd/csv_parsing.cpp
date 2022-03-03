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

	Dataset(std::vector<string> feature_names, std::vector<NumericVector> observations):
		std::vector<NumericVector>(observations){
		this->feature_names = feature_names;
	}

	int get_feature_count() const{
		return feature_names.size();
	}

	string get_feature_name(int i) const{
		return feature_names[i];
	}

	static Dataset* read_csv(const char* csv_name, char separator){
		fstream csv_file;
		csv_file.open(csv_name, std::ios::in);
		string line;
		if(!csv_file.is_open()){
			cout<<"Filed to open file "<< csv_name <<endl;
		}
		int observation_count=0;
		while(getline(csv_file,line)){
			observation_count++;
		}
		observation_count--;
		cout<<"There are "<<observation_count<<" observations."<<endl;
		std::vector<NumericVector> observations = std::vector<NumericVector>(observation_count);
		csv_file.clear();
		csv_file.seekg(0);
		getline(csv_file,line);
		int feature_count = std::count(line.begin(), line.end(), separator)+1;
		cout<<"Tere are "<< feature_count<< " features."<<endl;
		std::vector<string> feature_names = std::vector<string>(feature_count);
		size_t start=0;
		size_t end=0;
		for(size_t feature=0; feature<feature_count; feature++){
			while(end<line.size()&&line[end]!=';')end++;
			feature_names[feature] = line.substr(start,end-start);
			end++;
			start=end;
		}
		for(size_t i=0; i<observation_count; i++){
			if(!getline(csv_file,line)) break;
			NumericVector features = NumericVector(feature_count);
			start=0;
			end=0;
			for(size_t feature=0; feature<feature_count; feature++){
				while(end<line.size()&&line[end]!=';')end++;
				string source = line.substr(start,end-start);
				features[feature] = atof(source.c_str());	
				end++;
				start=end;
			}
			observations[i] = features; 
		}
		Dataset *ds = new Dataset(feature_names, observations);
		return ds;
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
	Dataset *data = Dataset::read_csv("./test.csv",';');
	cout<<*data;
}
