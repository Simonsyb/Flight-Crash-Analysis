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
