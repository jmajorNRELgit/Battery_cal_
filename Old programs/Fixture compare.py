import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df1 = pd.read_csv('C:/Users/jmajor/Desktop/github/Battery_cal_/Calibration data/Condensed raw data/Bldg 16 calibration.csv')

df1 = df1[5800:]

df2 = pd.read_csv('C:/Users/jmajor/Desktop/github/Battery_cal_/Calibration data/Condensed raw data/Rad Cal calibration shakedown.csv')

#data from calibration
TEG1 = list(df1['TEG1'])
TEG2 = list(df1['TEG2'])
current = list(df1['Current'])
supply_voltage = list(df1['Supply_voltage'])
cell_voltage = list(df1['Cell_voltage'])

TEG_sum = []
for i in range(len(TEG1)):
    TEG_sum.append((TEG1[i] + TEG2[i])+.00015)


power = []
for i in range(len(supply_voltage)):
    power.append((supply_voltage[i] * current[i])+.01)




#data from calibration
rad_TEG1 = list(df2['TEG1'])
rad_TEG2 = list(df2['TEG2'])
rad_current = list(df2['Current'])
rad_supply_voltage = list(df2['Supply_voltage'])
rad_cell_voltage = list(df2['Cell_voltage'])

rad_TEG_sum = []
for i in range(len(rad_TEG1)):
    rad_TEG_sum.append(rad_TEG1[i] + rad_TEG2[i])

rad_power = []
for i in range(len(rad_supply_voltage)):
    rad_power.append(rad_supply_voltage[i] * rad_current[i])


fig = plt.figure(figsize = (12,8))

ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212, sharex = ax1)

ax1.plot(rad_TEG_sum, 'bo-', label = 'RAD TEG sum')
ax1.plot(TEG_sum, 'o-', label = 'BATH TEG sum')

ax2.plot(rad_power, 'bo-', label = 'Rad cal power' )
ax2.plot(power, 'o-', label = 'Bath power' )

ax1.scatter(7789, rad_TEG_sum[7789], s=600, c = 'r', marker='+', )
ax1.scatter(7086, rad_TEG_sum[7086], s=600, c = 'r', marker='+', )

ax1.scatter(11019, TEG_sum[11019], s=600, c = 'r', marker='+', )
ax1.scatter(10571, TEG_sum[10571], s=600, c = 'r', marker='+', )


ax1.legend(loc='center left', bbox_to_anchor=(1.1, 0.6))
ax2.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))

fig.tight_layout()


print('\nRAD STD at top of high power pulse (500 dp): ', str(np.std(rad_TEG_sum[5200:5400])))
print('BATH STD at top of high power pulse (500 dp): ', str(np.std(TEG_sum[7400:7900])))

print('\nRAD P2P at equlibrium (2000 dp): ', str(max(rad_TEG_sum[6500:8500]) - min(rad_TEG_sum[6500:8500])))
print('Bath P2P at equlibrium (2000 dp): ', str(max(TEG_sum[9500:11200]) - min(TEG_sum[9500:11200])))


for i in range(9500,11200):
    if TEG_sum[i] == max(TEG_sum[9500:11200]):
        print(i)
        break
