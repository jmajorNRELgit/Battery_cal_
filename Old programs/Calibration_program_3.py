# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 09:52:07 2019

@author: jmajor
"""

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
import time
import pandas as pd
import threading
import visa
import numpy as np
import matplotlib.pyplot as plt
from numpy import random


import psutil

dry_run = 0



'''
Enter calibration parameters here
'''
#####################################################
initial_sleep = 10
voltages_to_test = [1, 1.5, 2]
durations_of_tests_in_seconds = [10,10,10]
duration_of_sleep_after_tests_in_seconds = [10,10,10]
#####################################################







stop = 0

def animate(i):

    TEG1 = app.TEG1
    currents = app.currents
    TEG2 = app.TEG2
    supply_voltage = app.supply_voltage

    min_list_length = min([len(app.TEG2), len(app.TEG1), len(app.times), len(app.cell_voltage), len(app.supply_voltage)])
    TEG2 = app.TEG2[:min_list_length]
    TEG1 = app.TEG1[:min_list_length]
    currents = app.currents[:min_list_length]
    cell_voltage = app.cell_voltage[:min_list_length]
    supply_voltage = app.supply_voltage[:min_list_length]

    zoom_level = -80

    app.ax1.clear()
    app.ax2.clear()
    app.ax3.clear()


    if app.zoom1 == 0:


        app.ax1.plot(TEG1, 'bo-', label = 'TEG1')
        app.ax3.plot( currents, 'yo-', label = 'Current')
        app.ax1.plot( TEG2, 'go-', label = 'TEG2')
        app.ax2.plot( supply_voltage, 'ro-', label = 'Supply voltage')
        app.ax2.plot(cell_voltage, 'bo-', label = 'Cell voltage')
        app.ax2.plot()

    else:

        app.ax1.plot(TEG1[zoom_level:], 'bo-', label = 'TEG1')
        app.ax3.plot(currents[zoom_level:], 'yo-', label = 'Current')
        app.ax1.plot(TEG2[zoom_level:], 'go-', label = 'TEG2')
        app.ax2.plot(supply_voltage[zoom_level:], 'ro-', label = 'Supply voltage')
        app.ax2.plot(cell_voltage[zoom_level:], 'bo-', label = 'Cell voltage')



    app.ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    app.ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    app.ax3.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    app.f.tight_layout()



class TIM(tk.Tk):

    f = Figure(figsize=(10,7), dpi = 100) #creates the matplotlib figure
    ax1 = f.add_subplot(311) #adds the top plot (full time and partial time plots)
    ax2 = f.add_subplot(312) #adds the top plot (full time and partial time plots)
    ax3 = f.add_subplot(313) #adds the top plot (full time and partial time plots)


    def __init__(self, volts,duration,sleep, initia_sleep, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)


        self.voltages_to_test = volts
        self.durations_of_tests_in_seconds = duration
        self.duration_of_sleep_after_tests_in_seconds = sleep
        self.initial_sleep = initial_sleep

        self.graph_frame()
        self.button_frame()

        self.start = time.time()
        self.TEG1 = []
        self.supply_voltage = []
        self.cell_voltage = []
        self.TEG2 = []
        self.currents = []
        self.times = []

        self.ram = []


        self.zoom1 = 0

        self.resolution = .0000001


        if dry_run == 0:
            self.name = 'HEWLETT-PACKARD,34970A,0,13-2-2\n'
            self.rm = visa.ResourceManager()
            self.DAQ = self.rm.open_resource('GPIB0::3::INSTR')

            #check if connection is made
            if self.DAQ.query('*IDN?') == self.name:
                print('Communication established with Keysight DAQ')

            else:
                print('Communication FAILED with Keysight DAQ')


            self.power_supply = self.rm.open_resource('GPIB0::4::INSTR')

        else:
            print('it works')


        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start(  )


    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O.
        """
        global stop
        global dry_run
        pri = 0

        while stop == 0:

            if dry_run == 0:

                self.TEG1.append(float(self.DAQ.query('MEAS:volt:dc? 0.1, {0}, (@101)'.format(self.resolution))))
                self.supply_voltage.append(float(self.DAQ.query('MEAS:volt:dc? AUTO, (@103)'.format(self.resolution))))
                self.cell_voltage.append(float(self.DAQ.query('MEAS:volt:dc? AUTO, (@104)'.format(self.resolution))))
                self.TEG2.append(float(self.DAQ.query('MEAS:volt:dc? 0.1, {0}, (@102)'.format(self.resolution))))
                self.currents.append(float(self.DAQ.query('MEAS:curr:dc? AUTO, (@122)')))

                self.times.append(time.time() - self.start)

                self.ram.append(psutil.virtual_memory()[1])


            else:
                self.TEG1.append(self.random_data())
                self.supply_voltage.append(self.random_data())
                self.TEG2.append(self.random_data())
                self.currents.append(self.random_data())
                self.times.append(time.time() - self.start)
                self.cell_voltage.append(self.random_data())

                self.ram.append(psutil.virtual_memory()[1])
                time.sleep(1)

            if len(self.TEG1) % 5000 == 0:
                self.save_data()

                self.TEG1 = []
                self.supply_voltage = []
                self.TEG2 = []
                self.currents = []
                self.times = []
                self.cell_voltage = []


            if dry_run == 0:
                if pri == 0:
                    print('Voltage NPLC: ' + self.DAQ.query('SENS:VOLT:DC:NPLC?  (@101,102,103,104)'))
                    print('Current NPLC: ' + self.DAQ.query('SENS:current:DC:NPLC?  (@122)'))
                    pri = 1



    def graph_frame(self):
        frame1 = tk.Frame(self,width=100, height=200)
        frame1.grid(row=0,column=0)

        canvas = FigureCanvasTkAgg(self.f, frame1)
        canvas.get_tk_widget().grid(row = 2, column = 0)



    def button_frame(self):

        frame2 = tk.Frame(self,width=100, height=200, borderwidth=10)
        frame2.grid(row=0, column = 1)

        graph_one_zoom_button = ttk.Button(frame2, text = 'Zoom graph', command = self.zoom_graph)
        graph_one_zoom_button.grid(row = 0, column = 0)


        save_button = ttk.Button(frame2, text = 'Save data', command = self.save_data)
        save_button.grid(row = 1, column = 0)

        text_field = tk.StringVar(frame2, value='Set filename')
        self.text_box = tk.Entry(frame2,textvariable=text_field)
        self.text_box.grid(row=1, column = 1)
        self.text_box.focus_set()


        supply_pulse_button = ttk.Button(frame2, text = 'Start calibration', command = self.power_supply_pulse)
        supply_pulse_button.grid(row = 6, column = 0)

    def power_supply_pulse(self):



        def pulse_thread_function():

            print('Started test. Initial sleep for {} seconds'.format(str(self.initial_sleep)))

            for i in range(initial_sleep):
                if i % 10 == 0:
                    print(str(initial_sleep - i))
                time.sleep(1)

            for i in range(len(self.voltages_to_test)):


                print('Power on')
                self.power_supply.write('APPL P25V, {0}, 1.0'.format(self.voltages_to_test[i]))
                self.power_supply.write('output:state on')
                time.sleep(self.durations_of_tests_in_seconds[i])
                self.power_supply.write('APPL P25V, {0}, 1.0'.format(0))
                self.power_supply.write('output:state off')
                print('Power off')
                time.sleep(self.duration_of_sleep_after_tests_in_seconds[i])
                self.save_data(path = 'home_cal_data')

        self.pulse_thread = threading.Thread(target= pulse_thread_function)
        self.pulse_thread.start(  )


    def zoom_graph(self):
        if self.zoom1 == 0:
            self.zoom1 = 1
        else:
            self.zoom1 = 0




    def save_data(self, path = None):

        if path == None:
            path = 'data'
        else:
            path = path


        min_list_length = min([len(app.TEG2), len(app.TEG1), len(app.times), len(app.cell_voltage), len(app.supply_voltage)])
        TEG2 = app.TEG2[:min_list_length]
        TEG1 = app.TEG1[:min_list_length]
        currents = app.currents[:min_list_length]
        cell_voltage = app.cell_voltage[:min_list_length]
        times = app.times[:min_list_length]
        supply_voltage = app.supply_voltage[:min_list_length]

        data = {'Time': times, 'Current': currents, 'TEG2': TEG2, 'TEG1': TEG1, 'Supply_voltage' : supply_voltage, 'Cell_voltage': cell_voltage }

        df = pd.DataFrame(data)

        file_time = time.strftime("%b %d %Y, time_%H_%M_%S")
        file = self.text_box.get()
        print('{0} {1}.csv'.format(file, file_time))

        df.to_csv('{0}/{1} {2}.csv'.format(path, file,  file_time), index = None)

    def random_data(self):
        return random.randint(1,30)







