#include<stdlib.h>

void c_python_test_square(int size, double *array_in, double *array_out){
	for(int i=0; i<size; i++){
		array_out[i] = array_in[i]*array_in[i];
	}
}
