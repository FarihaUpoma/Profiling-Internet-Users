#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 01:28:34 2019

@author: farihamoomtaheen
"""


def calculate_zValue(r1a2a, r1a2b, r2a2b):

    rm2 = ((r1a2a ** 2) + (r1a2b ** 2)) / 2
    f = (1 - r2a2b) / (2 * (1 - rm2))
    h = (1 - f * rm2) / (1 - rm2)

    z1a2a = 0.5 * (math.log10((1 + r1a2a)/(1 - r1a2a)))
    z1a2b = 0.5 * (math.log10((1 + r1a2b)/(1 - r1a2b)))

    z = (z1a2a - z1a2b) * (( len(val1) -3) ** 0.5) / (2 * (1 - r2a2b) * h)

    return z

def calculate_pValue(z):
    p = 0.3275911
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429

    sign = None
    if z < 0.01:
        sign = -1
    else:
        sign = 1

    x = abs(z) / (2 ** 0.5)
    t = 1 / (1 + p * x)
    erf = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x*x)

    return 0.5 * (1 + sign * erf)


def populate_weekSheet():
    
    for k in range(len(df['Real First Packet'])):
        t = df['Real First Packet'][k] / 1000
        x = time.strftime("%A %d %m %Y %H %M %S +0000", time.localtime(t))
        x = x.split(" ")
        year = int(x[3])
        month = int(x[2])
        day = int(x[1])
        hour = int(x[4])
        minute = int(x[5])
        second = int(x[6])
        xx = datetime.datetime(year, month, day, hour, minute, second)
        delta = xx - startTime
        delta2 = xx - startTime2
        
        if delta.days >= 0 and delta.days < 5 and xx.time() >= startTime.time() and xx.time() < endTime.time() and df['Duration'][k] > 0:
            stHour = int(startTime.strftime("%H"))
            indx = delta.days * 142 + int(((hour-stHour) * 3600 + int(minute * 60) + second) / 227)
            od = df['doctets'][k] / df['Duration'][k]
            if indx >= 715:
                print(indx)
                print(xx)
            if countVal[indx] == 0:

                d.at[indx, 'Octets/Duration'] = od
            else:
                prev = d['Octets/Duration'][indx]
                d.at[indx, 'Octets/Duration'] = (prev * countVal[indx] + od ) / (countVal[indx] + 1)
            countVal[indx] = countVal[indx] + 1
            
        elif delta2.days >= 0 and delta2.days < 5 and xx.time() >= startTime2.time() and xx.time() < endTime2.time() and df['Duration'][k] > 0:
            stHour = int(startTime2.strftime("%H"))
            
            indx = delta2.days * 142 + int(((hour-stHour) * 3600 + int(minute * 60) + second)/227)
            od = df['doctets'][k] / df['Duration'][k]
            if countVal[indx] == 0:
                dd.at[indx, 'Octets/Duration'] = od
            else:
                prev = dd['Octets/Duration'][indx]
                dd.at[indx, 'Octets/Duration'] = (prev * countVal[indx] + od ) / (countVal[indx] + 1)
            countVal[indx] = countVal[indx] + 1
    


def create_weekSheet(startTime, endTime):
    
    dff = pd.DataFrame(columns = columns)
    weekList = []
    timeList = []
    fromList = []
    toList = []
    
    t1 = startTime
    j = 0
    for i in range(0,5):
        flag = 0
        while True:
            t2 =  t1 + td
            
            if t2 >= endTime:
                t2 = endTime
                flag = 1
    #make string with t1.time() and t2.time()
            s1 = t1.strftime("%I:%M:%S%p")
            s = s1 + "-" + t2.strftime("%I:%M:%S%p")
            
            fromList.insert(j, t1)
            toList.insert(j, t2)
            timeList.insert(j, s)
            weekList.insert(j, weekdays[i%5])
            
            t1 = t2
            j = j + 1
            if flag == 1:
                if i < 4:
                    t1 = t1 + newDay
                    endTime = endTime + newEnd
                break
    
    dff['Weekday'] = weekList
    dff['Time'] = timeList
    dff['fromTime'] = fromList
    dff['toTime'] = toList
    #dff['Octets/Duration'] = countList    
    
    return dff



import pandas as pd
import time
import datetime
import os
import scipy.stats
import math

columns = ['Weekday', 'fromTime', 'toTime', 'Time', 'Octets/Duration']
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
zeroList = [0.00] * 715
opdWeek1 = [[]]
opdWeek2 = [[]]

os.chdir("users")
path = os.getcwd()
files = os.listdir(path)
excelFiles = [f for f in files if f[-4:] == 'xlsx']
excelFiles.sort()

for user in range(len(excelFiles)):
#for user in range(54):

    countVal = [0] * 715

    df = pd.read_excel(excelFiles[user], sheet_name = 'Sheet1')
    
    t = df['Real First Packet'][0]/1000
    x = time.strftime("%A %d %m %Y %H %M %S +0000", time.localtime(t))
    x = x.split(" ")
    print("working with", user)
    adjust = 0
    if x[0] != 'Monday':
        for i in range(5):
            if weekdays[i] == x[0]:
                adjust = 7-i
                break
    
    year = int(x[3])
    month = int(x[2])
    day = int(x[1])
    hour = int(x[4])
    minute = int(x[5])
    second = int(x[6])
    xx = datetime.datetime(year, month, day, hour, minute, second)
    xx = xx + datetime.timedelta(days = adjust)
    
    year = int(xx.strftime("%Y"))
    month = int(xx.strftime("%m"))
    day = int(xx.strftime("%d"))
    
    startTime = datetime.datetime(year, month, day, 8, 0, 0)
    endTime = datetime.datetime(year, month, day, 17, 0, 0)
    
    nD = datetime.timedelta(days = 7)
    startTime2 = startTime + nD
    endTime2 = endTime + nD
    
    
    print("test start end")
    print(startTime)
    print(startTime2)
    
    newDay = datetime.timedelta(hours = 15)
    newEnd = datetime.timedelta(days = 1)
    
    
    #choose time window
    #td = datetime.timedelta(seconds = 10)
    td = datetime.timedelta(seconds = 227)
    #td = datetime.timedelta(minutes = 5)
    
    dff = pd.DataFrame(columns = columns)
    
    filename1 = "Subject" + str(user+1) + "_week1.xlsx"
    filename2 = "Subject" + str(user+1) + "_week2.xlsx"
    
    
    d = create_weekSheet(startTime, endTime)
    
    dd = create_weekSheet(startTime2, endTime2)
    
    weekEnd = endTime + nD
    weekEnd2 = endTime2 + nD

    d['Octets/Duration'] = zeroList
    dd['Octets/Duration'] = zeroList
    
    populate_weekSheet()
    
    
    opdWeek1.insert(user, d['Octets/Duration'])
    opdWeek2.insert(user, dd['Octets/Duration'])
    
    os.chdir("../usersOutput-Window227")
    d.to_excel(filename1)
    dd.to_excel(filename2)
    os.chdir("../users")


userList = ['User1', 'User2', 'User3', 'User4', 'User5', 'User6', 'User7', 'User8', 'User9', 'User10', 'User11', 'User12', 'User13', 'User14', 'User15', 'User16', 'User17', 'User18', 'User19', 'User20', 'User21', 'User22', 'User23', 'User24', 'User25', 'User26', 'User27', 'User28', 'User29', 'User30', 'User31', 'User32', 'User33', 'User34', 'User35', 'User36', 'User37', 'User38', 'User39', 'User40', 'User41', 'User42', 'User43', 'User44', 'User45', 'User46', 'User47', 'User48', 'User49', 'User50', 'User51', 'User52', 'User53', 'User54' ]
finalTable = pd.DataFrame(columns = userList, index = userList)

print("done hishab")

for userA in range(54):
    val1 = opdWeek1[userA]
    val2 = opdWeek2[userA]
    r1a2a = scipy.stats.spearmanr(val1, val2)[0]
    ind1 = "User"+ str(userA+1)
    for userB in range(54):
        val3 = opdWeek2[userB]
        #if (val3['Octets/Duration'] == 0).all() or (val1['Octets/Duration'] == 0).all() or (val2['Octets/Duration'] == 0).all():
#        if (val3['Octets/Duration'] = 0).all():
#            print("BLABLABLABLABL")
#            continue
        r1a2b = scipy.stats.spearmanr(val1, val3)[0]
        r2a2b = scipy.stats.spearmanr(val2, val3)[0]
        if r1a2a == 1.00:
            r1a2a = 0.99
        if r1a2b == 1.00:
            r1a2b = 0.99
        if r2a2b == 1.00:
            r2a2b = 0.99
        #print(r1a2a, r1a2b, r2a2b)
        z = calculate_zValue(r1a2a, r1a2b, r2a2b)
        pVal = calculate_pValue(z)
        ind2 = "User"+ str(userB+1)
        #print(ind1, ind2)
        finalTable.at[ind1, ind2] = pVal
        
os.chdir("../")
finalTable.to_excel("results/finalTable227.xlsx")

