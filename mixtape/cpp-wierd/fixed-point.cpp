#include <cstdint>
#include <exception>

//=================================================================================================
//                                           EXCEPTIONS
//=================================================================================================
class OutOfRangeException: public std::exception{
	private:
		double value;
		double lower_limit;
		double upper_limit;

	public:
		OutOfRangeException(double value, double lower_limit, double upper_limit){
			this->value = value;
			this->lower_limit = lower_limit;
			this->upper_limit = upper_limit;
		}

		double get_upper_limit() const{
			return this->upper_limit;
		}

		double get_lower_limit() const{
			return this->lower_limit;
		}

		double get_value() const{
			return this->value;
		}
};

//=================================================================================================
//                                 NUMERIC IMPLEMENTATION 
//=================================================================================================

class Numeric{
private:
	uint32_t data;

	static const uint32_t FLAG_MASK = 2139095040;
	static const uint32_t TYPE_MASK = 2147483648;
	static const size_t VALUE_SIZE = 23;

public:

	Numeric(){
		this->data = 0;
	}

	Numeric(double d){

	}
	
	char get_flag() const{
		uint32_t flag = data | FLAG_MASK;
		flag = flag >> VALUE_SIZE;
		char *flag_bytes = (char*)(&flag);
		return flag_bytes[3];
	}



	static bool is_in_valid_range(double value){
	}
};

int main(){

}
