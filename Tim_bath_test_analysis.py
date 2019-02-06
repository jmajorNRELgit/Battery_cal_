# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 15:01:33 2019

@author: jmajor
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np




TEG_file = 'C:/Users/jmajor/Desktop/github/Battery_cal_/TIM_data/ten_min_bath_shutoff Feb 05 2019, time_14_55_19.csv'
df = pd.read_csv(TEG_file)

data_range_high = None
range_low = 1000

times = df['Time'][range_low:data_range_high]
volts = df['Voltage'][range_low:data_range_high]
currents = df['Current'][range_low:data_range_high]
base = df['Ground'][range_low:data_range_high]

TIM_file = 'C:/Users/jmajor/Desktop/github/Battery_cal_/TIM_data/TEG_test_pre_shutoff.txt'
df2 = pd.read_table(TIM_file,index_col = None, skiprows = 15, names = ['Temp1','Temp2','Temp3','Temp4'], usecols = [0,1,2,3])

temp1 = df2['Temp1']
temp2 = df2['Temp2']
temp3 = df2['Temp3']
temp4 = df2['Temp4']


f = plt.figure(figsize=(10,5), dpi = 100) #creates the matplotlib figure
ax1 = f.add_subplot(211) #adds the top plot (full time and partial time plots)
ax2 = f.add_subplot(212) #STD plot

ax1.plot(times, currents, 'o')
ax1.plot(times, currents, 'y-')
#ax1.plot(times,volts, 'ro')
#ax1.plot(times,volts, 'b-')
#ax1.plot(times, base, 'ro')
#ax1.plot(times, base, 'g-')
ax1.legend()


ax2.plot(temp1, 'ro')
ax2.plot(temp1)
ax2.plot(temp2, 'ro')
ax2.plot(temp2)
ax2.plot(temp3, 'ro')
ax2.plot(temp3)
ax2.plot(temp4, 'ro')
ax2.plot(temp4)
ax2.legend()
