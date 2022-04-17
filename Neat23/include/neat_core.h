/*!
 * This header defines classes and enumerations that are core for the NEAT 
 * algorithm operations. 
 * */

#ifndef NEAT_CORE_H
#define NEAT_CORE_H

#include<vector>
#include "utils.h"



/*! This structure describes mutation that changes vale represented by an enumeration.
 * As such it can only switch between already defined values, for that fied called
 * distribution was added. It provides probability distibution for occurence of each state.
 */
struct EnumeratedMutation{
	double probability_of_occurence; /*!< Probability of mutation occuring */
	std::vector<double> distribution; /*!< Probability distributuion for mutation results */
};


/*! Probabilities of topology changing mutation. Such mutation can add or remove element from
 * network graph.
 */
struct TopologyMutation{
	double deletion_probability; /*!< Probability of adding new element to model */
	double addition_probability; /*!< Probability of removing element*/
};

/*! Data describing a mutation that changes value of a numeric value.
 * Mutation result is calculated according to equation new=old+random(-1;1)*old*factor where 
 * random(-1;1) represents a number chosen randomly with uniform distribution from inclusive range
 * and old and new represent values of changed variable.
 * Setting factor to zero generates value with equation new_bias=random(-1;1) ignoring old value. 
 * All calculations are made with double precision floating point representation however final result is cast
 * to numeric representation specified in class template. This may result in precision loss as well as in 
 * range clamping.
 */
struct NumericMutation{
	double probability_of_occurence; /*!< Probability of mutation occuring. */
	double factor; /*!< Maximum factor by which value can change. */
};


/*! This structure holds all information required for executing mutation step.
 * We distinguish three types of mutations. First is a mutation that changes topology
 * of network. Those are most dramatic mutation as they can add or remove link or node.
 * If node is removed all links assosciated with it will be also removed. 
 * Second type of mutation is change in some enumerated value, in this case it will change
 * to another valid enumeration based on probability distribution.
 * Last type is numeric mutation which changes some numeric value within maximum factor given.
 */
struct MutationConfiguration{
	TopologyMutation node; /*!< Addition or deletion of node */
	TopologyMutation connection; /*!< Addition or deletion of link*/
	EnumeratedMutation activation; /*!< Change of activation function in node*/
	EnumeratedMutation agregation; /*!< Change of agregation function in node*/
	NumericMutation weight; /*!< Change of weight value in connection.*/
	NumericMutation bias; /*!< Change of bias value in node.*/
};

/*! This class is used as a parent for every object that is part of neural network topology.
 * It provides a mechanism for identification of unique placement of objects in network 
 * topology which corresponds with their placement on chromosome.
 * This is required so that crosover operators will be able to compare correct information.
 *
 */
class GenotypeDependant{
protected:
	unsigned long genetic_marker; /*!< The unique genetic marker.*/
	static unsigned long last_genetic_marker; /*!< Base used for generation of markers. */

	/*! A constructor that creates an object with new genetic marker 
	 * */
	GenotypeDependant();

	/*! A constructor that creates an objects with copy of marker from
	 * source object.
	 *
	 * \param source A genotype dependant object which marker will be copied.
	 */
	GenotypeDependant(const GenotypeDependant &source);
public:
	unsigned long get_marker() const;
	bool operator==(const GenotypeDependant &source) const;
};

#endif
