# Serotype ocurrence as whole for Rio de Janeiro per epi week
# years 2007 to 2021, sorotipo available for all these times
# Code developed by Denise Cammarota

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys 
import glob
from epiweeks import Year

def serotype_RJ(id_mun):
    # years we use for analysis
    years = np.arange(2007,2024,1)
    data_total = pd.DataFrame()
    # processing for each state and each year
    for year in years:
        file_path = 'Data/DataBR_Processed/dengue_BR_'+str(year)+'.csv'
        # find year corresponding to file
        if(year >= 2007):
            id_mun_real = id_mun[0:6]
        else:
            id_mun_real = id_mun
        data_test = pd.read_csv(file_path, 
                                delimiter = ';',
                                index_col=False,
                                parse_dates = ['DT_SIN_PRI','SEM_PRI','DT_NOTIFIC','SEM_NOT'])
        data_test = data_test.drop(columns = ['Unnamed: 0'])
        filt_df1 = (data_test['ID_MN_RESI'] == id_mun_real)
        data_test = data_test[filt_df1]
        data_total = data_total.append(data_test)
    
    #data_total = data_total[data_total['ID_MN_RESI'] == 330455]
    data_total['NUMBER'] = 1
    
    data_total_grouped = data_total.groupby(['SEM_PRI','SOROTIPO'])['NUMBER'].sum()
    data_total_grouped = data_total_grouped.to_frame(name = 'NUMBER').reset_index()
    
    # Now we have to do the actual padding
    years_int = np.arange(min(years),max(years)+1,1)
    
    year_week_epi = []
    for year in years_int:
        nweeks_year = Year(year).totalweeks()
        weeks_year = list(np.arange(1,nweeks_year+1))
        weeks_year = [str(x) for x in weeks_year]
        weeks_year = ['0'+x if len(x) == 1 else x for x in weeks_year]
        weeks_year = [str(year)+x for x in weeks_year]
        year_week_epi.extend(weeks_year)
    cases_week_epi = list(np.zeros(len(year_week_epi)))
    
    df_aux = pd.DataFrame({'SEM_PRI': year_week_epi, 'CASO': cases_week_epi})
    
    # Returning the results
    
    return data_total_grouped, df_aux
    
id_mun = '3550308'
df_data, df_aux = serotype_RJ(id_mun)
    
df_aux = df_aux.merge(df_data, how = 'left', on = 'SEM_PRI')
df_aux = df_aux.drop(columns = 'CASO')

df_aux = df_aux.replace(np.nan,0)
df_aux = df_aux.replace(' ',0)

df_copy = df_aux.copy()


df_copy = df_copy.pivot_table(values='NUMBER', index='SEM_PRI', columns='SOROTIPO', aggfunc='first')
df_copy = df_copy.reset_index()
df_copy = df_copy.fillna(0)
df_copy['CASES'] = df_copy[0] + df_copy['1'] + df_copy['2'] + df_copy['3'] + df_copy['4']

df_copy.to_csv('serotypes_SP.csv')