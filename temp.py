import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('C:/Users/jmajor/Desktop/github/Battery_cal_/Data/Set filename Feb 22 2019, time_00_31_10.csv')

#df.plot(x = 'Time')

teg1 = df['TEG1']
teg2 = df['TEG2']

supply_voltage = df['Supply_voltage']
cell_voltage = df['Cell_voltage']


plt.plot(teg1)
plt.plot(teg2)
plt.plot(supply_voltage)
plt.plot(cell_voltage)

plt.show()
