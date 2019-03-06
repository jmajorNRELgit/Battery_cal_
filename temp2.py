import visa

rm = visa.ResourceManager()

daq = rm.open_resource('GPIB0::3::INSTR')

daq.write('*RST')

daq.write('SENS:VOLT:DC:NPLC 10,(@101)')
#daq.write('SENS:RES:APER 0.002,(@101)')

daq.write('SENSE:VOLT:DC:RANG:AUTO ON,(@101)')
daq.write('SENSE:VOLT:DC:APER 0.001,(@101)')














#resolution = .001
#
#daq.write('CONF:VOLT:AC AUTO, MAX,(@101)')
#print(daq.write('SENS:VOLT:AC:BAND 200, (@101)'))
#print(daq.query('SENS:VOLT:AC:BAND? (@101)'))
#
#
#for i in range(3):
#    print(daq.query('MEAS:VOLT:AC? (@101)'), 'measurement')
#    print('\n', daq.query('SENS:VOLT:AC:BAND? (@101)'))
#
#
#
while True:
    error = daq.query('SYSTem:ERRor?')
    print(error)
    if error == '+0,"No error"\n':
        break