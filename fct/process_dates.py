# Processing of cases as whole for any files after initial clean 
# years 2000 to 2021, compatibilized in order to know the total time series
# doesn't include imported or not imported cases actually
# Code developed by Denise Cammarota


import numpy as np
import pandas as pd

def process_dates(df):
    min_year = min(df['SIN_YEAR'])
    max_year = max(df['SIN_YEAR'])
    if(max_year > 2021):
        max_year = 2021
    years = np.arange(min_year,max_year+1,1)

    # generate weeks for each years and count cases 
    list_year = []
    list_week = []
    list_begin = []
    list_cases = []
    list_imported = []


    for year in years:
        start_year = str(year)+'-01-01'
        end_year = str(year)+'-12-31'
        weeks_year = pd.date_range(start=start_year, end = end_year, freq='W-SUN', inclusive = 'left')
        n_weeks = len(weeks_year)
        for week in range(n_weeks):
            list_year.append(year)
            list_week.append(week+1)
            list_begin.append(weeks_year[week].date().strftime('%Y-%m-%d'))
            # and now we count the total number of cases 
            filt_df = ((df['SIN_WEEK'] == week) & (df['SIN_YEAR'] == year))
            df_tmp = df[filt_df]
            if df_tmp.empty == False:
                list_cases.append(df_tmp.iloc[0]['CASES'])
                list_imported.append(df_tmp.iloc[0]['IMPORTED'])
            else:
                list_cases.append(0)
                list_imported.append(0)

    df_final = pd.DataFrame(list(zip(list_year, list_week, list_begin, list_cases, list_imported)),
                   columns =['SIN_YEAR', 'SIN_WEEK', 'FIRST_DAY', 'CASES','IMPORTED'])

    return df_final

