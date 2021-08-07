from ctypes import c_double, c_int, CDLL, CFUNCTYPE, POINTER
import sys
import numpy as np

lib_path = 'lib/c_python_test.so'
basic_function_lib = CDLL(lib_path)

python_c_square = basic_function_lib.c_python_test_square
python_c_square.restype = None # Because it returns None (void)


def get_percent(percent):
    """Print advancement and set the next call when C has advanced a further 20%"""
    print(f'Advancement of C calculations: {percent*100}')
    return percent + 0.2

CB_FTYPE_DOUBLE_DOUBLE = CFUNCTYPE(c_double, c_double) # define C pointer to a function type
cb_get_percent = CB_FTYPE_DOUBLE_DOUBLE(get_percent) # define a C function equivalent to the python function "get_percent"
basic_function_lib.assign_progress_printer_callback(cb_get_percent)  # the the C code about that C function


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
