# Cases data for any municipality including the age groups TABNET of
# dataSUS, separating by age group to see the age profile of people infected
# we will also separate by serotype since it could be important
# Code developed by Denise Cammarota

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys 
import glob

def process_age_serotype():
    years = np.arange(2007,2022,1)
    data_total = pd.DataFrame()
    for year in years:
        file_path = 'Data/DataBR_Processed/dengue_BR_'+str(year)+'.csv'
        
        data_test = pd.read_csv(file_path, 
                                delimiter = ';',
                                index_col=False,
                                parse_dates = ['DT_SIN_PRI','SEM_PRI','DT_NOTIFIC','SEM_NOT'])
    
        # first column is read differently
        df = data_test.copy()
        
        age_groups = np.array([0,4,9,14,19,29,39,49,59,69,79,120]) # age groups of tabnet datasus
        
        # group by age, serotype and separate by age groups
        df = df[['NU_IDADE_N','SOROTIPO','NU_ANO','ID_MUNICIP']]
        df['age_range'] = df.groupby(['NU_ANO','SOROTIPO','ID_MUNICIP','NU_IDADE_N'])[['NU_IDADE_N']].transform(lambda x: pd.cut(x, bins = age_groups).astype(str))
        
        data_total = data_total.append(df)
    data_total.to_csv('Data/dengue_BR_ageclasses.csv', sep = ';')

process_age_serotype()