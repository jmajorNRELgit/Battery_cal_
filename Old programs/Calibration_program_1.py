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


stop = 0


def animate(i):

    times = app.times
    TEG1 = app.TEG1
    currents = app.currents
    TEG2 = app.TEG2
    supply_voltage = app.supply_voltage

    min_list_length = min([len(TEG2), len(TEG1), len(times)])
    TEG2 = TEG2[:min_list_length]
    TEG1 = TEG1[:min_list_length]
    currents = currents[:min_list_length]
    times = times[:min_list_length]
    supply_voltage = supply_voltage[:min_list_length]

    zoom_level = -50

    app.ax1.clear()
    app.ax2.clear()

    if app.zoom1 == 0:


        app.ax1.plot(times,TEG1, 'bo-', label = 'TEG1')

        app.ax2.plot(times, currents, 'yo-', label = 'Current')

        app.ax1.plot(times, TEG2, 'go-', label = 'TEG2')

        app.ax2.plot(times, supply_voltage, 'po-', label = 'Supply voltage')

    else:

        app.ax1.plot(times[zoom_level:],TEG1[zoom_level:], 'bo-', label = 'TEG1')

        app.ax2.plot(times[zoom_level:], currents[zoom_level:], 'yo-', label = 'Current')

        app.ax1.plot(times[zoom_level:], TEG2[zoom_level:], 'go-', label = 'TEG2')

        app.ax2.plot(times[zoom_level:], supply_voltage[zoom_level:], 'po-', label = 'Supply voltage')



    app.ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    app.ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    app.f.tight_layout()



