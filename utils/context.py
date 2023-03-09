import os
from os import path
import sys

PROJ_DIR = path.abspath(os.path.dirname(path.dirname(__file__)))
DATA_DIR = path.join(PROJ_DIR, 'raw-data')
RESULT_DIR = path.join(PROJ_DIR, 'Result')
TASK1_DIR = path.join(RESULT_DIR, 'task1')
TASK2_DIR = path.join(RESULT_DIR, 'task2')
TASK3_DIR = path.join(RESULT_DIR, 'task3')
UTILS_DIR = path.join(PROJ_DIR, 'utils')

sys.path.append(PROJ_DIR)