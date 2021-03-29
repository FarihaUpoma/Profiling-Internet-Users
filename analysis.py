#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 11:19:56 2019

@author: farihamoomtaheen
"""

import os
import pandas as pd


os.chdir("analysis")
path = os.getcwd()
files = os.listdir(path)
excelFiles = [f for f in files if f[-4:] == 'xlsx']
excelFiles.sort()

match = []

j = 0
count = 0
for file in range(len(excelFiles)):
    count = 0
    total = 0
    df = pd.read_excel(excelFiles[file], sheet_name = 'Sheet1')
    print(excelFiles[file])
    for index, row in df.iterrows():
    #row = next(df.iterrows())[1]
        #print(row)
        for ind in range(len(row)):
            total = total + 1
            if row[ind] > 0.5:
                count = count + 1
    match.insert(j, count)
    percentage = (count / total) * 100
    print(count, total, percentage)

avg = (match[0]+match[1]+match[2])/3
print(avg)