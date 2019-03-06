# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 08:33:32 2019

@author: jmajor
"""

import serial

# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 09:52:07 2019

@author: jmajor

Simple daq data collection program with manually updated graph.

"""

daq_address = 'COM4'

voltage_type = 'dc'

stop = 0

dry_run = 0

auto_data_save_at_this_number_of_samples = 5000

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time
import pandas as pd
import threading
import visa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib import ticker



class TIM(tk.Tk):

    '''Initiate data variables. Start GUI threads and DAQ threads'''
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.start_time = time.time()

        self.time_stamp = []
        self.elapsed_time = []
        self.TEG1 = []
        self.TEG2 = []
        self.current = []
        self.supply_voltage = []
        self.cell_voltage = []


        self.graph_frame()
        self.button_frame()
        self.daq_establish_com()


        self.thread1 = threading.Thread(target=self.worker_thread_1)
        self.thread1.start(  )

    '''update the graph manually'''
    def update_graph(self):

        elapsed_time, TEG1, TEG2, current, supply_voltage, cell_voltage, time_stamp = self.syncronize_data()


        #clear the graphs
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()

        #plot TEG data
        self.ax1.plot( TEG1, 'bo-', label = 'TEG1')
        self.ax1.plot( TEG2, 'o-', label = 'TEG2')

        #plot voltage data
        self.ax2.plot( supply_voltage, label = 'Supply voltage')
        #self.ax2.plot( cell_voltage, label = 'Cell voltage')

        #plot current data
        self.ax3.plot( current, label = 'Supply current')

        self.ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        self.ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        self.ax3.legend(loc='center left', bbox_to_anchor=(1, 0.5))


        M = 6
        yticks = ticker.MaxNLocator(M)
        self.ax1.yaxis.set_major_locator(yticks)

        self.fig.tight_layout()

        self.canvas.draw()





    '''worker thread: does the data acquisition'''
    def worker_thread_1(self):
        global stop

        while stop == 0:
            if dry_run == 0:
                try:
                    self.TEG1.append(float(self.DAQ.query('MEAS:volt:dc? 0.1, .0000001, (@101)')))
                    self.TEG2.append(float(self.DAQ.query('MEAS:volt:dc? 0.1, .0000001, (@102)')))

                    self.supply_voltage.append(float(self.DAQ.query('MEAS:volt:{0}? auto, (@103)'.format(voltage_type))))
                    self.cell_voltage.append(float(self.DAQ.query('MEAS:volt:{0}? auto, (@104)'.format(voltage_type))))

                    self.current.append(float(self.DAQ.query('MEAS:curr:{0}? auto, (@122)'.format(voltage_type))))

                    self.elapsed_time.append(time.time() - self.start_time)
                    self.time_stamp.append(time.strftime("%m %d %Y, %H_%M_%S"))

                    if len(self.TEG1) % auto_data_save_at_this_number_of_samples == 0:
                        self.save_data('auto_saved_data')

                except TypeError:
                    #print('This caught it')
                    pass

            else:
                time.sleep(1)
                self.TEG1.append(np.random.randint(0,50))


    '''graph frame gui'''
    def graph_frame(self):


        self.fig = Figure(figsize=(10,7), dpi = 100) #creates the matplotlib figure
        self.ax1 = self.fig.add_subplot(311)
        self.ax2 = self.fig.add_subplot(312)
        self.ax3 = self.fig.add_subplot(313)

        frame1 = tk.Frame(self,width=100, height=200)
        frame1.grid(row=0,column=0)

        self.canvas = FigureCanvasTkAgg(self.fig, frame1)
        self.canvas.get_tk_widget().grid(row = 2, column = 0)

        frame2 = tk.Frame(self,width=100, height=200)
        frame2.grid(row=1,column=0)

        toolbar = NavigationToolbar2Tk(self.canvas, frame2 )
        toolbar.update()

    '''button frame gui'''
    def button_frame(self):

        frame2 = tk.Frame(self,width=100, height=200, borderwidth=10)
        frame2.grid(row=0, column = 1)

        graph_one_zoom_button = ttk.Button(frame2, text = 'Update graph', command = self.update_graph)
        graph_one_zoom_button.grid(row = 0, column = 0)


        save_button = ttk.Button(frame2, text = 'Save data', command = self.save_data)
        save_button.grid(row = 1, column = 0)

        text_field = tk.StringVar(frame2, value='Set filename')
        self.text_box = tk.Entry(frame2,textvariable=text_field)
        self.text_box.grid(row=1, column = 1)
        self.text_box.focus_set()

    '''save the data'''
    def save_data(self, path = None):

            if path == None:
                path = 'manually_saved_data'
            else:
                path = path

            elapsed_time, TEG1, TEG2, current, supply_voltage, cell_voltage, time_stamp = self.syncronize_data()

            data = {'Time': elapsed_time, 'TEG1': TEG1, 'TEG2': TEG2, 'Current': current, 'Supply_voltage' : supply_voltage, 'Cell_voltage': cell_voltage, 'Time_stamp' : time_stamp }

            df = pd.DataFrame(data)

            file_time = time.strftime("%b %d %Y, %H_%M_%S")
            file = self.text_box.get()
            print('{0} {1}.csv'.format(file, file_time))

            df.to_csv('{0}/{1} {2}.csv'.format(path, file,  file_time), index = None)

    '''get all the data lists the same length'''
    def syncronize_data(self):

        min_list_length = min([len(self.TEG2), len(self.TEG1), len(self.elapsed_time), len(self.cell_voltage), len(self.supply_voltage), len(self.current), len(self.time_stamp)])

        TEG1 = self.TEG1[:min_list_length]
        TEG2 = self.TEG2[:min_list_length]
        current = self.current[:min_list_length]
        cell_voltage = self.cell_voltage[:min_list_length]
        elapsed_time = self.elapsed_time[:min_list_length]
        supply_voltage = self.supply_voltage[:min_list_length]
        time_stamp = self.time_stamp[:min_list_length]

        return elapsed_time, TEG1, TEG2, current, supply_voltage, cell_voltage, time_stamp


    '''establish com with daq'''
    def daq_establish_com(self):
        #name = 'HEWLETT-PACKARD,34970A,0,13-2-2\n'
        self.ser = serial.Serial(
                port = daq_address,
                baudrate = 9600,
                parity = serial.PARITY_NONE,
                stopbits = serial.STOPBITS_ONE,
                bytesize = serial.EIGHTBITS
                )
        self.ser.timeout = 2
        self.ser.flushInput()
        self.ser.write(b'*IDN?\n')
        print(self.ser.readline())




        class DAQ_class():

            def query(command):
                command = command + '\n'
                self.ser.write(command.encode())
                reply = self.ser.readline()
                print(reply)
                if reply == b'':
                    pass

                else:
                    return(reply)

        self.DAQ = DAQ_class


