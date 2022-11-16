import numpy as np
import pandas as pd
from collections import Counter
from operator import sub
import cleaning


#Determines which quater of the day the plane crashes happens. Split into 4 brackets
#each being 6 hours long.
def crash_times(df):
    crashTime_count = []
    morning_crash, afternoon_crash, evening_crash, night_crash, faulty_data = 0,0,0,0,0
    crashTime_df = pd.DataFrame(columns=['Morning','Afternoon','Evening','Night','Faulty Data'])
    time_column_idx = df.columns.get_loc("Time")

    for i in range(df.shape[0]):
        if pd.isnull(df.iat[i,time_column_idx]):
            pass
        elif int(df.iat[i,time_column_idx][:2]) >= 24:
            faulty_data += 1
        elif 0 <= int(df.iat[i,time_column_idx][:-3]) and int(df.iat[i,time_column_idx][:-3]) <= 5:
            night_crash += 1
        elif 6 <= int(df.iat[i,time_column_idx][:-3]) and int(df.iat[i,time_column_idx][:-3]) <= 11:
            morning_crash += 1
        elif 12 <= int(df.iat[i,time_column_idx][:-3]) and int(df.iat[i,time_column_idx][:-3]) <= 17:
            afternoon_crash += 1
        elif 18 <= int(df.iat[i,time_column_idx][:-3]) and int(df.iat[i,time_column_idx][:-3]) <= 23:
            evening_crash += 1

    crashTime_count.extend([morning_crash,afternoon_crash,evening_crash,night_crash,faulty_data])        
    crashTime_df.loc[len(crashTime_df.index)] = crashTime_count
    crashTime_df.index = ['Crash Count']
    return crashTime_df


#Determine the number of plane crashes in 10 year intervals over the last 100 years.
def crash_dates(df):
    start_year, interval = 1919, 1919
    count = 0
    year_brackets, crash_count = [],[]
    date_column_idx = df.columns.get_loc("Date")
    crashDate_df = pd.DataFrame(columns=['CrashCount'])

    #Creates a list containing the brackets.
    while start_year < 2019:
        year_brackets.append(str(start_year) + ' - ' + str(start_year+9))
        start_year += 10     

    #Creates a list of the # of crashes in 10 year intervals.
    for i in range(df.shape[0]):
        if pd.isnull(df.iat[i,date_column_idx]):
            pass
        elif (interval + 10) == int(df.iat[i,date_column_idx][-4:]):
            crash_count.append(count)
            count = 1
            interval += 10
        else:
            count += 1
    crash_count.append(count)

    #Combine our two lists into a DF
    crashDate_df=crashDate_df.assign(CrashCount=crash_count)
    crashDate_df.index = year_brackets
    return crashDate_df


#Determines the number of people on board, death and survivors for each of
#the 10 year interval brackets.
def crash_deaths(df):
    start_year, interval = 1919, 1919
    count_a,count_d = 0,0
    year_brackets = []
    aboard_count,death_count = [], []
    
    death_df = pd.DataFrame()
    date_column_idx = df.columns.get_loc("Date")
    aboard_column_idx = df.columns.get_loc("Aboard")
    death_column_idx = df.columns.get_loc("Fatalities")
    
    while start_year < 2019:
        year_brackets.append(str(start_year) + ' - ' + str(start_year+9))
        start_year += 10

    #Counts the number of people on board and deaths that occured.
    for i in range(df.shape[0]):
        if pd.isnull(df.iat[i,aboard_column_idx]):
            pass
        elif (interval + 10) == int(df.iat[i,date_column_idx][-4:]):
            aboard_count.append(count_a)
            death_count.append(count_d)
            count_a = df.iat[i,aboard_column_idx]
            count_d = df.iat[i,death_column_idx]
            interval += 10
        else:
            count_a = count_a + df.iat[i,aboard_column_idx]
            count_d = count_d + df.iat[i,death_column_idx]
            
    aboard_count.append(count_a)
    death_count.append(count_d)
    death_df=death_df.assign(Aboard=aboard_count,Deaths=death_count,Survivors=[a - b for a, b in zip(aboard_count, death_count)]) #Subtract deaths from people on bored to find the survivors.
    death_df.index = year_brackets
    return death_df


