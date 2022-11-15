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
    bad_data = 0
    
    while start_year < 2019:
        year_brackets.append(str(start_year) + ' - ' + str(start_year+9))
        start_year = start_year + 10     
    crashDate_df = pd.DataFrame(columns=year_brackets)
    
    
    for i in range(df.shape[0]):
        if pd.isnull(df.iat[i,date_column_idx]):
            pass
        elif int(df.iat[i,date_column_idx][-4:]) > 2019 or int(df.iat[i,date_column_idx][-4:]) < 1919:
            bad_data = bad_data +1
        elif (start_range + 10) == int(df.iat[i,date_column_idx][-4:]):
            year_brackets_count.append(count)
            count = 1
            start_range = start_range + 10
        else:
            count = count + 1
    print(year_brackets)
    print(year_brackets_count)     
    print(sum(year_brackets_count))
    print(df.shape[0])
