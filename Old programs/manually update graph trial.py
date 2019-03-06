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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk



class TIM(tk.Tk):




    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.graph_frame()
        self.button_frame()

        self.y = [0,1,2]



    def graph_frame(self):

        plt.ion()

        self.f = Figure(figsize=(10,7), dpi = 100) #creates the matplotlib figure
        self.ax1 = self.f.add_subplot(111)



        frame1 = tk.Frame(self,width=100, height=200)
        frame1.grid(row=0,column=0)



        self.canvas = FigureCanvasTkAgg(self.f, frame1)
        self.canvas.get_tk_widget().grid(row = 2, column = 0)

        frame2 = tk.Frame(self,width=100, height=200)
        frame2.grid(row=1,column=0)

        toolbar = NavigationToolbar2Tk(self.canvas, frame2 )
        toolbar.update()






    def button_frame(self):

        frame2 = tk.Frame(self,width=100, height=200, borderwidth=10)
        frame2.grid(row=0, column = 1)

        graph_one_zoom_button = ttk.Button(frame2, text = 'Zoom graph', command = self.call_animate)
        graph_one_zoom_button.grid(row = 0, column = 0)



    def call_animate(self):
        print('foo')
        self.ax1.clear()
        self.ax1.plot(self.y)
        #self.ax1.autoscale()
        self.canvas.draw()
        self.y.append(self.y[-1] + 1)












app = TIM()


app.mainloop()

