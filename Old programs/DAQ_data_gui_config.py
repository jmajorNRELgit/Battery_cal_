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
    app.ax1.plot(times,volts, 'b-')
    app.ax1.plot(times, currents, 'ro')
    app.ax1.plot(times, currents, 'y-')
    app.ax1.plot(times, ground, 'ro')
    app.ax1.plot(times, ground, 'g-')



class TIM(tk.Tk):

    x_start = time.time() #used to create the x-axis values

    temp_list = [] #list that the worker thread uses to calculate STD

    f = Figure(figsize=(10,5), dpi = 100) #creates the matplotlib figure
    ax1 = f.add_subplot(111) #adds the top plot (full time and partial time plots)

    zoom1 = 0 #class variable to control the zoom in funtionality of plot app.ax1
    zoom2 = 0 #class variable to control the zoom in funtionality of plot app.ax1

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
                time.sleep(2)
                self.pause = 0
            self.inst.write('CONF:VOLT:DC (@101)')
            self.volts.append(float(self.inst.query('READ?')))
            self.inst.write('CONF:VOLT:DC (@102)')
            self.ground.append(float(self.inst.query('READ?')))
            self.currents.append(float(self.inst.query('MEAS:curr:dc? min, (@122)')))
            self.times.append(time.time() - self.start)

            if pri == 0:
                print('NPLC: ' + self.inst.query('SENS:VOLTage:DC:NPLC?  (@101,102)'))
                pri = 1



    def graph_frame(self):
        frame1 = tk.Frame(self,width=100, height=200)
        frame1.grid(row=0,column=0)

        canvas = FigureCanvasTkAgg(self.f, frame1)
        canvas.get_tk_widget().grid(row = 2, column = 0)

        button1 = ttk.Button(frame1, text = 'Resolution', command = self.change_resolution)
        button1.grid(row = 1, column = 0)

    def change_resolution(self):
        self.pause = 1
        print('Paused')
        time.sleep(1)
        print('unpaused')
        if self.resolution == .0000001:
            self.resolution = .000001
            print('NPLC: ' + self.inst.query('SENS:VOLTage:DC:NPLC?  (@101,102)'))

        else:
            self.resolution = .0000001
            print('NPLC: ' + self.inst.query('SENS:VOLTage:DC:NPLC?  (@101,102)'))


app = TIM()
ani = animation.FuncAnimation(app.f,animate, interval = 1000)

app.mainloop()

stop = 1

data = {'Time': app.times, 'Current': app.currents, 'Ground': app.ground, 'Voltage': app.volts}

df = pd.DataFrame(data)
df.plot(x = 'Time')
#df.to_csv('Touch_test_1_resolution 6.5.csv', index = None)
