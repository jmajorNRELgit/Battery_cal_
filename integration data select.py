'''Integration data select'''

import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import pandas as pd
import numpy as np
from scipy import signal

#calibration
#file = 'C:/Users/jmajor/Desktop/github/Battery_cal_/Calibration data/Condensed raw data/Bldg 16 calibration.csv'

#first overnight test
file = 'C:/Users/jmajor/Desktop/github/Battery_cal_/Experimental data/overnight_test Mar 05 2019, 11_03_10.csv'

calibration_slope = 8.113447
calibration_intercept = -0.0002121


df = pd.read_csv(file)

#data from calibration
TEG1 = df['TEG1']
TEG2 = df['TEG2']
current = df['Current']
supply_voltage = df['Supply_voltage']
cell_voltage = df['Cell_voltage']
time = df['Time']

TEG_sum = []
for i in range(len(TEG1)):
    TEG_sum.append(TEG1[i] + TEG2[i])

TEG_fitted = [(i*calibration_slope+calibration_intercept) for i in TEG_sum]





power = []
for i in range(len(supply_voltage)):
    power.append(supply_voltage[i] * current[i])


#TEG_fitted = power


#figures and plots
f = plt.figure(figsize=(12, 8))
ax1 = f.add_subplot(111)




x = list(range(len(TEG_sum)))

ax1.plot(x, TEG_fitted, label = 'Fitted TEG data')
ax1.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))
ax1.set_title('Press left mouse button and drag to test')



f.tight_layout()


#data collected from the plot
data_lists = []


def onselect(xmin, xmax):
    global data_dictionaries
    x_data = None

    indmin, indmax = np.searchsorted(x, (xmin, xmax))
    indmax = min(len(x) - 1, indmax)

    x_data = x[indmin:indmax]
    TEG_data_to_integrate = TEG_fitted[indmin:indmax]

    integration_time = time[indmin:indmax]

    min_data = min(TEG_data_to_integrate)

    if min_data < 0:
        TEG_data_to_integrate = [i + (min_data*-1) for i in TEG_data_to_integrate]

    else:
        TEG_data_to_integrate = [i - min_data for i in TEG_data_to_integrate]


    data_lists.append((x_data, TEG_data_to_integrate, integration_time))


# set useblit True on gtkagg for enhanced performance
span = SpanSelector(ax1, onselect, 'horizontal', useblit=True,
                    rectprops=dict(alpha=0.5, facecolor='red'))

plt.show(block = True)

for i in range(len(data_lists)):
    plt.fill_between(data_lists[i][2],[0]*len(data_lists[i][0]), data_lists[i][1])

for i in range(len(data_lists)):
    print('Area {}: {}'.format(i+1, np.trapz(data_lists[i][1]) / (data_lists[i][2][-1:] - data_lists[i][2][0:1]) ))


#TEG                          Power
#Area 1: 1.2773989371499532   Area 1: 1.1824694969290674
#Area 2: 1.6473845785478214   Area 2: 1.5637378081802868
#Area 3: 2.3018776749395515   Area 3: 2.2638601973365162
#Area 4: 7.398267892010971    Area 4: 7.456473500905397
#Area 5: 12.486453677887733   Area 5: 12.483297254283066
#Area 6: 0.01237235354251649  Area 6: 0.018648658727085297
#Area 7: 0.08752071828919303  Area 7: 0.0612968801043543
#Area 8: 0.11369527030920656  Area 8: 0.09769241974977154









