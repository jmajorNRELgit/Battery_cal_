# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 12:12:49 2019

@author: jmajor
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import pandas as pd
from scipy import signal
from scipy import stats
from operator import mul
import scipy
#
#file =  'C:/Users/jmajor/Desktop/github/Battery_cal_/Calibration data/Condensed raw data/Rad Cal calibration shakedown_full_data.csv'

#file = 'C:/Users/jmajor/Desktop/github/Battery_cal_/Calibration data/Condensed raw data/Rad Cal calibration shakedown.csv'

file = 'C:/Users/jmajor/Desktop/github/Battery_cal_/Calibration data/Condensed raw data/Bldg 16 calibration.csv'

df = pd.read_csv(file)

#df = df[14000:15000]

#data from calibration
TEG1 = df['TEG1']
TEG2 = df['TEG2']
current = df['Current']
supply_voltage = df['Supply_voltage']
cell_voltage = df['Cell_voltage']

#def TEG_abs(TEG):
#    TEG_min = min(TEG)
#    if TEG_min < 0:
#        TEG = [i + (-1*TEG_min) for i in TEG]
#
#    return TEG
#
#TEG1 = TEG_abs(TEG1)
#TEG2 = TEG_abs(TEG2)

#addition of the two TEGs
TEG_sum = []
for i in range(len(TEG1)):
    TEG_sum.append(TEG1[i] + TEG2[i])

#TEG_sum = scipy.signal.medfilt(TEG_sum,51)


#figures and plots
f = plt.figure(figsize=(12, 8))
ax1 = f.add_subplot(211)
ax2 = f.add_subplot(212)

x = list(range(len(TEG1)))

ax1.plot(x, TEG_sum, label = 'TEG Sum')
ax1.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))
ax1.set_title('Press left mouse button and drag to test')

line2, = ax2.plot(x, TEG_sum, label = 'TEG average')

ax3 = ax2.twinx()
ax3.plot(x, supply_voltage, 'r', label = 'Supply Voltage')

ax2.legend(loc='center left', bbox_to_anchor=(1.1, 0.6))
ax3.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))

f.tight_layout()





#data collected from the plot
data_dictionaries = []


def onselect(xmin, xmax):
    global data_dictionaries
    x_data = None
    TEG_sum_data = None
    supply_voltage_data = None
    supply_current_data = None



    indmin, indmax = np.searchsorted(x, (xmin, xmax))
    indmax = min(len(x) - 1, indmax)

    x_data = x[indmin:indmax]
    TEG_sum_data = TEG_sum[indmin:indmax]
    supply_voltage_data = supply_voltage[indmin:indmax]
    supply_current_data = current[indmin:indmax]

    data_dictionaries.append({'X_data': x_data, 'TEG_sum_data': TEG_sum_data, 'Supply_voltage_data':  supply_voltage_data, 'Supply_current_data':  supply_current_data, 'Power': supply_voltage_data*supply_current_data })

    line2.set_data(x_data, TEG_sum_data)
    f.canvas.draw_idle()

    # save
    #np.savetxt("text.out", np.c_[thisx, thisy])

# set useblit True on gtkagg for enhanced performance
span = SpanSelector(ax1, onselect, 'horizontal', useblit=True,
                    rectprops=dict(alpha=0.5, facecolor='red'))

plt.show(block = True)





#get data averages
for data in data_dictionaries:
   data['TEG_sum_data'] = np.mean(data['TEG_sum_data'])
   data['X_data'] = np.mean(data['X_data'])
   data['Power'] = np.mean(data['Power'])






'''finding coeffiecients'''
cof = np.polyfit([data['TEG_sum_data'] for data in data_dictionaries], [data['Power'] for data in data_dictionaries], 1)
fit = np.poly1d(cof)

'''fitting the data'''
fit_data = [fit(i) for i in [data['TEG_sum_data'] for data in data_dictionaries]]
slope, intercept, r_value, p_value, std_err = stats.linregress([data['Power'] for data in data_dictionaries], fit_data)





print('y = {0}*x + {1}'.format(cof[0], cof[1]))
print('R^2 = {}'.format(r_value))

power = list(map(mul, supply_voltage, current))
fitted_TEG_data = [fit(i) for i in TEG_sum]
#yhat1 = savgol_filter(fitted_TEG_data, 31, 1) # window size 51, polynomial order 3
#yhat1 = scipy.signal.medfilt(fitted_TEG_data, 51)

plt.plot(power, 'o-', label = 'Power (W)')
plt.plot(fitted_TEG_data, label = 'Fitted TEG data')
#plt.plot(yhat1,  label = 'Smoothed TE data')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()


df2 = {'Power' : power, 'TEG_data': fitted_TEG_data}

df2 = pd.DataFrame(df2)

#df2.to_csv('data/bldg 16 calibrated data for integration.csv', index = False)

plt.plot(TEG1)
plt.plot(TEG2)
