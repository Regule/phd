#include "agent.h"

using std::shared_ptr;

Connection::Connection(): GenotypeDependant(){
}

Connection::Connection(Numeric weight): GenotypeDependant(){
	this->weight = weight;
}

Connection::~Connection(){
	if(source) source->disconnect_outgoing(*this);
	if(target) target->disconnect_incoming(*this);
}

Connection::Connection(const Connection& source): GenotypeDependant(source){
	this->weight = source.weight;
}

void Connection::set_target(shared_ptr< Soma<Numeric>> target){
	this->target = target;
}

void Connection::set_source(shared_ptr< Soma<Numeric>> source){
	this->source = source;
}

Numeric Connection::pass_signal(Numeric signal) const{
	return signal*weight;
}



