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


stop = 0


def animate(i):


    y1 = app.y1
    y2 = app.y2


    app.ax1.clear()
    app.ax2.clear()



    app.ax1.plot(y1, 'ro-', label = 'y1')
    app.ax2.plot(y2, 'go-', label = 'y2')

    app.ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    app.ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    app.f.tight_layout()






class TIM(tk.Tk):

    f = Figure(figsize=(10,7), dpi = 100) #creates the matplotlib figure
    ax1 = f.add_subplot(211) #adds the top plot (full time and partial time plots)
    ax2 = f.add_subplot(212) #adds the top plot (full time and partial time plots)



    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.y1 = []
        self.y2 = []
        self.time = []

        self.start = time.time()

        self.graph_frame()


        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start(  )


    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O.
        """
        global stop

        while stop == 0:
           time.sleep(.001)
           self.y1.append(random.rand()*1*-10**-7)
           self.y2.append(random.rand()*1*-10**-7)
           self.time.append(time.time() - self.start)

           if len(self.y1) % 10000 == 0:
               self.save_data()

           if len(self.y1) % 1000 == 0:
               print(len(self.y1))

    def save_data(self):
        min_list_length = min([len(self.y1), len(self.y2), len(self.time)])
        y1 = app.y1[:min_list_length]
        y2 = app.y2[:min_list_length]
        times = app.time[:min_list_length]


        data = {'Time': times, 'y1': y1, 'y2': y2}

        df = pd.DataFrame(data)

        file = time.strftime("%b %d %Y, time_%H_%M_%S")
        print('{0}.csv'.format(file))

        df.to_csv('test_data/{0}.csv'.format(file), index = None)



    def graph_frame(self):
        frame1 = tk.Frame(self,width=100, height=200)
        frame1.grid(row=0,column=0)

        canvas = FigureCanvasTkAgg(self.f, frame1)
        canvas.get_tk_widget().grid(row = 2, column = 0)



app = TIM()
ani = animation.FuncAnimation(app.f,animate, interval = 1)

app.mainloop()

stop = 1
