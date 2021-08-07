#include<stdlib.h>


typedef double func_double_to_double(double p); // type definition

func_double_to_double *progress_printer;             // pointer to a function of type "give_and_take_double"

void assign_progress_printer_callback(func_double_to_double *function)
{
    // Function called by Python once
    // Defines what "tell_python" is pointing to
    progress_printer = function;
}


void c_python_test_square(int size, double *array_in, double *array_out){
	double percent = 0.2;
	for(int i=0; i<size; i++){
		if ((double)i / size > percent){
			percent = progress_printer(percent);
        }
		array_out[i] = array_in[i]*array_in[i];
	}
}
