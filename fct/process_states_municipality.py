# Processing of cases as whole for any state, given the IBGE code
# years 2000 to 2021, compatibilized in order to know the total time series
# includes imported and sum of all cases, separates states
# Code developed by Denise Cammarota

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys 
import glob


# importing functions in fct folder
from process_dates import process_dates 
from process_imported import process_imported
from process_municipality import process_municipality
from find_municipality import find_municipality

def process_state_municipality(id_state):
    # find all files
    files = glob.glob('./Data/DataBR_Processed/*.csv')
    # creating the dataframe that will contain the results
    data_total = pd.DataFrame()
    # if we need municipality, find municipality list
    list_mun = find_municipality(id_state)
    for id_municip in list_mun:
        df_tmp = process_municipality(id_municip)
        df_tmp['ID_MUNICIP'] = id_municip
        data_total.append(df_tmp)
    # save in a different path
    path_save = 'Data/'+str(id_state)+'/'
    file_save = path_save+str(id_state)+'_municipalities.csv'
    if(not(os.path.exists(path_save))):
        os.makedirs(path_save)
    data_total.to_csv(file_save, sep=';')