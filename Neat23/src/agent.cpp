#include "agent.h"

using std::shared_ptr;

Connection::Connection(): GenotypeDependant(){
}

Connection::Connection(Numeric weight): GenotypeDependant(){
	this->weight = weight;
}

Connection::Connection(const Connection& source): GenotypeDependant(source){
	this->weight = source.weight;
}

void Connection::set_target(shared_ptr< Soma<Numeric>> target){
	this->target = target;
}
