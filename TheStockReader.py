# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 09:05:36 2022

@author: dtket
"""
import os
import pandas as pd
import datetime
import numpy as np 
import matplotlib.pyplot as plt
path = os.getcwd()
files = os.listdir(path)
files_xls = [f for f in files if f[-4:] == 'xlsx']
df = pd.DataFrame()
corr=np.array([0.0]*500)
corr2=np.array([0.0]*500)
stockindex=0
tod = datetime.datetime.now() #todays date
ind=0
for stockindex in range(500):
    CurrentArray=np.array([])
    ExpectedArray=np.array([])
    for ind in range(len(files_xls)):
        d = datetime.timedelta(days = ind)
        now= tod-d
        nowstr = str(now.year)+ '_'+str(now.month)+'_'+  str(now.day)+'.xlsx'    
        data = pd.read_excel(nowstr)    
        CurrentArray = np.append(CurrentArray,[data.iloc[stockindex]['Current']])   
        ExpectedArray = np.append(ExpectedArray,[data.iloc[stockindex]['Expected']])   
    CurrentArray=CurrentArray[::-1]
    ExpectedArray=ExpectedArray[::-1]
    temp=np.corrcoef(CurrentArray[1:], ExpectedArray[:-1])[1][0]
    temp2=np.corrcoef(CurrentArray[1:], CurrentArray[:-1])[1][0]
    print(stockindex)
    print(temp)
    if np.isnan(temp):
        0
    else:
        corr[stockindex]  = temp
        corr2[stockindex] = temp2
        
        #    print(corr)
#    plt.figure(stockindex)
#    plt.plot(CurrentArray[1:],label="Actual")
#    plt.plot(ExpectedArray[:-1],label="Expected")
#    plt.legend()
#    plt.show()
        
corr3 = corr2 - corr