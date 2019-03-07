# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 15:17:43 2019

@author: jmajor
"""

import visa
import time

rm = visa.ResourceManager()

power_supply = rm.open_resource('GPIB0::1::INSTR')

##################################
#initial_sleep = 60*60
#voltages_to_test =                         [.27, .43, .495, .595, 1.03,1.33]     +      [0]         +     [.595, 1.03,1.33]
#durations_of_tests_in_seconds =            [60*60]*6                             +      [60*60]     +     [30]*3
#duration_of_sleep_after_tests_in_seconds = [60*20]*6                             +      [0]         +     [60*60]*3
##################################


#################################
initial_sleep = 60*60
voltages_to_test =                         [.5, .7, 1, 1.25, 1.5,1.75]           +      [0]         +     [1.25, 1.5,1.75]
durations_of_tests_in_seconds =            [60*30]*6                             +      [60*60]     +     [30]*3
duration_of_sleep_after_tests_in_seconds = [60*30]*6                             +      [0]         +     [60*60]*3
#################################



print('Started test. Initial sleep for {} seconds'.format(str(initial_sleep)))

for i in range(initial_sleep):
    if i % 10 == 0:
        print(str(initial_sleep - i))
    time.sleep(1)

for i in range(len(voltages_to_test)):


    print('Power on')
    power_supply.write('APPL P25V, {0}, 1.0'.format(voltages_to_test[i]))
    power_supply.write('output:state on')
    time.sleep(durations_of_tests_in_seconds[i])
    power_supply.write('APPL P25V, {0}, 1.0'.format(0))
    power_supply.write('APPL P25V, 0, 0')
    print('Power off')
    time.sleep(duration_of_sleep_after_tests_in_seconds[i])

power_supply.write('output:state off')
print('Test done')