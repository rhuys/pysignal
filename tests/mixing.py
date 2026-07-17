## pysignal by Roeland Huys
#
# mixing.py: demonstration ADC + mixing + bandpass filtering
#

import numpy as np
import matplotlib.pyplot as plt
import pysignal as ps

fs_d = 620e6                  # base digital sample rate

fs_IF = fs_d * 6
fs_ADC = fs_d * 6 * 7

fs = fs_ADC * 4            # Simulation sample rate
N = 2**14   # number of points


# create 7 bands in the total RF range
bands = np.linspace(27500 + 500/2 , 31000-500/2 , 7)*1e6  

# create 7 signal bands in a stack
# result is a matrix with size (N,7)
# most scipy and plot function work on the signals in parallel if you use axis=0
x = np.column_stack([
    ps.bandpass_noise( N=N, fs=fs, fc=fc, bw=500e6, P=1)
    for fc in bands
])

# create -20dB/Hz power
dB_Hz = -120  # dB per herz power density
P = 10**(dB_Hz/10) * fs  # total signal power
x = np.column_stack((x, ps.awgn(N=N, P=P, complex = False)))


## sample
x_ADC = ps.adc()


#### create plots
fig, ax = plt.subplots(2,1)

## print input RF signal
# better plot decoration
ps.nice_axes(ax[0])

ps.plot_psd(x, fs, Nbins = 1024)
ax.set_ylim(-130, -80)

# print the total signal power for all signals
ps.print_power(x)

# draw an arrow
ps.varrow(fs_ADC, f'fs_ADC {fs_ADC/1e9:.3f}GHz')

## print ADC sampeld signal
ps.nice_axes(ax[1])

ps.plot_psd(x_ADC, fs_ADC, Nbins=64)


plt.show(block=not plt.isinteractive())  