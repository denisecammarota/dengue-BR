# Processing of cases separating imported cases for each municipality
# years 2007 onwards actually have the TPAUTOCTO field in order to filter this 
# Code developed by Denise Cammarota

import numpy as np
import pandas as pd

def process_imported(data_filtered_3, data_filtered_1, year):
    if(year >= 2007):
        df = data_filtered_1.groupby(['SIN_WEEK','SIN_YEAR','TPAUTOCTO'])['TPAUTOCTO'].size()
        df = df.to_frame(name = 'CASES').reset_index()
        df = df.replace(' ',3)
        df['TPAUTOCTO'] = df['TPAUTOCTO'].astype(int)
        df['CASES'] = df['CASES'].astype(int)
        df['new'] = df['TPAUTOCTO'].isin([1])
        df['new'] = df['new'].astype(int)
        # counting number of imported cases
        df['new_2'] = df['new']*df['TPAUTOCTO']*df['CASES']
        df = df.groupby(['SIN_WEEK','SIN_YEAR'])['new_2'].sum()
        df = df.to_frame(name = 'IMPORTED').reset_index()
        df['CASES'] = data_filtered_3['CASES']
        # permutating the two last columns
        columns_titles = ['SIN_WEEK','SIN_YEAR','CASES','IMPORTED']
        df = df.reindex(columns=columns_titles)
    else:
        df = data_filtered_3.copy()
        df['IMPORTED'] = 0
    return df