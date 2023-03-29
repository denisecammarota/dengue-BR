# Processing of cases as whole for any files after initial clean 
# years 2000 to 2021, compatibilized in order to know the total time series
# doesn't include imported or not imported cases actually
# Code developed by Denise Cammarota


import numpy as np
import pandas as pd
import sys 
import os

def process_dates():
    print('hello world')


path_file = 'Data/431490/'
file = 'Data/431490/431490_total.csv'
df =  pd.read_csv(file, 
                  delimiter = ';',
                  index_col=False,
                  parse_dates = ['DT_SIN_PRI','SEM_PRI','DT_NOTIFIC','SEM_NOT'])
