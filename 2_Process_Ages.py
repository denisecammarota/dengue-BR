# Processing of cases as whole for any municipio, given the IBGE code
# years 2000 to 2021, compatibilized in order to know the total time series
# include the profile of age of cases
# Code developed by Denise Cammarota

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys 
import glob

# adding path to runtime 
sys.path.insert(1, './fct/')

# creating the dataframe that will contain the results
# using a tmp file to do the code, since i don't have the full data here on this pc
file = './Data/dengue_BR_2013.csv'
data_total = pd.DataFrame()

# municipality
id_municip = 431490

# getting the correct year
year = int(file[-8:-4])
# loading the file 
data_test = pd.read_csv(file, 
                            delimiter = ';',
                            index_col=False,
                            parse_dates = ['DT_SIN_PRI','SEM_PRI','DT_NOTIFIC','SEM_NOT'])
# first column is read differently
data_test = data_test.drop(columns = ['Unnamed: 0'])
# filter data from desidered municipality
filt_df1 = (data_test['ID_MUNICIP'] == id_municip)
data_filtered_1 = data_test[filt_df1]
data_filtered_1

data_filtered_1['NU_IDADE_N']

if data_filtered_1.empty == False:
    data_filtered_2 = data_filtered_1.groupby(['SIN_WEEK','SIN_YEAR']).size()
    data_filtered_3 = data_filtered_2.to_frame(name = 'CASES').reset_index()
    data_filtered_4 = data_filtered_3.copy()
    