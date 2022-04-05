#include "numeric_types.h"


Numeric& Numeric::operator+=(const Numeric& other){
	*this = *this + other;
	return this;
}

Numeric& Numeric::operator-=(const Numeric& other){
	*this = *this - other;
	return this;
}

Numeric& Numeric::operator*=(const Numeric& other){
	*this = *this * other;
	return this;
}

Numeric& Numeric::operator/=(const Numeric& other){
	*this = *this / other;
	return this;
}

bool Numeric::operator!=(const Numeric& other)const {
	return !(*this == other); 
}	

bool Numeric::operator> (const Numeric& other)const {
	return other < *this; 
}

bool Numeric::operator<=(const Numeric& other)const {
	return !(*this > other); 
}

bool Numeric::operator>=(const Numeric& other)const {
	return !(*this < other);
}
