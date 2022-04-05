


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
