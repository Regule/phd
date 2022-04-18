/*!
 * In this header all usefull declarations that cannot be assigned to any other
 * more specific location are stored.
 */

#ifndef UTILS_H
#define UTILS_H

#include <random>
#include <memory>

#define minimum(a,b) a<b?a:b
#define maximum(a,b) a>b?a:b

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


class CriticallError{
public:
	std::string line;
	std::string file;
	std::string msg;

	CriticallError(const char* file, const char* line, const char* msg);
	std::string get_description() const;
};

#endif
