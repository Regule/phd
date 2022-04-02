/*!
 * This header defines classes and enumerations that are core for the NEAT 
 * algorithm operations. 
 * */
#include<vector>
#include <memory>


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

/*! Objects of this class represent links between two neural cells. 
 * Each connection have assigned weight and target node, for purposes of evolutionary algorithm it also
 * stores information about its source node however that is not required during normal operation.
 * Connections are identified by their unique genetic marker which indicates their position in network
 * topology. Changing weight do not affect genetic marker.
 *
 * \tparam Numeric Must be a C++ builtin numeric type or a class that implement all of equivalent functionalities.
 */
template<class Numeric> class Link{

private:
	long genetic_marker; /*!< A unique identifier related to position of link in network topology.*/
	Numeric weight; /*!< Weight by which signal will be multiplied when traveling trough link.*/
	std::shared_ptr< Node<Numeric> > target; /*!< Node to which signal travels trough given link.*/
	std::shared_ptr< Node<Numeric> > source; /*!< Node from which this link originates, required only during topology modification.*/

	static long last_genetic_marker; /*!< Last assigned marker, used for generation of new identifiers*/

public:
	Link(Numeric weight, std::shared_ptr< Node<Numeric> > target, std::shared_ptr< Node<Numeric> > source);
	Link(long genetic_marker, Numeric weight, std::shared_ptr< Node<Numeric> > target, std::shared_ptr< Node<Numeric> > source);
	void pass_signal(Numeric signal, long cycle) const;
	void mutate(double factor);
	Numeric get_weight() const;
	std::shared_ptr< Node<Numeric> > get_target() const;
	std::shared_ptr< Node<Numeric> > get_source() const;

	bool operator==(const Link<Numeric> &other); 
	std::string to_string() const;
};


template<class Numeric> class Node{
private:
	long genetic_marker;
	ActivationType activation;
	AgregationType argregation;
	NodeRole role;
	std::vector< std::shared_ptr<Numeric> > outbound;
	std::vector< std::shared_ptr<Numeric> > inbound;
	long cycle;
	Numeric activation_potential;
	Numeric bias;

	static long last_genetic_marker;

public:
	Node(ActivationType activation, AgregationType argregation, NodeRole role, Numeric bias);

	void add_signal(Numeric signal);
	void reset_activation_potential();
	Numeric activate() const;

	void increment_cycle();
	bool is_current_cycle(long current_cyce);
	void reset_cycle();

	void mutate_activation();
	void mutate_agregation();
	void mutate_bias(double factor);

	std::vector< std::shared_ptr<Numeric> > get_outbound_connections() const;
	void connect_outgoing(std::shared_ptr< Link<Numeric> > link);
	void connect_incoming(std::shared_ptr< Link<Numeric> > link);

	bool operator==(const Node<Numeric> &other); 
	std::string to_string() const;


};

