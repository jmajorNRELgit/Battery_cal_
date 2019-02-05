# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 18:00:31 2019

@author: jmajor
"""

import visa
import time
import matplotlib.pyplot as plt



rm = visa.ResourceManager()

inst = rm.open_resource('GPIB0::4::INSTR')


inst.write('APPL P25V, 25.0, 1.0')
inst.write('APPL N25V, -25.0, 1.0')
inst.write('output:state on')

voltage = []
current = []

start = time.time()
for i in range(20):
    voltage.append(inst.query('meas:volt:dc? p25v'))
    current.append(inst.query('meas:current:dc? p25v'))

    print('Voltage : ' + voltage[-1])
    print('Current: ' + current[-1])
    time.sleep(.5)

voltage = list(map(float, voltage))
current = list(map(float, current))

finish = time.time() - start
inst.write('output:state off')
print(finish)

f = plt.figure(figsize=(10,5), dpi = 100) #creates the matplotlib figure
ax1 = f.add_subplot(211) #adds the top plot (full time and partial time plots)
ax2 = f.add_subplot(212) #STD plot

ax1.plot(voltage, 'ro')
ax1.plot(voltage)

ax2.plot(current, 'ro')
ax2.plot(current)