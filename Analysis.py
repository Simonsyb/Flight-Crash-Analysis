def crash_times(df):
    crashTime_df = pd.DataFrame(columns=['Morning','Afternoon','Evening','Night','Faulty Data'])
    crashTime_count = []
    time_column_idx = df.columns.get_loc("Time")
    morning_crash = 0
    afternoon_crash = 0
    evening_crash = 0
    night_crash = 0
    bad_data = 0

    for i in range(df.shape[0]):
        if pd.isnull(df.iat[i,time_column_idx]):
            pass
        elif int(df.iat[i,time_column_idx][:2]) >= 24:
            bad_data = bad_data +1
        elif 0 <= int(df.iat[i,time_column_idx][:-3]) and int(df.iat[i,time_column_idx][:-3]) <= 5:
            night_crash = night_crash +1
        elif 6 <= int(df.iat[i,time_column_idx][:-3]) and int(df.iat[i,time_column_idx][:-3]) <= 11:
            morning_crash = morning_crash +1
        elif 12 <= int(df.iat[i,time_column_idx][:-3]) and int(df.iat[i,time_column_idx][:-3]) <= 17:
            afternoon_crash = afternoon_crash +1
        elif 18 <= int(df.iat[i,time_column_idx][:-3]) and int(df.iat[i,time_column_idx][:-3]) <= 23:
            evening_crash = evening_crash +1

    crashTime_count.extend([morning_crash,afternoon_crash,evening_crash,night_crash,bad_data])        
    crashTime_df.loc[len(crashTime_df.index)] = crashTime_count
    return crashTime_df

def crash_dates(df):
    start_year = 1919
    start_range = 1919
    count = 0
    year_brackets = []
    year_brackets_count = []
    date_column_idx = df.columns.get_loc("Date")
    
    while start_year < 2019:
        year_brackets.append(str(start_year) + ' - ' + str(start_year+9))
        start_year = start_year + 10     
    crashDate_df = pd.DataFrame(columns=year_brackets)
    
    
    for i in range(df.shape[0]):
        if pd.isnull(df.iat[i,date_column_idx]):
            pass
        elif (start_range + 10) == int(df.iat[i,date_column_idx][-4:]):
            year_brackets_count.append(count)
            count = 1
            start_range = start_range + 10
        else:
            count = count + 1
    year_brackets_count.append(count)

    crashDate_df.loc[len(crashDate_df.index)] = year_brackets_count 
    return crashDate_df


def crash_deaths(df):
    start_year = 1919
    start_range = 1919
    year_brackets = []
    count_a = 0
    count_d = 0
    
    death_df = pd.DataFrame()
    date_column_idx = df.columns.get_loc("Date")
    aboard_column_idx = df.columns.get_loc("Aboard")
    death_column_idx = df.columns.get_loc("Fatalities")

    aboard_count = []
    survive_count = []
    death_count = []
    
    while start_year < 2019:
        year_brackets.append(str(start_year) + ' - ' + str(start_year+9))
        start_year = start_year + 10
    
    
    for i in range(df.shape[0]):
        if pd.isnull(df.iat[i,aboard_column_idx]):
            pass
        elif (start_range + 10) == int(df.iat[i,date_column_idx][-4:]):
            aboard_count.append(count_a)
            death_count.append(count_d)
            count_a = df.iat[i,aboard_column_idx]
            count_d = df.iat[i,death_column_idx]
            start_range = start_range + 10
        else:
            count_a = count_a + df.iat[i,aboard_column_idx]
            count_d = count_d + df.iat[i,death_column_idx]
            
    aboard_count.append(count_a)
    death_count.append(count_d)
    death_df=death_df.assign(Aboard=aboard_count,Deaths=death_count,Survivors=[a - b for a, b in zip(aboard_count, death_count)])
    death_df.index = year_brackets

    return death_df

def crash_cause(df):
    fire_count, fire_death = 0,0
    hijack_count, hijack_death = 0,0
    weather_count,weather_death = 0,0
    shot_count,shot_death = 0,0
    other_count,other_death = 0,0
    na_count,na_death = 0,0
    
    final_counts,final_deaths = [],[]
    crashCause_df = pd.DataFrame(columns=['Fire','Hijack','Weather','Shot Down','Other','N/A'])
    summary_column_idx = df.columns.get_loc("Summary")
    death_column_idx = df.columns.get_loc("Fatalities")

    for i in range(df.shape[0]):
        if pd.isnull(df.iat[i,summary_column_idx]):
            na_count = na_count+1
            if pd.notnull(df.iat[i,death_column_idx]):   
                na_death = na_death + df.iat[i,death_column_idx]
        elif "hijack" in df.iat[i,summary_column_idx] or "Hijack" in df.iat[i,summary_column_idx] :
            hijack_count = hijack_count + 1
            if pd.notnull(df.iat[i,death_column_idx]):  
                hijack_death = hijack_death + df.iat[i,death_column_idx]
        elif "shot" in df.iat[i,summary_column_idx] or "Shot" in df.iat[i,summary_column_idx] :
            shot_count = shot_count + 1
            if pd.notnull(df.iat[i,death_column_idx]):  
                shot_death = shot_death + df.iat[i,death_column_idx]
        elif "fire" in df.iat[i,summary_column_idx] or "Fire" in df.iat[i,summary_column_idx] :
            fire_count = fire_count + 1
            if pd.notnull(df.iat[i,death_column_idx]):  
                fire_death = fire_death + df.iat[i,death_column_idx]
        elif "weather" in df.iat[i,summary_column_idx] or "Weather" in df.iat[i,summary_column_idx] :
            weather_count = weather_count + 1
            if pd.notnull(df.iat[i,death_column_idx]):  
                weather_death =weather_death + df.iat[i,death_column_idx]
        else:
            other_count = other_count+1
            if pd.notnull(df.iat[i,death_column_idx]):  
                other_death = other_death + df.iat[i,death_column_idx]
            
    final_deaths.extend((fire_death,hijack_death,weather_death,shot_death,other_death,na_death))       
    final_counts.extend((fire_count,hijack_count,weather_count,shot_count,other_count,na_count))
    crashCause_df.loc[len(crashCause_df.index)] = final_counts
    crashCause_df.loc[len(crashCause_df.index)] = final_deaths
    print(sum(final_deaths))
    return crashCause_df


def crash_operators(df):
    df_upd = df['Operator'].value_counts()
    return df_upd

def crash_aircrafts(df):
    df_upd = df['AC Type'].value_counts()
    return df_upd

