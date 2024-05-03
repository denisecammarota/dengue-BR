# Processing of cases as whole for any municipio, given the IBGE code
# years 2000 to 2021, compatibilized in order to know the total time series
# doesn't include imported or not imported cases actually
# Code developed by Denise Cammarota

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys 
import glob

# adding path to runtime 
sys.path.insert(1, './fct/')

# importing functions in fct folder
from process_dates import process_dates 
from process_imported import process_imported
from process_municipality import process_municipality

process_municipality(id_municip = '3550308', sorotipo = True) # são paulo
process_municipality(id_municip = '3304557') # rio de janeiro
