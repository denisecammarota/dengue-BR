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

def process_municipality(id_municip, sorotipo = False):
    # find all files
    files = glob.glob('./Data/DataBR_Processed/*.csv')
    # creating the dataframe that will contain the results
    data_total = pd.DataFrame()
    if(sorotipo == True):
        data_sorotipo = pd.DataFrame()
    for file in files:
        # find year corresponding to file
        year = int(file[-8:-4])
        if(year >= 2007):
            id_municip_real = id_municip[0:6]
        else:
            id_municip_real = id_municip
        # reading data 
        data_test = pd.read_csv(file, 
                                delimiter = ';',
                                index_col=False,
                                parse_dates = ['DT_SIN_PRI','SEM_PRI','DT_NOTIFIC','SEM_NOT'])
        # first column is read differently
        data_test = data_test.drop(columns = ['Unnamed: 0'])
        # we cast the id_mn_resi to string
        data_test['ID_MN_RESI'] = data_test['ID_MN_RESI'].astype(str)
        # filter data from desidered municipality
        filt_df1 = (data_test['ID_MN_RESI'] == id_municip_real)
        data_filtered_1 = data_test[filt_df1]
        # see if there are available data and sum for week + year
        if(year >= 2007):
            data_filtered_1['WEEK_PRI'] = data_filtered_1['SEM_PRI'].str[0:4]
            data_filtered_1['YEAR_PRI'] = data_filtered_1['SEM_PRI'].str[4:]
        else:
            data_filtered_1['WEEK_PRI'] = data_filtered_1['SEM_PRI'].str[:2]
            data_filtered_1['YEAR_PRI'] = data_filtered_1['SEM_PRI'].str[2:]
        if data_filtered_1.empty == False:
            data_total = data_total.append(data_filtered_1)
            if sorotipo == True and year >= 2007:
                data_filtered_1['CASES'] = 1
                data_filtered_2 = data_filtered_1.groupby(['WEEK_PRI','YEAR_PRI', 'SOROTIPO'])['CASES'].sum()
                data_filtered_2 = data_filtered_2.reset_index(name = 'CASES')
                data_sorotipo = data_sorotipo.append(data_filtered_2)
    # after all years are processed, we put initial week date
    #data_total = process_dates(data_total)
    #regrouping
    data_total['CASES'] = 1
    data_total = data_total.groupby(['WEEK_PRI','YEAR_PRI'])['CASES'].sum()
    data_total = data_total.reset_index(name = 'CASES')
    if(sorotipo == True):
        data_sorotipo = data_sorotipo.groupby(['WEEK_PRI','YEAR_PRI', 'SOROTIPO'])['CASES'].sum()
        data_sorotipo = data_sorotipo.reset_index(name = 'CASES')
    # save in a different path
    path_save = 'Data/'+str(id_municip[0:6])+'/'
    file_save = path_save+str(id_municip[0:6])+'_total_new.csv'
    file_save_sorotipo = path_save+str(id_municip[0:6])+'_total_serotype.csv'
    if(not(os.path.exists(path_save))):
        os.makedirs(path_save)
    data_total.to_csv(file_save, sep=';')
    if(sorotipo == True):
        data_sorotipo.to_csv(file_save_sorotipo, sep=';')