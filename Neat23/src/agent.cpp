#include "agent.h"
#include "utils.h"

using std::shared_ptr;

template <class Numeric> Connection<Numeric>::Connection(): GenotypeDependant(){
}

template <class Numeric> Connection<Numeric>::Connection(Numeric weight): GenotypeDependant(){
	this->weight = weight;
}

template <class Numeric> Connection<Numeric>::~Connection(){
	if(source) source->disconnect_outgoing(*this);
	if(target) target->disconnect_incoming(*this);
}

template <class Numeric> Connection<Numeric>::Connection(const Connection& source): GenotypeDependant(source){
	this->weight = source.weight;
}

template <class Numeric> void Connection<Numeric>::set_target(shared_ptr< Soma<Numeric>> target){
	this->target = target;
}

template <class Numeric> void Connection<Numeric>::set_source(shared_ptr< Soma<Numeric>> source){
	this->source = source;
}

template <class Numeric> Numeric Connection<Numeric>::pass_signal(Numeric signal) const{
	return signal*weight;
}

template <class Numeric> void Connection<Numeric>::mutate(double factor){
	double random = RandomNumberGenerator::get_generator()->get_value();
	this->weight += this->weight*factor*random;
}

template <class Numeric> Numeric Connection<Numeric>::get_weight() const{
	return this->weight;
}

template <class Numeric> bool Connection<Numeric>::is_inhibitory() const{
	return this->weight < 0;
}
