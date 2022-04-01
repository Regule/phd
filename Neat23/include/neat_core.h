
template<class Numeric> class Link;
template<class Numeric> class Node;


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

enum NodeRole{
	INPUT,
	OUTPUT,
	HIDDEN
};

