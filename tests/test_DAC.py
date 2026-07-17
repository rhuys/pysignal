## pysignal by Roeland Huys
#
# test_ADC: simple ADC test
#

import numpy as np
import matplotlib.pyplot as plt
import pysignal as ps

fs = 8e6            # Simulation sample rate

N = 2**14   # number of points

nsamples = 4
fs_dac = fs / nsamples  # DAC sample rate


t = np.arange(N/nsamples)/fs_dac
x = np.sin(2*np.pi*t * 0.55e6)

gain = np.max(abs(x))
x_adc = ps.adc(x/gain, fs, nsamples=nsamples, nbits=3, dither = False)
t_adc = np.arange(N/nsamples) / (fs/nsamples)
fs_adc = fs / nsamples

### PLOTTING

fig, ax = plt.subplots(2,2)

## plot input RF 

# better plot decoration
ps.nice_axes(ax[0,0])

ps.plot_fft(x, fs)
#plt.ylim(-130, -60)

# print the total signal power for all signals
ps.print_power(x)

# draw an arrow
ps.varrow(fs_adc, f'fs_adc {fs_adc/1e9:.1f}GHz')

# time domain plot

ps.nice_axes(ax[0,1])
ps.plot_t(x, fs)
plt.xlim(0, 1e-5)

## plot after ADC sampling

ps.nice_axes(ax[1,0])

ps.plot_fft(x_adc, fs_adc)

ps.nice_axes(ax[1,1])
ps.plot_t(x_adc, fs_adc)
plt.xlim(0, 1e-5)


plt.show(block=not plt.isinteractive())  