#        self.DAQ = rm.open_resource(daq_address)
#
#        if dry_run == 0:
#            #check if connection is made
#            if self.DAQ.query('*IDN?') == name:
#                print('Communication established with Keysight DAQ')
#
#            else:
#                print('Communication error with DAQ. Check GPIB address in keysight connection expert.')





app = TIM()

app.mainloop()

#stops the data acquisition thread inside the gui class: TIM() - worker_thread_1
stop = 1








'''plot the data'''

elapsed_time, TEG1, TEG2, current, supply_voltage, cell_voltage, time_stamp = app.syncronize_data()

fig = plt.figure(figsize=(10,7))

ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)

#clear the graphs
ax1.clear()
ax2.clear()
ax3.clear()

#plot TEG data
ax1.plot(elapsed_time, TEG1, 'bo-', label = 'TEG1')
ax1.plot(elapsed_time, TEG2, 'o-', label = 'TEG2')

#plot voltage data
ax2.plot(elapsed_time, supply_voltage, label = 'Supply voltage')
ax2.plot(elapsed_time, cell_voltage, label = 'Cell voltage')

#plot current data
ax3.plot(elapsed_time, current, label = 'Supply current')

ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax3.legend(loc='center left', bbox_to_anchor=(1, 0.5))


M = 6
yticks = ticker.MaxNLocator(M)
ax1.yaxis.set_major_locator(yticks)

fig.tight_layout()

time.sleep(2)
app.ser.close()
print('closed com')


#shows any errors the DAQ encountered
#plt.pause(6)
#while True:
#    error = app.DAQ.query('SYSTem:ERRor?')
#    print(error)
#    if error == '+0,"No error"\n':
#        break

