# Finding municipalities affected by dengue for a state given its
# based on the IBGE code, if necessary
# Code developed by Denise Cammarota


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys 
import glob


def find_municipality(id_state):
    # find all files
    files = glob.glob('./Data/DataBR_Processed/*.csv')
    # creating final municipalities list
    list_mun = []
    for file in files:
        # reading data 
        data_test = pd.read_csv(file, 
                                delimiter = ';',
                                index_col=False,
                                parse_dates = ['DT_SIN_PRI','SEM_PRI','DT_NOTIFIC','SEM_NOT'])
        # first column is read differently
        data_test = data_test.drop(columns = ['Unnamed: 0'])
        # filter data from desidered state
        filt_df1 = (data_test['SG_UF_NOT'] == id_state)
        data_filtered_1 = data_test[filt_df1]
        # finding and processing municipalities 
        # unique municipality values for this year that had dengue
        list_mun.extend(list(data_filtered_1['ID_MUNICIP'].unique()))
    # filter list for unique elements
    list_mun = list(set(list_mun))
    # filter municipalities not in this state, that is, errors
    list_mun = [str(x) for x in list_mun]
    list_mun = [x for x in list_mun if x.startswith(str(id_state))]
    list_mun = [int(x) for x in list_mun]
    return list_mun 