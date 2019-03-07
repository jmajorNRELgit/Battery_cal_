# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 07:49:51 2019

@author: jmajor
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
from scipy import signal

file = 'C:/Users/jmajor/Desktop/github/Battery_cal_/manually_saved_data/rad_cal_shakedown_1 Mar 05 2019, 09_29_46.csv'


df = pd.read_csv(file)

#df = df[8300:25000]




#df.to_csv('data/Rad Cal calibration shakedown.csv', index = False)



TEG1 = list(df['TEG1'])
TEG2 = list(df['TEG2'])
times = list(df['Time'])
current = list(df['Current'])

supply_voltage = df['Supply_voltage']
cell_voltage = df['Cell_voltage']


#yhat1 = savgol_filter(TEG1, 79, 1) # window size 51, polynomial order 3
#yhat2 = savgol_filter(TEG2, 79, 1) # window size 51, polynomial order 3


f = plt.figure(figsize=(15,7), dpi = 100) #creates the matplotlib figure
ax1 = f.add_subplot(311) #adds the top plot (full time and partial time plots)
ax2 = f.add_subplot(312) #adds the top plot (full time and partial time plots)
ax3 = f.add_subplot(313) #adds the top plot (full time and partial time plots)

ax1.plot(TEG1, label = 'TEG1' )
#ax1.plot(yhat1, label = 'TEG1 smoothed')
ax1.plot(TEG2, label = 'TEG2' )
#ax1.plot(yhat2, label = 'TEG2 smoothed')


ax2.plot(supply_voltage, 'bo-', label = 'Supply voltage')
ax2.plot(cell_voltage, 'ro-', label = 'Cell voltage')

ax3.plot(current, 'bo-', label = 'Supply current')


ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax3.legend(loc='center left', bbox_to_anchor=(1, 0.5))

f.tight_layout()

TEG3 = [i + 3.6462e-05 for i in TEG1]

ax1.plot(TEG3)

#ax1.plot(signal.medfilt(TEG3,51))