app = TIM(voltages_to_test, durations_of_tests_in_seconds, duration_of_sleep_after_tests_in_seconds, initial_sleep)

ani = animation.FuncAnimation(app.f,animate, interval = 1000)

app.mainloop()

stop = 1

#app.inst.close()


min_list_length = min([len(app.TEG2), len(app.TEG1), len(app.times), len(app.cell_voltage), len(app.supply_voltage)])
TEG2 = app.TEG2[:min_list_length]
TEG1 = app.TEG1[:min_list_length]
currents = app.currents[:min_list_length]
cell_voltage = app.cell_voltage[:min_list_length]
times = app.times[:min_list_length]
supply_voltage = app.supply_voltage[:min_list_length]

data = {'Time': times, 'Current': currents, 'TEG2': TEG2, 'TEG1': TEG1, 'Supply_voltage' : supply_voltage, 'Cell_voltage': cell_voltage }

df = pd.DataFrame(data)

print('Seconds per sample: ' + str(float( df['Time'][-1:]/len(df['TEG1']))))

f = plt.figure(figsize=(15,7), dpi = 100) #creates the matplotlib figure
ax1 = f.add_subplot(311) #adds the top plot (full time and partial time plots)
ax2 = f.add_subplot(312) #adds the top plot (full time and partial time plots)
ax3 = f.add_subplot(313) #adds the top plot (full time and partial time plots)


ax1.plot(times, TEG1, 'bo-', label = 'TEG1')
ax1.plot(times, TEG2, 'go-', label = 'TEG2')
ax2.plot(times, supply_voltage, 'ro-', label = 'Supply voltage')
ax2.plot(times, cell_voltage, 'bo-', label = 'Cell voltage')
ax3.plot(times, currents, 'yo-', label = 'Current')

ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax3.legend(loc='center left', bbox_to_anchor=(1, 0.5))


