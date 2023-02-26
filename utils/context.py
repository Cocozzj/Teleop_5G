import os
from os import path
import sys

PROJ_DIR = path.abspath(os.path.dirname(path.dirname(__file__)))
DATA_DIR = path.join(PROJ_DIR, 'raw-data')
DATA_PROCESS_DIR = path.join(PROJ_DIR, 'process-data')
PLOT_DIR = path.join(PROJ_DIR, 'plots')
UTILS_DIR = path.join(PROJ_DIR, 'utils')
sys.path.append(PROJ_DIR)