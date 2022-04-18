#ifndef AGENT_H
#define AGENT_H

#include <vector>
#include <memory>
#include "utils.h"
#include "neat_core.h"

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
	UNIPOLAR, /*!< Approximation of unipolar function, it must be implemeted for type used as Numeric in templates*/
	BIPOLAR /*!< Approximation of bipolar function, it must be implemeted for type used as Numeric in templates*/
};


/*! This enumeration describes role which node plays in the network.
 */
enum SomaRole{
	INPUT, /*!< Input nodes have their responses correspond to observation instead of activation*/
	OUTPUT, /*!< Output nodes are similar hidden ones however they cannot be deleted, network response is taken from them.*/
	HIDDEN /*!< Most common type of node, there is nothing special about it*/
};

template<class Numeric> class Connection;
template<class Numeric> class Soma;

/*! Objects of this class represent links between two neural cells. 
 * Each connection have assigned weight and target node, for purposes of evolutionary algorithm it also
 * stores information about its source node however that is not required during normal operation.
 * Connections are identified by their unique genetic marker which indicates their position in network
 * topology. Changing weight do not affect genetic marker.
 *
 * \tparam Numeric Must be a C++ builtin numeric type or a class that implement all of equivalent functionalities.
 */
template<class Numeric> class Connection: public GenotypeDependant{

private:
	Numeric weight; /*!< Weight by which signal will be multiplied when traveling trough link.*/
	std::shared_ptr< Soma<Numeric> > target; /*!< Soma to which signal travels trough given link.*/
	std::shared_ptr< Soma<Numeric> > source; /*!< Soma from which this link originates, required only during topology modification.*/

public:

	/*! This is a constructor used for creating new Connections that do not correspond to any existing topology.
	 * It will automaticly assing a new uniqe genetic marker as well as random weight between -1.0 and 1.0.
	 *
	 * */
	Connection();

	/*! This is a constructor used for creating new Connections that do not correspond to any existing topology.
	 * It will automaticly assing a new uniqe genetic marker.
	 *
	 * \param weight A weight by which signal traveling trough the link will be multiplied.
	 * */
	Connection(Numeric weight);

	/*! This constructor copies other link genetic marker. Actual topological linkage is not copied
	 *  as new link must connect to node eqivalents in its own graph not to the original ones.
	 *
	 * \param source Other link
	 * */
	Connection(const Connection& source);

	/*! A destructor, it will attempt to disconnect this connection from source and target
	 * if those are not null.
	 */
	~Connection();
	
	/*! Attaches link to target node object.
	 *
	 * \param target Target node
	 */
	void set_target(std::shared_ptr< Soma<Numeric>> target);

	/*! Attaches link to source node object.
	 *  Connection to source node is required only during evolution phase.
	 *
	 * \param source Source node
	 */
	void set_source(std::shared_ptr< Soma<Numeric>> source);
	
	/*! This function multiplies given signal by link weight.
	 *
	 * \param signal A signal sent by source node.
	 */
	Numeric pass_signal(Numeric signal) const;

	/*! Mutates link weight in range of given factor. For example if current
	 * weight is 0.8 and factor is 0.5 resulting weight can reach values from range
	 * of 0.5*0.8 to 1.5*0.8.  If factor is set to zero a new random value from between
	 * -1.0 and 1.0 will be generated. Setting factor to zero or value above 1.0 can change
	 *  a node role betwen excitatory and inhibitory.
	 *
	 * \param factor Factor by which weight can be changed. If set to zero new weight is generated.
	 */
	void mutate(double factor);

	/*! Returns connection weight. This should be used for display purposes only, for 
	 * multiplying signal by weight a pass_signal function should be used.
	 *
	 * \return weight stored in connection
	 */
	Numeric get_weight() const;

	/*! Connections can be either excitatory or inhibitory depending on their weight sign.
	 *  If weight is greater than zero then positive signal will result in rise of activation
	 *  potential in target neuron, therfore making such connection excitatory.
	 *  However if weight is less than zero then positive signal will cause a drop of activation
	 *  potential in target neuron and such connection will be called inhibitory.
	 *
	 *  \return True if connection is inhibitory and false if it is excitatory.
	 */
	bool is_inhibitory() const;

	/*!
	 * \return Target node of connection.
	 */
	std::shared_ptr< Soma<Numeric> > get_target() const;

	/*!
	 * \return Source node of connection.
	 */
	std::shared_ptr< Soma<Numeric> > get_source() const;

};

/*! This stucture gathers all elements relative to neural cell transfer function.
 *  All non topological mutations will change one of values contained in this 
 *  structure.
 */
template<class Numeric> struct SomaTransfer{
	ActivationType activation; /*!< Type of activation function used by neuron.*/
	AgregationType argregation; /*!< Type of agregation function used by neuron.*/
	Numeric bias; /*!< Bias by which node dampens activation potential.*/
};

