#include <cstdint>

//=================================================================================================
//                                           EXCEPTIONS
//=================================================================================================
class OutOfRangeException: public std::exception{
	private:
		double value;
		double lower_limit;
		double upper_limit;

	public:
		FileNotFoundException(double value, double lower_limit, double upper_limit){
			this->value = value;
			this->lower_limit = lower_limit;
			this->upper_limit = upper_limit;
		}

		double get_upper_limit() conts{
			return this->upper_limit;
		}

		double get_lower_limit() conts{
			return this->lower_limit;
		}

		double get_value() conts{
			return this->value;
		}
};

//=================================================================================================
//                                 NUMERIC IMPLEMENTATION 
//=================================================================================================

class Numeric{
private:
	uint32_t data;

public:
	Numeric(){
		this->data = 0;
	}

	Numeric(double d){

	}
	
	char get_flag() const{
	}

	static is_in_valid_range(double value){
	}
};

int main(){

}
