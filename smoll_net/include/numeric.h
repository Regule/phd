#ifndef NUMERIC_H
#define NUMERIC_H

#include  <cstddef>


#ifndef USE_CUSTOM_NUMERIC
    typedef float Numeric;
#define EPSILON 0.000001
    
#else
class Numeric{
private:
    int32_t data;

public:
    Numeric(float floating_point);
    
    Numeric operator+(const Numeric& other);
    Numeric operator-(const Numeric& other);
    Numeric operator*(const Numeric& other);
    Numeric operator/(const Numeric& other);
    Numeric operator=(const Numeric& other);
    
    
    Numeric operator++();
    Numeric operator--();
    
    bool operator==(const Numeric& other);
    bool operator!=(const Numeric& other);
    bool operator< (const Numeric& other);
    bool operator> (const Numeric& other);
    bool operator<=(const Numeric& other);
    bool operator>=(const Numeric& other);
    
    operator float();
    
};
#endif

#endif