class TIM(tk.Tk):

    f = Figure(figsize=(10,7), dpi = 100) #creates the matplotlib figure
    ax1 = f.add_subplot(211) #adds the top plot (full time and partial time plots)
    ax2 = f.add_subplot(212) #adds the top plot (full time and partial time plots)


    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.graph_frame()
        self.button_frame()

        self.start = time.time()
        self.TEG1 = []
        self.supply_voltage = []
        self.TEG2 = []
        self.currents = []
        self.times = []

        self.zoom1 = 0

        self.resolution = .0000001
        self.pause = 0


        self.name = 'HEWLETT-PACKARD,34970A,0,13-2-2\n'
        self.rm = visa.ResourceManager()
        self.DAQ = self.rm.open_resource('GPIB0::3::INSTR')

        #check if connection is made
        if self.DAQ.query('*IDN?') == self.name:
            print('Communication established with Keysight DAQ')

        else:
            print('Communication FAILED with Keysight DAQ')


        self.power_supply = self.rm.open_resource('GPIB3::2::INSTR')


        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start(  )


    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O.
        """
        global stop
        pri = 0

        while stop == 0:

            if self.pause == 1:
                time.sleep(1)


            self.TEG1.append(float(self.DAQ.query('MEAS:volt:dc? 0.1, {0}, (@101)'.format(self.resolution))))
            self.supply_voltage.append(float(self.DAQ.query('MEAS:volt:dc? AUTO, (@103)'.format(self.resolution))))
            self.TEG2.append(float(self.DAQ.query('MEAS:volt:dc? 0.1, {0}, (@102)'.format(self.resolution))))
            self.currents.append(float(self.DAQ.query('MEAS:curr:dc? AUTO, (@122)')))
            self.times.append(time.time() - self.start)

            if pri == 0:
                print('Voltage NPLC: ' + self.DAQ.query('SENS:VOLT:DC:NPLC?  (@101,102,103)'))
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

        resolution_button = ttk.Button(frame2, text = 'Resolution', command = self.change_resolution)
        resolution_button.grid(row = 0, column = 1)

        save_button = ttk.Button(frame2, text = 'Save data', command = self.save_data)
        save_button.grid(row = 1, column = 0)

        text_field = tk.StringVar(frame2, value='Set filename')
        self.text_box = tk.Entry(frame2,textvariable=text_field)
        self.text_box.grid(row=1, column = 1)
        self.text_box.focus_set()

        spacer = ttk.Label(frame2, text = '' )
        spacer.grid(row = 2, column = 0)
        spacer2 = ttk.Label(frame2, text = '' )
        spacer2.grid(row = 3, column = 0)

        supply_voltage_label = ttk.Label(frame2, text = 'Set supply voltage (V): ' )
        supply_voltage_label.grid(row = 4, column = 0)

        supply_voltage_text_field = tk.StringVar(frame2, value='1')
        self.supply_voltage_text_box = tk.Entry(frame2,textvariable = supply_voltage_text_field)
        self.supply_voltage_text_box.grid(row=4, column = 1)
        self.supply_voltage_text_box.focus_set()

        supply_time_label = ttk.Label(frame2, text = 'Set pulse time (S): ' )
        supply_time_label.grid(row = 5, column = 0)

        supply_time_text_field = tk.StringVar(frame2, value='1')
        self.supply_time_text_box = tk.Entry(frame2,textvariable = supply_time_text_field)
        self.supply_time_text_box.grid(row=5, column = 1)
        self.supply_time_text_box.focus_set()

        supply_pulse_button = ttk.Button(frame2, text = 'Send power supply pulse', command = self.power_supply_pulse)
        supply_pulse_button.grid(row = 6, column = 0)

    def power_supply_pulse(self):

        pulse_voltage = float(self.supply_voltage_text_box.get())
        pulse_time = float(self.supply_time_text_box.get())
        print('Power supply on, {0} Volts, {1} second(s)'.format(pulse_voltage, pulse_time))

        def pulse_thread_function():

            print('Power on')

            sleep_time = 2*60*60

            print('Starting calibration run')
            for i in range(30):
                time.sleep(1)
                if i % 10 == 0:
                    print(30-i)

            print('Starting Calibration')
            #2V for 2 hours then two hour break
            self.power_supply.write('APPL P25V, .25, 1.0')
            self.power_supply.write('output:state on')
            time.sleep(sleep_time)
            self.power_supply.write('output:state off')
            self.save_data()
            print('Done')
            time.sleep(sleep_time)

            #3V for 2 hours then two hour break
            self.power_supply.write('APPL P25V, .5, 1.0')
            self.power_supply.write('output:state on')
            time.sleep(sleep_time)
            self.power_supply.write('output:state off')
            self.save_data()
            print('DOne')
            time.sleep(sleep_time)

            #4V for 2 hours then two hour break
            self.power_supply.write('APPL P25V, .75, 1.0')
            self.power_supply.write('output:state on')
            time.sleep(sleep_time)
            self.power_supply.write('output:state off')
            self.save_data()
            print('Done')
            time.sleep(sleep_time)


            self.power_supply.write('APPL P25V, 0, 1.0')
            self.power_supply.write('output:state off')
            print('Power off')

        self.pulse_thread = threading.Thread(target= pulse_thread_function)
        self.pulse_thread.start(  )


    def zoom_graph(self):
        if self.zoom1 == 0:
            self.zoom1 = 1
        else:
            self.zoom1 = 0



    def change_resolution(self):
        self.pause = 1
        print('Paused')
        time.sleep(1)
        print('unpaused')
        if self.resolution == .0000001:
            self.resolution = .000001
            print('NPLC: ' + self.DAQ.query('SENS:VOLT:DC:NPLC?  (@101,102,103)'))
            self.pause = 0

        else:
            self.resolution = .0000001
            print('NPLC: ' + self.DAQ.query('SENS:VOLT:DC:NPLC?  (@101,102,103)'))
            self.pause = 0

    def save_data(self):

        min_list_length = min([len(app.TEG2), len(app.TEG1), len(app.times), len(app.currents)])
        TEG2 = app.TEG2[:min_list_length]
        TEG1 = app.TEG1[:min_list_length]
        currents = app.currents[:min_list_length]
        times = app.times[:min_list_length]
        supply_voltage = app.supply_voltage[:min_list_length]

        data = {'Time': times, 'Current': currents, 'TEG2': TEG2, 'TEG1': TEG1, 'Supply_voltage' : supply_voltage}

        df = pd.DataFrame(data)

        file_time = time.strftime("%b %d %Y, time_%H_%M_%S")
        file = self.text_box.get()
        print('{0} {1}.csv'.format(file, file_time))

        df.to_csv('data/{0} {1}.csv'.format(file, file_time), index = None)







app = TIM()
ani = animation.FuncAnimation(app.f,animate, interval = 1000)

app.mainloop()

stop = 1

#app.inst.close()


min_list_length = min([len(app.TEG2), len(app.TEG1), len(app.times), len(app.supply_voltage)])
app.TEG2 = app.TEG2[:min_list_length]
app.TEG1 = app.TEG1[:min_list_length]
app.currents = app.currents[:min_list_length]
app.times = app.times[:min_list_length]
app.supply_voltage = app.supply_voltage[:min_list_length]



data = {'Time': app.times, 'Current': app.currents, 'TEG2': app.TEG2, 'TEG1': app.TEG1, 'Supply_voltage' : app.supply_voltage}

df = pd.DataFrame(data)
#df.plot(x = 'Time')
print('\n')
print('TEG1 STD: ' + str(np.std(df['TEG1'])))
print('TEG2 STD: ' + str(np.std(df['TEG2'])))
print('Current STD: ' + str(np.std(df['Current'])))
print('\n')
#print('TEG1 SNR: ' + str(np.abs(np.mean(df['TEG_voltage']) / np.std(df['TEG_voltage']))))
#print('TEG2 SNR: ' + str(np.abs(np.mean(df['TEG2']) / np.std(df['TEG2']))))
#print('Current SNR: ' + str(np.abs(np.mean(df['Current']) / np.std(df['Current']))))
#print('\n')
print('Seconds per sample: ' + str(float( df['Time'][-1:]/len(df['TEG1']))))

#f = plt.figure(figsize=(15,7), dpi = 100) #creates the matplotlib figure
#ax1 = f.add_subplot(211) #adds the top plot (full time and partial time plots)
#ax2 = f.add_subplot(212) #adds the top plot (full time and partial time plots)
#
#ax1.plot(app.times, app.TEG1, 'ro')
#ax1.plot(app.times, app.TEG1, 'b-', label = 'TEG1')
#ax2.plot(app.times, app.currents, 'ro')
#ax2.plot(app.times, app.currents, 'y-', label = 'Current')
#ax1.plot(app.times, app.TEG2, 'ro')
#ax1.plot(app.times, app.TEG2, 'g-', label = 'TEG2')
#ax2.plot(app.times, app.supply_voltage, 'ro')
#ax2.plot(app.times, app.supply_voltage, 'p-', label = 'Supply voltage')
#ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))

