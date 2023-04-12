# Processing of cases as whole for any municipio, given the IBGE code
# years 2000 to 2021, compatibilized in order to know the total time series
# and dividing for different types of imported cases
# the tourists from municipality (IMP_MUN)
# and the tourists from elsewhere (IMP_OTHER)
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


# basic pseudocode 

id_municip = 431490

files = glob.glob('./Data/DataBR_Processed/*.csv')
file = files[12]
# creating the dataframe that will contain the results
data_total = pd.DataFrame()

# reading data 
data_test = pd.read_csv(file, 
                             delimiter = ';',
                             index_col=False,
                             parse_dates = ['DT_SIN_PRI','SEM_PRI','DT_NOTIFIC','SEM_NOT'])
# first column is read differently
data_test = data_test.drop(columns = ['Unnamed: 0'])
# filter data from desidered municipality
filt_df1 = (data_test['ID_MUNICIP'] == id_municip)
data_filtered_1 = data_test[filt_df1]
# filter imported cases by TP_AUTOCTO

# residents in municipality infected elsewhere



# non-residents in municipality infected elsewhere

