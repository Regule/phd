#include "agent.h"

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

template <class Numeric> Soma<Numeric>::Soma(ActivationType activation, AgregationType agregation, SomaRole role, Numeric bias): GenotypeDependant(){
	this->activation = activation;
	this->agregation = agregation;
	this->role = role;
	this->bias = bias;
	this->reset_state();
}

template <class Numeric> Soma<Numeric>::Soma(const Soma<Numeric> &source): GenotypeDependant(source){
	this->transfer.activation = source.activation;
	this->transfer.agregation = source.agregation;
	this->role = source.role;
	this->transfer.bias = source.bias;
	this->reset_state();
}

template <class Numeric> void Soma<Numeric>::add_signal(Numeric signal){
	switch(this->transfer.activation){
		case SUM:
			this->state.activation_potential += signal;
			break;
		case PRODUCT:
			this->state.activation_potential *= signal;
			break;
		case MIN:
			this->state.activation_potential = minimum(this->state.activation_potential,signal);
			break;
		case MAX:
			this->state.activation_potential = maximum(this->state.activation_potential,signal);
			break;
		default:
			throw CriticallError(__FILE__, __LINE__, "Transfer function is set to incorrect value");
	}
}

template <class Numeric> void Soma<Numeric>::reset_activation_potential(){
	this->state.activation_potential = 0;
	this->state.cycle++;
}

template <class Numeric> Numeric Soma<Numeric>::activate() const{
	// FIXME : FOR TESTS ONLY LINEAR ACTIVATION WORKS
	return this->state.activation_potential - this->transfer.bias; 
}

