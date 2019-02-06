# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 07:49:51 2019

@author: jmajor
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file = 'C:/Users/jmajor/Desktop/github/Battery_cal_/Data/bus bar pulse test_1 Feb 06 2019, time_12_00_55.csv'

df = pd.read_csv(file)

low = 0
high = 1400

low = int(low*.74)
high = int(high *.74)


#df.plot(x = 'Time')
print('\n')
print('TEG_voltage_voltage STD: ' + str(np.std(df['TEG1'])))
print('TEG2 STD: ' + str(np.std(df['TEG2'])))
print('Current STD: ' + str(np.std(df['Current'])))
print('\n')
print('TEG1 SNR: ' + str(np.abs(np.mean(df['TEG1']) / np.std(df['TEG1']))))
print('TEG2 SNR: ' + str(np.abs(np.mean(df['TEG2']) / np.std(df['TEG2']))))
print('Current SNR: ' + str(np.abs(np.mean(df['Current']) / np.std(df['Current']))))
print('\n')
print('Samples per second: ' + str(float(len(df['TEG1']) / df['Time'][-1:])))

f = plt.figure(figsize=(15,7), dpi = 100) #creates the matplotlib figure
ax1 = f.add_subplot(211) #adds the top plot (full time and partial time plots)
ax2 = f.add_subplot(212) #adds the top plot (full time and partial time plots)

ax1.plot(df['Time'][low:high], df['TEG1'][low:high], 'ro')
ax1.plot(df['Time'][low:high], df['TEG1'][low:high], 'b-', label = 'TEG1')
ax2.plot(df['Time'][low:high], df['Current'][low:high], 'ro')
ax2.plot(df['Time'][low:high], df['Current'][low:high], 'y-', label = 'Current')
ax1.plot(df['Time'][low:high], df['TEG2'][low:high], 'ro')
ax1.plot(df['Time'][low:high], df['TEG2'][low:high], 'g-', label = 'TEG2')
ax2.plot(df['Time'][low:high], df['Supply_voltage'][low:high], 'ro')
ax2.plot(df['Time'][low:high], df['Supply_voltage'][low:high], 'p-', label = 'Supply voltage')
ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))