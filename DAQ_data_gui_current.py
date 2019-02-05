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


stop = 0


def animate(i):

    times = app.times
    volts = app.volts
    currents = app.currents
    ground = app.ground

    min_list_length = min([len(ground), len(volts), len(times)])
    ground = ground[:min_list_length]
    volts = volts[:min_list_length]
    currents = currents[:min_list_length]
    times = times[:min_list_length]

    app.ax1.clear()
    app.ax1.plot(times,volts, 'ro')
    app.ax1.plot(times,volts, 'b-', label = 'Voltage')
    app.ax1.plot(times, currents, 'ro')
    app.ax1.plot(times, currents, 'y-', label = 'Current')
    app.ax1.plot(times, ground, 'ro')
    app.ax1.plot(times, ground, 'g-', label = 'Ground')
    app.ax1.legend()



class TIM(tk.Tk):

    f = Figure(figsize=(10,5), dpi = 100) #creates the matplotlib figure
    ax1 = f.add_subplot(111) #adds the top plot (full time and partial time plots)

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.graph_frame()

        self.start = time.time()
        self.volts = []
        self.ground = []
        self.currents = []
        self.times = []

        self.resolution = .0000001
        self.pause = 0


        self.name = 'HEWLETT-PACKARD,34970A,0,13-2-2\n'
        self.rm = visa.ResourceManager()
        self.inst = self.rm.open_resource('GPIB0::3::INSTR')

        #check if connection is made
        if self.inst.query('*IDN?') == self.name:
            print('Communication established with Keysight DAQ')

        else:
            print('Communication FAILED with Keysight DAQ')


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


            self.volts.append(float(self.inst.query('MEAS:volt:dc? 0.1, {0}, (@101)'.format(self.resolution))))
            self.ground.append(float(self.inst.query('MEAS:volt:dc? 0.1, {0}, (@102)'.format(self.resolution))))
            self.currents.append(float(self.inst.query('MEAS:curr:dc? .001, .00000001, (@122)')))
            self.times.append(time.time() - self.start)

            if pri == 0:
                print('NPLC: ' + self.inst.query('SENS:VOLTage:DC:NPLC?  (@101,102)'))
                pri = 1



    def graph_frame(self):
        frame1 = tk.Frame(self,width=100, height=200)
        frame1.grid(row=0,column=0)

        canvas = FigureCanvasTkAgg(self.f, frame1)
        canvas.get_tk_widget().grid(row = 2, column = 0)

        resolution_button = ttk.Button(frame1, text = 'Resolution', command = self.change_resolution)
        resolution_button.grid(row = 0, column = 1)

        save_button = ttk.Button(frame1, text = 'Save data', command = self.save_data)
        save_button.grid(row = 1, column = 1)

        text_field = tk.StringVar(frame1, value='Set filename')
        self.text_box = tk.Entry(frame1,textvariable=text_field)
        self.text_box.grid(row=1, column = 2)
        self.text_box.focus_set()



    def change_resolution(self):
        self.pause = 1
        print('Paused')
        time.sleep(1)
        print('unpaused')
        if self.resolution == .0000001:
            self.resolution = .000001
            print('NPLC: ' + self.inst.query('SENS:VOLTage:DC:NPLC?  (@101,102)'))
            self.pause = 0

        else:
            self.resolution = .0000001
            print('NPLC: ' + self.inst.query('SENS:VOLTage:DC:NPLC?  (@101,102)'))
            self.pause = 0

    def save_data(self):

        min_list_length = min([len(app.ground), len(app.volts), len(app.times)])
        app.ground = app.ground[:min_list_length]
        app.volts = app.volts[:min_list_length]
        app.currents = app.currents[:min_list_length]
        app.times = app.times[:min_list_length]

        data = {'Time': app.times, 'Current': app.currents, 'Ground': app.ground, 'Voltage': app.volts}

        df = pd.DataFrame(data)

        file_time = time.strftime("%b %d %Y, time_%H_%M_%S")
        file = self.text_box.get()
        print('{0} {1}.csv'.format(file, file_time))

        df.to_csv('data/{0} {1}.csv'.format(file, file_time), index = None)







app = TIM()
ani = animation.FuncAnimation(app.f,animate, interval = 1000)

app.mainloop()

stop = 1

app.inst.close()

min_list_length = min([len(app.ground), len(app.volts), len(app.times)])
app.ground = app.ground[:min_list_length]
app.volts = app.volts[:min_list_length]
app.currents = app.currents[:min_list_length]
app.times = app.times[:min_list_length]

data = {'Time': app.times, 'Current': app.currents, 'Ground': app.ground, 'Voltage': app.volts}

df = pd.DataFrame(data)
df.plot(x = 'Time')
print('\n')
print('TEG STD: ' + str(np.std(df['Voltage'])))
print('Ground STD: ' + str(np.std(df['Ground'])))
print('Current STD: ' + str(np.std(df['Current'])))
print('\n')
print('TEG SNR: ' + str(np.abs(np.mean(df['Voltage']) / np.std(df['Voltage']))))
print('Ground SNR: ' + str(np.abs(np.mean(df['Ground']) / np.std(df['Ground']))))
print('Current SNR: ' + str(np.abs(np.mean(df['Current']) / np.std(df['Current']))))
print('\n')
print('Samples per second: ' + str(float(len(df['Voltage']) / df['Time'][-1:])))
