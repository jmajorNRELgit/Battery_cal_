# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 08:15:11 2019

@author: jmajor
"""

import threading
import time

stop = 0
i = 0
def workerThread1():
    global i
    while stop == 0:
        print(i)
        i+=1
        time.sleep(1)

thread1 = threading.Thread(target = workerThread1)
thread1.start()




stop = input('Enter a number besides 0: ' or 1)