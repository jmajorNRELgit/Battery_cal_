# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 07:49:51 2019

@author: jmajor
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('Overnight voltage and ground test_1_31_19.csv')

time = df['Time']
voltage = df['Voltage']
ground = df['Ground']


plt.plot(time, voltage, 'ro')
plt.plot(time, voltage, 'b-')
plt.plot(time, ground, 'ro')
plt.plot(time, ground, 'g-')
plt.show()

base_std = np.std(ground)
