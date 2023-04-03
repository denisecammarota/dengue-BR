import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys 
import glob

file =  'Data/DataBR_Processed/dengue_BR_2006.csv'
id_municip = 431490
data_test = pd.read_csv(file, 
                        delimiter = ';',
                        index_col=False,
                        parse_dates = ['DT_SIN_PRI','SEM_PRI','DT_NOTIFIC','SEM_NOT'])
# first column is read differently
data_test = data_test.drop(columns = ['Unnamed: 0'])
# filter data from desidered municipality
filt_df1 = (data_test['ID_MUNICIP'] == id_municip)
data_filtered_1 = data_test[filt_df1]
# see if there are available data and sum for week + year
if data_filtered_1.empty == False:
    data_filtered_2 = data_filtered_1.groupby(['SIN_WEEK','SIN_YEAR']).size()
    data_filtered_3 = data_filtered_2.to_frame(name = 'CASES').reset_index()
    
data_filtered_4 = data_filtered_1.groupby(['SIN_WEEK','SIN_YEAR','TPAUTOCTO'])['TPAUTOCTO'].size()
data_filtered_4 = data_filtered_4.to_frame(name = 'CASES').reset_index()

for key in sorted(data_test.keys()):
    print(key)