#Determines the number of plane crashes and fatalities that were caused by fire, a hijacking,
#weather, shot down, other or N/A
def crash_cause(df):
    fire_count, fire_death = 0,0
    hijack_count, hijack_death = 0,0
    weather_count,weather_death = 0,0
    shot_count,shot_death = 0,0
    other_count,other_death = 0,0
    na_count,na_death = 0,0
    final_counts,final_deaths = [],[]

    summary_column_idx = df.columns.get_loc("Summary")
    death_column_idx = df.columns.get_loc("Fatalities")
    crashCause_df = pd.DataFrame(columns=['Fire','Hijack','Weather','Shot Down','Other','N/A'])

    #Sorts each crash situation into one of the 6 catagories
    for i in range(df.shape[0]):
        if pd.isnull(df.iat[i,summary_column_idx]):
            na_count +=1
            if pd.notnull(df.iat[i,death_column_idx]):   
                na_death += df.iat[i,death_column_idx]
        elif "hijack" in df.iat[i,summary_column_idx].lower():
            hijack_count += 1
            if pd.notnull(df.iat[i,death_column_idx]):  
                hijack_death += df.iat[i,death_column_idx]
        elif "shot" in df.iat[i,summary_column_idx].lower():
            shot_count += 1
            if pd.notnull(df.iat[i,death_column_idx]):  
                shot_death += df.iat[i,death_column_idx]
        elif "fire" in df.iat[i,summary_column_idx].lower():
            fire_count += 1
            if pd.notnull(df.iat[i,death_column_idx]):  
                fire_death += df.iat[i,death_column_idx]
        elif "weather" in df.iat[i,summary_column_idx].lower(): 
            weather_count += 1
            if pd.notnull(df.iat[i,death_column_idx]):  
                weather_death += df.iat[i,death_column_idx]
        else:
            other_count += 1
            if pd.notnull(df.iat[i,death_column_idx]):  
                other_death += df.iat[i,death_column_idx]
                
    #Combines the two lists ands adds them into our DF as well as lables for our indexs.       
    final_deaths.extend((fire_death,hijack_death,weather_death,shot_death,other_death,na_death))       
    final_counts.extend((fire_count,hijack_count,weather_count,shot_count,other_count,na_count))
    crashCause_df.loc[len(crashCause_df.index)] = final_counts
    crashCause_df.loc[len(crashCause_df.index)] = final_deaths
    crashCause_df.index = ['# of crashes','Fatalities']
    return crashCause_df


#Gives you the operator and the coresponding # of fatalities of that have occured on their flights.
def operator_deaths(df):
    df_upd = df['Operator'].value_counts()
    optor = df['Operator'].value_counts().keys()
    opDeaths_df = pd.DataFrame(columns=['Operator','Deaths'])
    operator_names, death_counts = [], []

    #Creates a list of the number of fatalities
    for i in range(len(optor)):
        count = df.loc[df['Operator'] == optor[i], 'Fatalities'].sum()
        death_counts.append(count)

    #Creates a list of operator names   
    for i in range(len(optor)):
        operator_names.append(optor[i])

    opDeaths_df=opDeaths_df.assign(Operator=operator_names,Deaths=death_counts)
    return opDeaths_df


#Gives you the aircraft type and the coresponding # of fatalities of that have occured on it.
def aircraft_deaths(df):
    df_upd = df['AC Type'].value_counts()
    ac_type = df['AC Type'].value_counts().keys()
    acDeaths_df = pd.DataFrame(columns=['Aircraft','Deaths'])
    death_counts = []
    ac_names = []
    
    for i in range(len(ac_type)):
        count = df.loc[df['AC Type'] == ac_type[i], 'Fatalities'].sum()
        death_counts.append(count)
        
    for i in range(len(ac_type)):
        ac_names.append(ac_type[i])


    acDeaths_df=acDeaths_df.assign(Aircraft=ac_names,Deaths=death_counts)
    return acDeaths_df


#Determines the total number of crashes each operator was involved in.   
def crash_operators(df):
    df_upd = df['Operator'].value_counts()
    return df_upd


#Determines the total number of crashes each aircraft was involved in.   
def crash_aircrafts(df):
    df_upd = df['AC Type'].value_counts()
    return df_upd


#Determines the total number of crashes based on location.
def crash_locations(df):
    df_upd = df['Location'].value_counts()
    return df_upd


if __name__ == "__main__":
    #Determine what time of the day that planes tend to crash
    print("The time of day that crashes happened at")
    print(crash_times(cleaning.limit_years(1919,cleaning.limit_columns())))
    print()
    print()

    #Determine the number of number of crashes per 10 year intervals
    print("The 10 year intervals with their associated count of plane crashes")
    print(crash_dates(cleaning.limit_years(1919,cleaning.limit_columns())))
    print()
    print()

    #Detemines the number of people on board, the # of deaths and the # of survivors for each 10 year bracket.
    print("The count of all passengers on board, deaths amd survivors.")
    print(crash_deaths(cleaning.limit_years(1919,cleaning.limit_columns())))
    print()
    print()

    #Classifies the reason for the crash into catagories. Gives total count and # of fatalities for each reason.
    print("Categorizes the reason for each crash as well as the number of fatalities.")
    print(crash_cause(cleaning.limit_years(1919,cleaning.limit_columns())))
    print()
    print()

    #Compares operators to fatalities
    print("The number of fatalities of each operator")
    print(operator_deaths(cleaning.limit_years(1919,cleaning.limit_columns())))
    print()
    print()

    #Compares aircraft model to fatalities
    print("Aircraft type and the number of fatalities that have occured while on board")
    print(aircraft_deaths(cleaning.limit_years(1919,cleaning.limit_columns())))
    print()
    print()

    #Determine what operators crash the most often
    print("Operators and their total number of crashes")
    print(crash_operators(cleaning.limit_years(1919,cleaning.limit_columns())))
    print()
    print()

    #Determine what aircrafts crash the most often
    print("Aircrafts and their total number of crashes")
    print(crash_aircrafts(cleaning.limit_years(1919,cleaning.limit_columns())))
    print()
    print()

    #Determine what locations the most crashes happen in.
    print("Locations with associated count of plane crashes")
    print(crash_locations(cleaning.limit_years(1919,cleaning.limit_columns())))
