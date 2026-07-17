## pysignal by Roeland Huys
#
# test_DAC: simple DAC test
#
# I use ps.bandpass_noise as a reference signal, because a quantized harmonic signal does not create a nice visual noise floor
# Also we make sure all PSD plots use the same df (display bandwidth) so you can compare the PSD levels
#


import numpy as np
import matplotlib.pyplot as plt
import pysignal as ps

fs = 8e6            # Simulation sample rate

N = 2**12   # number of simulation points

f_sig = 0.8e6  # harmonic frequency (Hz)
P_sig = 1      # harmonic power (W)
B_sig = 0.1e6  # sinal bandwidth (Hz)
P_noise = 0.01 # noise power (W)

nbits_dac = 3   # number of ADC bits
ov_dac = 4      # dac oversampling factor
fs_dac = fs / ov_dac  # adc sample rate
df = fs / 256   # display bin size for the PSD.  We make it the same for all plots independent on the sampling rate

# create a bandpass signal
x = ps.bandpass_noise(N, fs, f_sig, B_sig, P_sig);

# normalize the signal to match maximum output swing
gain = 1/np.max(abs(x))
x = ps.quantize(x*gain, nbits_dac, x_range = (-1, 1), int_out = True)

x_dac = ps.dac(x, fs, fs_dac, nbits=nbits_dac, dither = True)

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
