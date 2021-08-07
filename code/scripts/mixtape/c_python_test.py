from ctypes import c_double, c_int, CDLL
import sys
import numpy as np

lib_path = 'lib/c_python_test.so'
basic_function_lib = CDLL(lib_path)

python_c_square = basic_function_lib.c_python_test_square
python_c_square.restype = None # Because it returns None (void)

def do_square_using_c(list_in):
    """Call C function to calculate squares"""
    n = len(list_in)
    c_arr_in = (c_double * n)(*list_in)
    c_arr_out = (c_double * n)()

    python_c_square(c_int(n), c_arr_in, c_arr_out)
    return c_arr_out[:] # Indexing with : is basically cast to python list

my_list = np.arange(13)
squared_list = do_square_using_c(my_list)
print(squared_list)
