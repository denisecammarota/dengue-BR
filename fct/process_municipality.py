# Processing of cases as whole for any municipio, given the IBGE code
# years 2000 to 2021, compatibilized in order to know the total time series
# includes imported and sum of all cases 
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

def process_municipality(id_municip):
    # find all files
    files = glob.glob('./Data/DataBR_Processed/*.csv')
    # creating the dataframe that will contain the results
    data_total = pd.DataFrame()
    for file in files:
        # find year corresponding to file
        year = int(file[-8:-4])
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
        # see if there are available data and sum for week + year
        if data_filtered_1.empty == False:
            data_filtered_2 = data_filtered_1.groupby(['SIN_WEEK','SIN_YEAR']).size()
            data_filtered_3 = data_filtered_2.to_frame(name = 'CASES').reset_index()
            data_filtered_4 = data_filtered_3.copy()
            data_filtered_4 = process_imported(data_filtered_3, data_filtered_1, year)
            # appending to the final results 
            data_total = data_total.append(data_filtered_4)
    # after all years are processed, we put initial week date
    data_total = process_dates(data_total)
    # save in a different path
    path_save = 'Data/'+str(id_municip)+'/'
    file_save = path_save+str(id_municip)+'total_old.csv'
    if(not(os.path.exists(path_save))):
        os.makedirs(path_save)
    data_total.to_csv(file_save, sep=';')