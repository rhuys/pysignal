## pysignal by Roeland Huys
#
# direct_RF_in: simple direct sampling with ADC and digital DDC and multiple bands

import numpy as np
import matplotlib.pyplot as plt
import pysignal as ps

fs_d = 620e6                  # base digital sample rate
N_d = 2**10
#df = fs_d / 128     # psd display bin bandwidth

fs_IF = fs_d * 6
fs_adc = fs_d * 6 * 7

fs = fs_adc * 4            # Simulation sample rate
N = N_d * int(fs / fs_d)   # total number of simulation points

nbits_adc = 4

B_sig = 0.5e9  # sinal bandwidth (Hz)
f_sig = np.linspace(27.5e9 + B_sig/2 , 31e9-B_sig/2 , 7)    # 7 frequency bands
fc_sig = (f_sig[-1] + f_sig[0])/2  # center frequency of the signal
P_sig = 1      # signal power (W)

PSD_noise = -120   # noise PSD (dB/Hz)
P_noise = 10**(PSD_noise/10) * fs  # total noise power (W)

# create 7 bands in the total RF range
x = np.column_stack([    ps.bandpass_noise( N=N, fs=fs, fc=fc, bw=B_sig, P=P_sig)   for fc in f_sig   ])
#x = ps.bandpass_noise( N=N, fs=fs, fc=27.5e9, bw=B_sig, P=P_sig) 

# create noise
xn = ps.awgn(N=N, P=P_noise, as_complex = False)
x = np.column_stack((x, xn))

# normalize the signal to match maximum output swing
gain = 1/np.max(abs(x))
x = x*gain

x_adc = ps.adc(x, fs, fs_adc, nbits=nbits_adc, dither = True)
t_adc = np.arange(len(x_adc)) / fs_adc

# shift the bands to center frequency and perform decimation filter
f_shift = -(fc_sig - fs_adc)
nco = np.exp(1j * 2* np.pi * f_shift * t_adc) 
nco = np.repeat( nco[:, None], x_adc.shape[1], axis = 1)
x_shift = x_adc * nco


### PLOTTING

fig, ax = ps.subplots(3,1)

## plot input RF 

# better plot decoration
ps.axes(ax[0], f"input signal, PSD" )

ps.plot_PSD(x, fs, Nbins = 256)
plt.ylim(-140, -90)

# print the total signal power for all signals
#ps.print_power(x)

# draw an arrow
ps.varrow(fs_adc, f'fs_adc {fs_adc/1e6:.1f}MHz')

## plot after ADC sampling

ps.axes(ax[1], f"ADC output, {nbits_adc}bits")

ps.plot_PSD(x_adc, fs_adc, Nbins = 256)
#plt.ylim(-100, -50)

## plot after freqency shift

ps.axes(ax[2], f"after frequency shift")

ps.plot_PSD(x_shift, fs_adc, Nbins = 256)


## 

if not plt.isinteractive(): plt.show()  
