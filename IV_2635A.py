# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 10:42:55 2018

@author: lsd_u
"""
import time
start = time.time()
import numpy as np
import pyvisa as visa
import pathlib
import matplotlib.pyplot as plt

#====== Initial configs =====#

parametro = 15
pathlib.Path('/Users/LAB MAt/Desktop/Joao_Doutorado/Programas finais/IV_TEG/%d' % parametro).mkdir(parents=True, exist_ok=True)
number_of_curves = 1
medidas = [[] for i in range(number_of_curves)]
rm = visa.ResourceManager()
keithley = rm.open_resource('GPIB1::26::INSTR')
keithley.write('smua.reset()')
keithley.write('display.screen = 0')
keithley.write('display.smua.measure.func = display.MEASURE_DCAMPS')
#keithley.write('display.smua.measure.func = display.MEASURE_DCVOLTS')
#keithley.write('smua.sense = smua.SENSE_LOCAL')
keithley.write('smua.sense = smua.SENSE_REMOTE')
keithley.write('format.data = format.ASCII')
keithley.write('localnode.linefreq = 60')
keithley.write('smua.measure.nplc = 1')
#keithley.write('smua.measure.autozero = smua.AUTOZERO_AUTO')
keithley.write('smua.source.limiti = 1')
#===== Range configs ====#
#keithley.write('smua.source.rangei = 2')
keithley.write('smua.source.rangev = 20')
keithley.write('smua.measure.rangev = 20')
keithley.write('smua.measure.rangei = 20')
#keithley.write('smua.measure.autorangev = smua.AUTORANGE_ON')
#keithley.write('smua.measure.autorangei = smua.AUTORANGE_ON')
#keithley.write('smua.source.autorangev = smua.AUTORANGE_ON')
#keithley.write('smua.source.autorangei = smua.AUTORANGE_ON')

#===== Delay configs ====#
keithley.write('smua.measure.delay = smua.DELAY_AUTO')
keithley.write('smua.source.delay = 0.1')
#keithley.write('smua.measure.delay = 0.1')

#=== Buffer and source type configs ===#

#keithley.write('smua.nvbuffer1.collectsourcevalues = 1')
keithley.write('smua.source.func = smua.OUTPUT_DCVOLTS')
#keithley.write('smua.source.func = smua.OUTPUT_DCAMPS')


#=== Filter ===#
keithley.write('smua.measure.filter.count = 50')
keithley.write('smua.measure.filter.type = smua.FILTER_REPEAT_AVG')
keithley.write('smua.measure.filter.enable = smua.FILTER_OFF')

#=== Sweep ===#
#keithley.write('smua.source.highc = smua.ENABLE') 
#keithley.write('smua.source.levelv = 0.2')

#keithley.write('delay(1)')

for k in range(number_of_curves):
        keithley.write('smua.source.output = smua.OUTPUT_ON')
        keithley.write('smua.nvbuffer1.clear()')
        keithley.write('smua.nvbuffer1.appendmode = 1')
        keithley.write('smua.nvbuffer2.clear()')  
        keithley.write('smua.nvbuffer2.appendmode = 1')
#        keithley.write('smua.source.limiti = 0.01')
#        keithley.write('smua.source.rangev = 0.2')
        
        for v in np.arange(-0.1, 4.9, 0.01): # (minimo, maximo-passo, passo)
            keithley.write('smua.source.levelv = %.4f' % v)
            keithley.write('smua.measure.v(smua.nvbuffer1)')
            keithley.write('smua.measure.i(smua.nvbuffer2)')
            keithley.timeout = 200000000
            
        current = keithley.query('printbuffer(1, smua.nvbuffer2.n, smua.nvbuffer2.readings)')
        voltage = keithley.query('printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)')
        voltagem = [float(v) for v in voltage.split(",")]
        corrente = [-float(i) for i in current.split(",")]
        iv_curve = list(zip(voltagem,corrente))
        medidas[k].append(iv_curve)
#        f, axarr = plt.subplots(2, sharex=True)
#        axarr[0].plot(np.array(voltagem), np.array(corrente),'o-')
#        axarr[1].semilogy(np.array(voltagem), abs(np.array(corrente)),'o-')
        plt.plot(np.array(voltagem),np.array(corrente),'o-')
#        axarr[0].plot(np.array(corrente), np.array(voltagem),'ko-')
#        axarr[1].semilogy(np.array(corrente), abs(np.array(voltagem)),'ko-')
        keithley.write('smua.source.output = smua.OUTPUT_OFF')
for i in range(len(medidas)):
    with open('/Users/LAB MAt/Desktop/Joao_Doutorado/Programas finais/IV_TEG/%d/%i.txt' % (parametro,i), 'w') as f:
        for j in range(len(medidas[i][0])):
                f.write("%.4f %.5f \n" % (medidas[i][0][j][0], medidas[i][0][j][1]))
#
print("Done!")
end = time.time()
