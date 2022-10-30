#include "numeric.h"

#ifdef USE_CUSTOM_NUMERIC

Numeric::Numeric(float floating_point){
    
}
    
Numeric Numeric::operator+(const Numeric& other){}
Numeric Numeric::operator-(const Numeric& other){}
Numeric Numeric::operator*(const Numeric& other){}
Numeric Numeric::operator/(const Numeric& other){}
Numeric Numeric::operator=(const Numeric& other){}
    
    
Numeric Numeric::operator++(){}
Numeric Numeric::operator--(){}
    
bool Numeric::operator==(const Numeric& other){}
bool Numeric::operator!=(const Numeric& other){}
bool Numeric::operator< (const Numeric& other){}
bool Numeric::operator> (const Numeric& other){}
bool Numeric::operator<=(const Numeric& other){}
bool Numeric::operator>=(const Numeric& other){}
    
operator Numeric::float(){}
    
#endif

