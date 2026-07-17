## pysignal by Roeland Huys
#
# test_ADC_DAC: demonstration ADC and DAC
#

import numpy as np
import matplotlib.pyplot as plt
import pysignal as ps

fs = 64e9            # Simulation sample rate

N = 2**14   # number of points

# create 5 bands in the total RF range
bands = np.linspace(2 , 6 , 5)*1e9 

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

# sample with ADC
gain = 1/np.max(abs(x))
print(f"ADC gain: {gain}")
x_adc = ps.adc(x*gain, fs, 4, 8)
fs_adc = fs / 4

### PLOTTING

fig, ax = plt.subplots(2,2)

## plot input RF 

# better plot decoration
ps.nice_axes(ax[0,0])

ps.plot_psd(x, fs, Nbins = 1024)
plt.ylim(-130, -60)

# print the total signal power for all signals
ps.print_power(x)

# draw an arrow
ps.varrow(fs_adc, f'fs_adc {fs_adc/1e9:.1f}GHz')

# time domain plot

ps.nice_axes(ax[0,1])
plt.plot(x)

## plot after ADC sampling
ps.nice_axes(ax[1,0])

ps.plot_fft(x_adc, fs_adc)

ps.nice_axes(ax[1,1])
plt.plot(x_adc)


plt.show(block=not plt.isinteractive())  