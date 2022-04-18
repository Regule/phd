/*!
 * In this header all usefull declarations that cannot be assigned to any other
 * more specific location are stored.
 */

#ifndef UTILS_H
#define UTILS_H

#include <random>
#include <memory>

class RandomNumberGenerator{
private:
	std::mt19937 twister;
	std::uniform_real_distribution<double> distribution;
	
	RandomNumberGenerator();
	static std::shared_ptr<RandomNumberGenerator> singleton;

public:

	static std::shared_ptr<RandomNumberGenerator> get_generator();
	double get_value() const;
	int get_from_distribution() const;
};

#endif
