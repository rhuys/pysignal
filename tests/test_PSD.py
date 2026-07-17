## pysignal by Roeland Huys
#
# test_PSD: simple experiments with power spectral density plots
#
# tests:
#  * create a harmonic signal with sin() 
#  * create a bandpass "noisy" siganl with ps.bandpass_noise
#  * use ps.plot_PSD to check if the power (PSD) is correct
#
# observations:
#  * Using PSD plots, a harmonic signal level will depend on the bin width df.  less bins -> larger df -> peak will be smaller
#    Equation:  psd_sig = P_sig/df   # df is the display bandwidth.  Signal bandwidth is theoretically 0
#  * A bandpass noisy signal will not change in function of bin width.  
#    Equation:  psd_sig = P_sig/B_sig   # B is the signal bandwidth
#  * Selecting a smaller set of samples (SUBSET in the example)  will create a more noisy signal, but does not influence the PSD levels

import numpy as np 
import matplotlib.pyplot as plt
import pysignal as ps  # my own library

fs = 8e6            # Simulation sample rate
N = 2**14   # number of points

f_sig = 0.8e6  # harmonic frequency (Hz)
P_sig = 1  # harmonic power (W)
P_noise = 0.01 # noise power (W)

Nbins = 256 # display bin width for the spectrogram

## generate harmonic signal of 1W with noise of 0.1W

t = np.arange(N)/fs
x  = P_sig * np.sqrt(2) * np.sin(2*np.pi*t * f_sig)
x = x + ps.awgn(N, P_noise, False)

SUBSET = 4; # smaller sample set

### PLOTTING

fig, ax = ps.subplots(2,2)

# PLOT HARMONIC SIGNAL PSD

ps.axes(ax[0,0], f"Harmonic signal, fs = {fs/1e6}MHz, N = {len(x)}" )
df = ps.plot_PSD(x, fs, Nbins = 512)
plt.ylim(-90, -30)

# calculate the expected harmonic signal PSD
psd_sig_dB = 10*np.log10(P_sig/df)
plt.annotate(f'df: {df/1000:0.1f}kHz, sig: {psd_sig_dB:.1f}dB/Hz', (f_sig, psd_sig_dB), xytext = (0, 20), ha='center', textcoords='offset points', arrowprops=dict(arrowstyle='->') )


x = x[0:N//SUBSET]
ps.axes(ax[0,1], f"harmonic signal, fs = {fs/1e6}MHz, N = {len(x)}")
df = ps.plot_PSD(x, fs, Nbins = 128)
plt.ylim(-90, -30)

# calculate the expected harmonic signal PSD
psd_sig_dB = 10*np.log10(P_sig/df)
plt.annotate(f'df: {df/1000:0.1f}kHz, sig: {psd_sig_dB:.1f}dB/Hz', (f_sig, psd_sig_dB), xytext = (0, 20), ha='center', textcoords='offset points', arrowprops=dict(arrowstyle='->') )


## generate 1W "bandpass" noisy input signal with noise of 0.1W
## expecting a psd of 

P_sig   = 1
B_sig   = 0.1e6
P_noise = 0.01  # W

x  = ps.bandpass_noise(N, fs, 0.8e6, 0.1e6, 1, as_complex = False)
x = x + ps.awgn(N, P_noise, False)

### PLOTTING

ps.axes(ax[1,0], f"Bandpass noisy signal, fs = {fs/1e6}MHz, N = {len(x)}")
df = ps.plot_PSD(x, fs, Nbins = 512)
plt.ylim(-90, -30)

# calculate the expected harmonic signal PSD
psd_sig_dB = 10*np.log10(P_sig / B_sig)
plt.annotate(f'df: {df/1000:0.1f}kHz, sig: {psd_sig_dB:.1f}dB/Hz', (f_sig, psd_sig_dB), xytext = (0, 20), ha='center', textcoords='offset points', arrowprops=dict(arrowstyle='->') )


x = x[0:N//SUBSET]
ps.axes(ax[1,1], f"Bandpass noisy signal, fs = {fs/1e6}MHz, N = {len(x)}")
df = ps.plot_PSD(x, fs, Nbins = 128)
plt.ylim(-90, -30)

# calculate the expected harmonic signal PSD
psd_sig_dB = 10*np.log10(P_sig / B_sig)
plt.annotate(f'df: {df/1000:0.1f}kHz, sig: {psd_sig_dB:.1f}dB/Hz', (f_sig, psd_sig_dB), xytext = (0, 20), ha='center', textcoords='offset points', arrowprops=dict(arrowstyle='->') )

###

if not plt.isinteractive(): plt.show()  
