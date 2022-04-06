/*! This header contains all implementations of numeric variables are used by NEAT model
 * in place of built-in implementations like double or integer.
 */


/*! This is an abstract class that provides all operations required from a numeric variable 
 * by NEAT algorithm. It also guarantees that numeric type can be cast to double and can 
 * be created from it. As for precision and range loss it is assumed to be :W
 *
 */
class Numeric{


	virtual Numeric& operator=(const Numeric& other) = 0;
	virtual Numeric operator+(const Numeric& other) const = 0;
	virtual Numeric operator-(const Numeric& other) const = 0;
	virtual Numeric operator*(const Numeric& other) const = 0;
	virtual Numeric operator/(const Numeric& other) const = 0;
	virtual bool operator==(const Numeric& other) const = 0;
	virtual bool operator< (const Numeric& other) const = 0; 
	operator double() const = 0;

	Numeric& operator+=(const Numeric& other);
	Numeric& operator-=(const Numeric& other);
	Numeric& operator*=(const Numeric& other);
	Numeric& operator/=(const Numeric& other);
	bool operator!=(const Numeric& other) const;
	bool operator> (const Numeric& other) const;
	bool operator<=(const Numeric& other) const;
	bool operator>=(const Numeric& other) const;

};
