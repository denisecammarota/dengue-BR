# Serotype ocurrence as whole for all states for each year, separated by state
# and also by each municipality in each state 
# years 2007 to 2021, sorotipo available for all these times
# Code developed by Denise Cammarota

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys 
import glob

def serotype_states():
    # state and uf code from ibge for each state
    names_path = 'Data/estados.csv'
    state_names = pd.read_csv(names_path, index_col = False)
    state_names = state_names[['codigo_uf', 'uf']]
    dict_states = state_names.set_index('codigo_uf').T.to_dict('records')[0]
    # years we use for analysis
    years = np.arange(2007,2022,1)
    data_total = pd.DataFrame()
    # processing for each state and each year
    for year in years:
        file_path = 'Data/DataBR_Processed/dengue_BR_'+str(year)+'.csv'
        
        data_test = pd.read_csv(file_path, 
                                delimiter = ';',
                                index_col=False,
                                parse_dates = ['DT_SIN_PRI','SEM_PRI','DT_NOTIFIC','SEM_NOT'])
        data_test = data_test.drop(columns = ['Unnamed: 0'])
        
        g = data_test.groupby(['SG_UF_NOT','ID_MUNICIP','SOROTIPO'])['SOROTIPO'].size()
        g = g.to_frame(name = 'NUMBER').reset_index()
        g['YEAR'] = year
        
        g = g[g['SG_UF_NOT'] != '  ']
        g['SG_UF_NOT'] = g['SG_UF_NOT'].astype(int)
        g['UF_NAME'] = g['SG_UF_NOT'].replace(dict_states)
        data_total = data_total.append(g)
    data_total_grouped = data_total.groupby(['YEAR','SOROTIPO','SG_UF_NOT', 'UF_NAME','ID_MUNICIP'])['NUMBER'].sum()
    data_total_grouped = data_total_grouped.to_frame(name = 'NUMBER').reset_index()
    # create final dataframe
    data_final = pd.DataFrame()
    #filter out errors in municipality not being consistent with state
    data_total_grouped['ID_MUNICIP'] = data_total_grouped['ID_MUNICIP'].astype(str)
    for i in data_total_grouped['SG_UF_NOT'].unique():
        df_tmp = data_total_grouped[data_total_grouped['SG_UF_NOT'] == i]
        df_tmp = df_tmp[df_tmp['ID_MUNICIP'].str.startswith(str(i))]
        data_final = data_final.append(df_tmp)
    data_final['ID_MUNICIP'] = data_final['ID_MUNICIP'].astype(int)
    path_save = 'Data/'
    file_save =  path_save+'dengue_BR_serotypes.csv'
    if(not(os.path.exists(path_save))):
        os.makedirs(path_save)
    data_final.to_csv(file_save, sep=';')
    
serotype_states()
    
