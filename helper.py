import pandas as pd
import numpy as np
import calendar
import datetime

# Churn periods
churn = {'A': 360, 'B': 360, 'C': 120, 'D': 260}

def check_usertype(uid, df):
    print(df)
    df_temp = df.loc[df['_id'] == uid]

    if len(df_temp) == 1:
        return None
    
    userType = list(set(list(df_temp['usertype'])))

    if len(userType) > 1:
        return df_temp.index[0]

def find_return_user(uid, np_merge, np_ft_churn, dropOff, returnUser):
    i = np.where(np_merge == uid)[0]
    v = np.where(np_ft_churn == uid)[0]
    np_temp = np_merge[i]
    np_temp_ft = np_ft_churn[v]

    # Check if single
    if len(np_temp) <= 1:
        return (dropOff, returnUser)

    churn_period = np_temp_ft[0][1]
    for r in np_temp:
        if r[1] < churn_period:
            continue
        
        else:
            dropOff["{}-{}".format(calendar.month_name[churn_period.month], churn_period.year)] += 1
            returnUser["{}-{}".format(calendar.month_name[r[1].month], r[1].year)] += 1

            if r[4] == False:
                churn_period = r[1] + datetime.timedelta(days=churn[r[2]])

    return (dropOff, returnUser)