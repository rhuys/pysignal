## pysignal by Roeland Huys
#
# test_ADC: simple ADC test
#
# I use ps.bandpass_noise as a reference signal, because a quantized harmonic signal does not create a nice visual noise floor
#
# Observations:
#  with 2 bits sampling, we expect a quantization noise floor of SQNR = nbits*6.02 + 1.76 = 13.8dB
#  in the output plot, with 

import numpy as np
import matplotlib.pyplot as plt
import pysignal as ps

fs = 8e6            # Simulation sample rate

N = 2**10   # number of points

## generate input signal
t = np.arange(N)/fs
x  = np.sin(2*np.pi*t * 0.8e6)

# create a bandpass signal
#x = ps.bandpass_noise(N, fs, 0.8e6, 0.1e6, 1);

gain = np.max(abs(x))
x = x/gain

nsamples = 4
nbits = 2

x_adc = ps.adc(x, fs, nsamples=nsamples, nbits=nbits, dither = True)
fs_adc = fs / nsamples

### PLOTTING

fig, ax = plt.subplots(2,2)

## plot input RF 

# better plot decoration
ps.nice_axes(ax[0,0])

ps.plot_periodogram(x, fs)
plt.ylim(-100, -50)

# print the total signal power for all signals
ps.print_power(x)

# draw an arrow
ps.varrow(fs_adc, f'fs_adc {fs_adc/1e6:.1f}MHz')

# time domain plot

ps.nice_axes(ax[0,1])
ps.plot_t(x, fs)
plt.xlim(0, 1e-4)

## plot after ADC sampling

ps.nice_axes(ax[1,0])
plt.title(f"After ADC, {nbits}bits")

ps.plot_periodogram(x_adc, fs_adc)
plt.ylim(-100, -50)

ps.nice_axes(ax[1,1])
ps.plot_t(x_adc, fs_adc)
plt.xlim(0, 1e-4)


plt.show(block=not plt.isinteractive())  