## pysignal by Roeland Huys
#
# test_ADC: simple ADC test
#
# I use ps.bandpass_noise as a reference signal, because a quantized harmonic signal does not create a nice visual noise floor
# Also we make sure all PSD plots use the same df (display bandwidth) so you can compare the PSD levels
#
# Observations:
#  Quantization: 
#    with 3 bits sampling, we expect a quantization noise of SQNR = nbits*6.02 + 1.76 = 19.82dB
#    the power of the quantization noise is hence -19.82dB, if 0dB is the reference.
#    for PSD you must divide this by the sampling rate
#    note that the psd plot the output plot return_onesided, the power is folded from negative and positive freq so you have to add +3.01dB
#  Dither:  I tested this, and indeed, we get about the same noise power.

import numpy as np
import matplotlib.pyplot as plt
import pysignal as ps

fs = 8e6            # Simulation sample rate

N = 2**12   # number of simulation points

f_sig = 0.8e6  # harmonic frequency (Hz)
P_sig = 1      # harmonic power (W)
B_sig = 0.1e6  # sinal bandwidth (Hz)
P_noise = 0.01 # noise power (W)

nbits_adc = 3   # number of ADC bits
decim_adc = 4   # adc decimation
fs_adc = fs / decim_adc  # adc sample rate
df = fs / 256   # display bin size for the PSD.  We make it the same for all plots independent on the sampling rate

## generate input signal
#t = np.arange(N)/fs
#x  = np.sin(2*np.pi*t * 0.8e6)

# create a bandpass signal
x = ps.bandpass_noise(N, fs, f_sig, B_sig, P_sig);

# normalize the signal to match maximum output swing
gain = 1/np.max(abs(x))
x = x*gain

x_adc = ps.adc(x, fs, fs_adc, nbits=nbits_adc, dither = True)

### PLOTTING

fig, ax = ps.subplots(2,2)

## plot input RF 

# better plot decoration
ps.axes(ax[0,0], f"input signal, PSD" )

ps.plot_PSD(x, fs, Nbins = int(fs / df))
plt.ylim(-100, -50)

psd_sig_dB = 10*np.log10(P_sig*gain*gain / B_sig)
plt.text(f_sig, psd_sig_dB, f"sig: {psd_sig_dB:.1f}dB/Hz", ha='center')

# print the total signal power for all signals
#ps.print_power(x)

# draw an arrow
ps.varrow(fs_adc, f'fs_adc {fs_adc/1e6:.1f}MHz')

ps.axes(ax[0,1], f"input signal, time domain")
ps.plot_t(x, fs)
plt.xlim(0, 1e-4)

## plot after ADC sampling

ps.axes(ax[1,0], f"ADC output, {nbits_adc}bits")

ps.plot_PSD(x_adc, fs_adc, Nbins = int(fs_adc / df))
plt.ylim(-100, -50)

# compute the quantization noise shown on the PSD
# the bandwidth of the quantization noise is fs_adc but we add 3dB because the PSD plot folds the power of the negative frequencies
psd_qn_dB = -(nbits_adc*6.02 + 1.76)  - 10*np.log10(fs_adc) + 3.01
plt.text(0, psd_qn_dB, f"quant noise: {psd_qn_dB:.1f}dB/Hz")

ps.axes(ax[1,1], f"ADC output, {nbits_adc}bits")
ps.plot_t(x_adc, fs_adc)
plt.xlim(0, 1e-4)

if not plt.isinteractive(): plt.show()  
