'''
This script takes train, test and validation csv files then either loads neural network or trains
a new one. If only validation set is given no training occures.
'''


#==================================================================================================
#                                           IMPORTS
#==================================================================================================

import logging
import argparse
import numpy as np
import glob
import json
import time
import os
import sys
