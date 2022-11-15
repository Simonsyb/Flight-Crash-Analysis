import numpy as np
import pandas as pd

base_url = "https://raw.githubusercontent.com/Simonsyb/Flight-Crash-Analysis/main/Airplane_Crashes_and_Fatalities_Since_1908_20190820105639.csv"

def limit_columns():
    df = pd.read_csv(base_url)
    df = df.drop(labels=["Flight #", "Registration", "cn/ln", "Ground"], axis=1)
    return df

def limit_years(starting_year,df):
    i = 0
    count = 0
    
    while int(df.iat[i,0][-4:]) < starting_year:
        i = i + 1

    df = df.drop(range(0,i))

    for j in range(df.shape[0]):
        if 2019 == int(df.iat[j,0][-4:]):
            count = count + 1

    df = df.drop(range(df.shape[0]-count,df.shape[0]))
    return df

def count_null(df):
    null_df = pd.DataFrame(columns=df.columns)
    null_count = []
    
    for i in range(df.shape[1]):
        count = 0
        for j in range(df.shape[0]):
            if pd.isnull(df.iat[j,i]):
                count = count + 1
        null_count.append(count)
        
    null_df.loc[len(null_df.index)] = null_count
    return null_df
        

print(count_null(limit_years(1919,limit_columns())))