/*! This structure holds information about connections of neural cell. 
 * Mutations that change the topology of network will influence fields of this structure.
 *
 */
template<class Numeric> struct SomaConnections{
public:
	std::vector< std::shared_ptr<Numeric> > outbound; /*!< Connections by which signal leaves node.*/
	std::vector< std::shared_ptr<Numeric> > inbound; /*!< Connections from which signal enters node.*/
};

/*! This structure holds information about current state of neural cell. Operations like signal addition,
 * cell activation or reset will change it state.
 */
template<class Numeric> class SomaState{
	long cycle; /*!< Number of cycle in which this node operates, reseting activation potential increments cycle.*/
	Numeric activation_potential; /*!< Activation potential of node.*/

};

/*! This class represents a neural node, essentialy a cell soma.
 *  It contains information about neuron activation potential as well as its bias.
 *
 *
 * \tparam Numeric Must be a C++ builtin numeric type or a class that implement all of equivalent functionalities.
 */
template<class Numeric> class Soma: public GenotypeDependant{
private:
	SomaRole role; /*!< Role of node, it can be input, output or hidden.*/
	SomaTransfer<Numeric> transfer;
	SomaConnections<Numeric> connections;
	SomaState<Numeric> state;

public:

	/*! This is a constructor used for creating new Somas that do not correspond to any existing topology.
	 * It generates a new unique maker for it.
	 *
	 */
	Soma(ActivationType activation, AgregationType agregation, SomaRole role, Numeric bias);

	/*! This constructor copies other node genetic marker. Actual topological linkage is not copied
	 *  as new node must connect to links eqivalents in its own graph not to the original ones.
	 *
	 * \param source Other node
	 * */
	Soma(const Soma<Numeric> &source);

	/*! This function adds given signal to an activation potential of node. Activation potential is
	 * stored for duration of single cycle. Addition of signal is not nesecarly a arithmetical addition,
	 * it actual implementation depends on node aggregation type.
	 *
	 * \param signal A value of signal that will be agreagated into an activation potential
	 */
	void add_signal(Numeric signal);

	/*! Function resets node activation potential to zero and increments cycle count by one.
	 */
	void reset_activation_potential();

	/*! This function returns response of neural cell. To compute response bias is substracted from
	 * activation potential and resulting value is passed to activation function.
	 * This function do not affect neuron itself so it is not complete equivalent to biological concept
	 * of activation.
	 *
	 * \return Neuron response for stored activation potential
	 */
	Numeric activate() const;

	/*!
	 *
	 * \return True if this node activation potential is set for current cycle
	 */
	bool is_current_cycle(long current_cyce) const;

	/*! Resets cycle back to zero and sets activation potential back to zero.
	 * It should be used only when reseting whole network.
	 */
	void reset_state();

	/*! This method changes activation function randomly. Choice is limited to functions
	 * included in ActivationType enumeration. It is possible to draw current node function
	 * from pool in which case it will remain unchanged.
	 *
	 * \param distribution Probability distribution for activation types, values in this vector must sum up to 1.0
	 */
	void mutate_activation(std::vector<double> distribution);

	/*! This method changes agregation function randomly. Choice is limited to functions
	 * included in AgregationType enumeration. It is possible to draw current node function
	 * from pool in which case it will remain unchanged.
	 *
	 * \param distribution Probability distribution for agregation types, values in this vector must sum up to 1.0
	 */
	void mutate_agregation(std::vector<double> distribution);

	/*! This method changes node bias according to equation new_bias=old_bias+random(-1;1)*old_bias*factor where 
	 * random(-1;1) represents a number chosen randomly with uniform distribution from inclusive range.
	 * Setting factor to zero generates bias with equation new_bias=random(-1;1) ignoring old value of bias.
	 * All calculations are made with double precision floating point representation however final result is cast
	 * to numeric representation specified in class template. This may result in precision loss as well as in 
	 * range clamping.
	 *
	 * \param factor Factor by which bias can be changed, if set to zero new bias in range <-1,1> is generated.
	 * */
	void mutate_bias(double factor);

	/*! Intention of this method is to provide access to copy of outbound links vector so that signal propagation
	 * can be implemented outside of node class. This will allow greater control and easier debuging.
	 *
	 * \return Copy of vector of node outbound links
	 */
	std::vector< std::shared_ptr< Connection<Numeric> > > get_outbound_connections() const;

	/*! Adds a outgoing connection, this function is used for building a network topology.
	 *
	 * \param connection An outgoing connection
	 */
	void connect_outgoing(std::shared_ptr< Connection<Numeric> > connection);
	void disconnect_outgoing(const Connection<Numeric> &connection);

	/*! Adds an information about inboud connection to node. Information about those connections is 
	 * recuired only during evolution phase as removal of node must also remove all connections that 
	 * lead to it.
	 *
	 * \param connection An incoming connection
	 */
	void connect_incoming(std::shared_ptr< Connection<Numeric> > connection);
	void disconnect_incoming(const Connection<Numeric> &connection);

	/*!
	 *\return True if both nodes have same genetic marker and therfore same place in network topology.
	 */
	bool operator==(const Soma<Numeric> &other); 

};

