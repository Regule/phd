#include "neat_core.h"
	

unsigned long GenotypeDependant::last_genetic_marker = 0;


GenotypeDependant::GenotypeDependant(){
	this->genetic_marker = last_genetic_marker++; 
}

GenotypeDependant::GenotypeDependant(const GenotypeDependant &source){
	this->genetic_marker = source.genetic_marker;
}

unsigned long GenotypeDependant::get_marker() const{
	return this->genetic_marker;
}

bool GenotypeDependant::operator==(const GenotypeDependant &source) const{
	return this->genetic_marker == source.genetic_marker;
}
