## pysignal by Roeland Huys
#
# test_signal_PSD: demonstration of bandpass_noise, awgn, and plot_psd
#

import numpy as np
import matplotlib.pyplot as plt
import pysignal as ps

fs = 64e9            # Simulation sample rate

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

# create plot
fig, ax = plt.subplots()
# better plot decoration
ps.nice_axes(ax)

ps.plot_psd(x, fs, Nbins = 1024)
ax.set_ylim(-130, -60)

# print the total signal power for all signals
ps.print_power(x)

# draw an arrow
ps.varrow(0, 'DC')

plt.show(block=not plt.isinteractive())  