template<class Numeric> struct NeuralNetwork{
	unsigned long cycle; /*!< Number of current cycle in agent operation, activating agent increments cycle. */
	std::vector< std::shared_ptr< Soma<Numeric> > > sensoric; /*!< Vector of neurons which values are set according to observation. */
	std::vector< std::shared_ptr< Soma<Numeric> > > interneurons; /*!< Vector of internal neurons that do not interact directly with neither observation nor reaction. */
	std::vector< std::shared_ptr< Soma<Numeric> > > motoric; /*!< Vector of neurons which values will be treated as agent reaction. */
};

struct EvolutionMetadata{
	unsigned long species_id; /*!< Unique spieces identifier. Agents with same spieces identifier have same topology. */
	unsigned long parent_spieces; /*!< Identifier of spieces from which this one originated or zero if it was generated from scratch. */
	double fitness; /*!< Total fitness value gathered through agent operation. Can be reset alongside with cycle number. */
};

/*! This class represents a single neural network based agent. It recives an observation
 * that sets value on it sensoric neurons. After that network is activated and signal travels
 * trough interneurons to finally reach motoric neurons. Values from those motoric neurons are
 * then treated as agent response also reffered to as reaction.
 * Agent interactions with environment are described as a discrete process in which for every step
 * in time, called cycle, agent recieves observation from environment and returns reaction to it.
 * This class also implements functionality required for agent to participate in evalutionary process,
 * those elements are not required for agent basic functionality and may be ignored if already pretrained
 * agent is used.
 *
 * \tparam Numeric Must be a C++ builtin numeric type or a class that implement all of equivalent functionalities.
 */
template<class Numeric> class NeuralAgent{
private:
	NeuralNetwork<Numeric> net;
	EvolutionMetadata genetics;

	/*! This is constructor that creates a network from list of interconnected neural cells (Soma objects).
	 * Its visibility is set to private as manual creation of topologies is not permitet as it could potentialy impair 
	 * genetic marker identifier system used in this library. Instead network models should be either generated randomly by 
	 * dedicated method, created as a copies of existing networks and then mutated or read from file.
	 *
	 * \param sensoric  Vector of neurons which values are set according to observation. 
	 * \param interneurons  Vector of internal neurons that do not interact directly with neither observation nor reaction. 
	 * \param motoric  Vector of neurons which values will be treated as agent reaction.
	 */
	NeuralAgent(std::vector< std::shared_ptr< Soma<Numeric> > > sensoric,std::vector< std::shared_ptr< Soma<Numeric> > > interneurons, std::vector< std::shared_ptr< Soma<Numeric> > > motoric);

public:

	/*! Copy constuctor.
	 * It copies not only topology but also all other values from original. It creates a deep copy so all objects 
	 * conneted by pointers will be also copied instead of using same reference.
	 *
	 * \parameter agent Agent that will be copied.
	 */ 
	NeuralAgent(const NeuralAgent &agent);

	/*! This is main function of neural agent used for interaction with environment.
	 * Calling it will add values from observation vector into soma of sensoric neurons and 
	 * then propagate signals trought network. After that values from motoric neurons will be
	 * returned as a reaction vector. Another thing that will happen is incrementation of cycle
	 * count by one.
	 *
	 * \param observation A numeric vector representing agent observation of environment.
	 * \return A reaction vector that should be used for influencing environment.
	 */
	std::vector<Numeric> activate(const std::vector<Numeric> &observation);

	/*! Resets neural network that control agent behaviour. Reseting include zeroing activation potential
	 * in all neurons as well as setting cycle number and fitness back to zero.
	 */ 
	void reset();

	/*! This function adds a single reward to fitness of agent.  This way of calculating fitness means that genetic
	 * algorithm target is maximalisation of fitness function. Reward can be a negative value, in such case it
	 * will be described as a punishment.
	 *
	 * \param reward A reward recieved by action resulting from last reaction of agent.
	 */
	void add_reward(double reward);

	/*! This is part of genetic algorithm that creates a new offspring that copies values from both parents.
	 *  It is possible to 
	 */
	std::vector< std::shared_ptr< NeuralAgent<Numeric> > > crossover(std::shared_ptr< NeuralAgent<Numeric> > other, int litter_size) const;
	void mutate(const MutationConfiguration &config, bool allow_speciation);
	static std::shared_ptr< NeuralAgent<Numeric> > generate_new_spieces(size_t observation_size, size_t reaction_size, size_t interlayer_size);
};

#endif
