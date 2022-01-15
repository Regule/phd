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

class Observation{
private:
	size_t feature_count;
	float *features;
public:

	Observation(){
		this->feature_count=0;
		this->features=NULL;
	}

	Observation(size_t feature_count, float* features){
		this->feature_count = feature_count;
		this->features = features;
	}

	size_t get_feature_count(){
		return feature_count;
	}

	float get_feature(size_t index){
		if(index<0||index>=feature_count) return 0;
		return features[index];
	}

	const float* get_features(){
		return features;
	}

	string pretty_str(){
		std::stringstream ss;
		for(int i=0;i<feature_count;i++){
			ss<<features[i]<<' ';
		}
		return ss.str();
	}
};

class Dataset{
private:
	string *feature_names;
	size_t feature_count;
	Observation *observations;
	size_t obseration_count;

public:

	Dataset(string *feature_names, size_t feature_count, Observation* observations, 
			size_t obseration_count){
		this->feature_names = feature_names;
		this->observations = observations;
		this->feature_count = feature_count;
		this->obseration_count = obseration_count;
	}

	void pretty_print(){
		for(int i=0; i<feature_count; i++){
			cout<<feature_names[i]<<' ';
		}
		cout<<endl;
		for(int i=0; i<obseration_count; i++){
			cout<<observations[i].pretty_str()<<endl;
		}
	}
	
	static Dataset* read_csv(const char* csv_name, char separator){
		fstream csv_file;
		csv_file.open(csv_name, std::ios::in);
		string line;
		if(!csv_file.is_open()){
			cout<<"Filed to open file "<< csv_name <<endl;
		}
		size_t observation_count=0;
		Observation *observations;
		while(getline(csv_file,line)){
			cout<<line<<endl;
			observation_count++;
		}
		observation_count--;
		cout<<"There are "<<observation_count<<" observations."<<endl;
		observations = new Observation[observation_count];
		csv_file.clear();
		csv_file.seekg(0);
		getline(csv_file,line);
		size_t feature_count = std::count(line.begin(), line.end(), separator)+1;
		cout<<"Tere are "<< feature_count<< " features."<<endl;
		string *feature_names = new string[feature_count];
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
			float* features = new float[feature_count];
			start=0;
			end=0;
			for(size_t feature=0; feature<feature_count; feature++){
				while(end<line.size()&&line[end]!=';')end++;
				string source = line.substr(start,end-start);
				features[feature] = atof(source.c_str());	
				end++;
				start=end;
			}
			observations[i] = Observation(feature_count, features); 
		}
		Dataset *ds = new Dataset(feature_names, feature_count, observations, observation_count);
		return ds;
	}

};

int main(int argc, char**argv){
	Dataset *ds = Dataset::read_csv("./test.csv",';');
	ds->pretty_print();
}
