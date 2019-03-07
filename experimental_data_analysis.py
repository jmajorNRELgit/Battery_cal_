import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

#first weekend test with power outage
#file = 'C:/Users/jmajor/Desktop/github/Battery_cal_/Experimental data/Weekend_DC_test_31-1-19.csv'

#first test of the rad_setup. No TEG coolers at first
#file = 'C:/Users/jmajor/Desktop/github/Battery_cal_/Data/Radation_POC_fixture_1 Mar 04 2019, 15_10_13.csv'


#first rad cal overnight calibration test
#file = 'C:/Users/jmajor/Desktop/github/Battery_cal_/manually_saved_data/rad_cal_shakedown_1 Mar 05 2019, 09_29_46.csv'


# first bath, overnight, dc tests
#file = 'C:/Users/jmajor/Desktop/github/Battery_cal_/Experimental data/DC_pulse_overnight_1 Mar 05 2019, 11_03_10.csv'

# second bath, overnight, dc test
#file = 'C:/Users/jmajor/Desktop/github/Battery_cal_/Experimental data/DC_pulse_overnight_2 Mar 06 2019, 08_11_32.csv'

file = 'C:/Users/jmajor/Desktop/github/Battery_cal_/manually_saved_data/rad_cal_shakedown_1 Mar 05 2019, 09_29_46.csv'

df = pd.read_csv(file)
#df = df[8300:25000]
df.reset_index(inplace = True, drop = True)

#data from calibration
TEG1 = df['TEG1']
TEG2 = df['TEG2']
current = df['Current']
supply_voltage = df['Supply_voltage']
cell_voltage = df['Cell_voltage']
TEG_sum = []
power = []
time = df['Time']

#def TEG_abs(TEG):
#    TEG_min = min(TEG)
#    if TEG_min < 0:
#        TEG = [i + (-1*TEG_min) for i in TEG]
#
#    return TEG
#
#TEG1 = TEG_abs(TEG1)
#TEG2 = TEG_abs(TEG2)


for i in range(len(TEG1)):
    TEG_sum.append(TEG1[i] + TEG2[i])

for i in range(len(supply_voltage)):
    power.append(supply_voltage[i] * current[i])

teg1 = [(i * 8.122633691185543) for i in TEG_sum]






fig = plt.figure(figsize=(12, 8))

ax1 = fig.add_subplot(411)
ax2 = fig.add_subplot(412, sharex = ax1)
ax3 = fig.add_subplot(413, sharex = ax1)
ax4 = fig.add_subplot(414, sharex = ax1)

#ax1.plot(time,TEG1, label = 'TEG 1')
#ax1.plot(time,TEG2, label = 'TEG 2')
ax1.plot(time, TEG_sum, label = 'TEG sum')
ax2.plot(time,power, label = 'Power')
#ax2.plot(time,teg1, label = 'Fit TEG data')
ax3.plot(time,supply_voltage, label = 'Supply voltage')
ax4.plot(time,current, label = 'Current')

ax1.set_xlabel('Time')
ax2.set_xlabel('Time')
ax3.set_xlabel('Time')
ax4.set_xlabel('Time')


ax1.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))
ax2.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))
ax3.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))
ax4.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))

plt.subplots_adjust(left=None, bottom=.9, right=None, top=1, wspace=None, hspace=None)

plt.tight_layout()