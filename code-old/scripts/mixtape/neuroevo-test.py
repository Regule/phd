from ctypes import c_double, c_int, CDLL, CFUNCTYPE, POINTER
import sys
import numpy as np


NEUROEVO_C_LIB_PATH = 'lib/neuroevo-test.so'
neuroevo_lib = CDLL(NEUROEVO_C_LIB_PATH)

# Loading functions from c
test_meschach = neuroevo_lib.test_meschach
test_meschach.restype = None 

test_meschach()
