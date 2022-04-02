/*!
 * This header defines classes and enumerations that are core for the NEAT 
 * algorithm operations. 
 * */

#include<vector>




struct EnvironmentMetadata{
	int cycle;
	double reward;
	int running;
	int error_code;
	std::string error_msg;
};

/*! A interface that represents agent environment.
 * This is an interface that must be used by all classes handling communication 
 * between agents (neural networks) created by NEAT and their environment.
 * Agent gathers an observation from environment, then makes a decision and
 * returns an reaction. Those observations and reactions must be described by
 * a vector corresponding to a data representation in receptors and effectors.
 * This interface additionaly include a metadata information that support 
 * learning process, however not all environment can provide those.
 *
 * \tparam Numeric Must be a C++ builtin numeric type or a class that implement all of equivalent functionalities.
 */
template<class Numeric> class Environment{
	virtual std::vector<Numeric> get_observation() const = 0;
	virtual void send_reaction(const std::vector<Numeric> &reaction) const = 0;
	virtual EnvironmentMetadata get_metadata() const = 0;
	virtual bool provides_learning_metadata() const = 0;

};


/*! This enumeration informs about type of agregation operator of neuron.
 * Agregation takes a vector of input signals and changes it into a scalar 
 * value refered to as activation potential.
 * All input signals are already passed trough links (akson + dendrite) 
 * and as such multiplied by appropriate weights.*/
enum AgregationType{
	SUM, /*!< Signals are summed up.*/
	PRODUCT, /*!< Signals are multipled.*/
	MIN, /*!< Activation potential assumes value of smallest signal.*/
	MAX /*!< Activation potential assumes value of greatest signal.*/
};


/*! This enumeration represents an activation function used by a neuron.
 * Activation function takes neuron activation potential as input, substract
 * bias value form it and then transforms result into a cell response.
 */
enum ActivationType{
	LINEAR, /*!< Neuron returns its activation potential with bias substraced.*/
	RECTIFIER, /*!< If activation potential is positive this acts like a linear function otherwise returns zero.*/
	UNIPOLAR,
	BIPOLAR
};


/*! This enumeration describes role which node plays in the network.
 */
enum NodeRole{
	INPUT, /*!< Input nodes have their responses correspond to observation instead of activation*/
	OUTPUT, /*!< Output nodes are similar hidden ones however they cannot be deleted, network response is taken from them.*/
	HIDDEN /*!< Most common type of node, there is nothing special about it*/
};

template<class Numeric> class Link;
template<class Numeric> class Node;
