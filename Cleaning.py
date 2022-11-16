import numpy as np
import pandas as pd
from collections import Counter
from operator import sub

#Dataset titled "Airplane Crashes Since 1908" by Sauro Grandi. Downloaded @ 'https://www.kaggle.com/datasets/saurograndi/airplane-crashes-since-1908'
base_url = "https://raw.githubusercontent.com/Simonsyb/Flight-Crash-Analysis/main/Airplane_Crashes_and_Fatalities_Since_1908_20190820105639.csv"


#Cleaning the data to get rid of values that we won't need in our analysis.
#Majority of these columns are filled with null values leaving little to work with.
def limit_columns():
    df = pd.read_csv(base_url)
    df = df.drop(labels=["Flight #", "Registration", "cn/ln", "Ground"], axis=1)
    return df


#Cleaning the data to focus in on the 100 year peirod between 1919-2018.
def limit_years(starting_year,df):
    i = 0
    count = 0
    
    while int(df.iat[i,0][-4:]) < starting_year:
        i = i + 1
    df = df.drop(range(0,i)) #Drops years prior to 1919

    for j in range(df.shape[0]):
        if 2019 == int(df.iat[j,0][-4:]):
            count = count + 1
    df = df.iloc[:-count,:] #Drops years after 2018   
    return df


#Counts the amount of null cells in each of our columns.
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


if __name__ == "__main__":
    print()
    #print(limit_columns())
    #print(limit_years(1919,limit_columns()))
    #print(count_null(limit_years(1919,limit_columns())))
