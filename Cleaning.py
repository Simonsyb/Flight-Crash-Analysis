import numpy as np
import pandas as pd

base_url = "https://raw.githubusercontent.com/Simonsyb/Flight-Crash-Analysis/main/Airplane_Crashes_and_Fatalities_Since_1908_20190820105639.csv"

def limit_years(starting_year):
  






def count_null(url):
    df = pd.read_csv(url)
    null_df = pd.DataFrame(columns=df.columns)
    null_count = []
    
    for i in range(df.shape[1]):
        count = 0
        for j in range(df.shape[0]):
            if pd.isnull(df.iat[j,i]):
                count = count + 1
        null_count.append(count)
        
    null_df.loc[len(null_df.index)] = null_count
    print(null_df)
        
    
