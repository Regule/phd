/*! This header contains interfaces enums and structures that must be used by any
 * class that interfaces neural agents with environment.
 * There are no specific implementations here.
 */
#include<vector>



/*! This structure holds metadata returned by API responsible for interaction
 * between agent and environment. 
 *
 * @see Environment Interface implemented by API that returns this metadata. 
 */
struct EnvironmentMetadata{

	/*! This enumeration holds error codes that can be returned by environment endpoint. 
	* */
	enum ErrorCode{
		ENV_ERR_OK = 0, /*!< No error occured.*/
		ENV_ERR_UNKNOWN = 1 /*!< There is no specific code for error.*/
	};

	/*! Number of observation since initialization of simulation or sensor-receptor system.*/
	int cycle;
	/*! Reward related to current observation, required by learning algorithms.*/
	double reward;
	/*! Set to 1 if environment interaction endpoint is active otherwise 0.*/
	int running;
	/*! Error codes*/
	ErrorCode error_code;
	/*! An human readable description of error for logging purposes.*/
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

	/*! Function returns an observation from environment. 
	 * \return A numeric vector representing observation.
	 * */
	virtual std::vector<Numeric> get_observation() const = 0;

	/*! Function sends a reaction to environment endpoint.
	 * Reaction do not directly transform environment but influences how
	 * efectors interact with it.
	 *
	 * \param reaction A numeric vector that encodes efectors behavior.
	 */
	virtual void send_reaction(const std::vector<Numeric> &reaction) const = 0;

	/*! Returns additional metadata from environent API that is not a part of 
	 * normal observation but informs about endpoint itself.
	 *
	 * \return Metadata of environment endpoint.
	 */
	virtual EnvironmentMetadata get_metadata() const = 0;

	/*! Not every environment API provides infromation reqired for agent learning.
	 *  This function allows for checking if cycle number and reward returned in
	 *  metadata contain a actual information. 
	 *
	 *  \return True if learning related metadata contains usefull information, otherwise False.
	 */
	virtual bool provides_learning_metadata() const = 0;

};
