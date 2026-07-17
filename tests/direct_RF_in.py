## pysignal by Roeland Huys
#
# direct_RF_in: simple direct sampling with ADC and digital DDC and multiple bands

import numpy as np
import matplotlib.pyplot as plt
import pysignal as ps
from scipy.signal import butter, lfilter

# base band digital sample rate
# this is also the sampling rate of ALL filters
fs_band = 620e6  

# output of IF, runs at an integer rate of fs_band
# so the filters can be implemented 6x polyphasic, and run at the same digital clock
fs_IF = fs_band * 6

# the ADC sample runs at an integer rate of fs_IF
# so the ADC could be implemented as parallel filter banks running at fs_band
# also the decimation filter runs with 42 parallel polyphasic filters running at fs_band
fs_adc = fs_IF * 7

# Simulation sample rate for input RF (analog) signals
fs = fs_adc * 4

# basic number of bits
# we tune this in such a way that the output SNR is dominated by the input noise
# here, we achive about 10dB output SNR
# however, this can be reduced, depending on the desired output SNR
nbits_adc = 4
nbits_IF = 6
nbits_Band = 6

N_bands = 7
B_band = 0.45e9   # bandwidth of a single band
# create a set of bands
f_sig = np.linspace(27.5e9 + B_band/2, 31e9 - B_band/2, N_bands)

fc_sig = np.mean(f_sig)   # center RF carrier frequency
B_sig  = np.ptp(f_sig) + B_band  # ptp(x) = max(x) - min(x)

# signal power (W) - we eventually normalize this to the ADC input range so don't bother
P_sig = 1
PSD_noise = -110   # noise PSD (dB/Hz)
P_noise = 10**(PSD_noise/10) * fs  # total noise power (W)

# calculate number of required datapoints
N_d = 2**11       # number of simulation datapoints

N = N_d * int(fs / fs_band)   # total number of simulation points

# create 7 bands in the total RF range
x = np.column_stack([    ps.bandpass_noise( N=N, fs=fs, fc=fc, bw=B_band, P=P_sig)   for fc in f_sig   ])
#x = ps.bandpass_noise( N=N, fs=fs, fc=27.5e9, bw=B_sig, P=P_sig) 

# create noise
xn = ps.awgn(N=N, P=P_noise, as_complex = False)
x = np.column_stack((x, xn))

# normalize the signal to match maximum output swing
gain = 1/np.max(abs(x))
x = x*gain

x_adc = ps.adc(x, fs, fs_adc, nbits=nbits_adc, dither = True)   # 4 bits ADC seems sufficient in this example
t_adc = np.arange(len(x_adc)) / fs_adc

# shift the bands to center frequency 
f_shift = -(fc_sig - fs_adc)
nco = np.exp(1j * 2* np.pi * f_shift * t_adc) 
nco = np.repeat( nco[:, None], x_adc.shape[1], axis = 1)
x_shift = x_adc * nco

# perform decimation filter, we need at least 3th order to prevent aliasing
b, a = butter(3, Wn=B_sig/fs_adc, btype='low')
x_filt = lfilter(b, a, x_shift, axis = 0)
x_filt = ps.quantize(x_filt, nbits_IF)  # number of bits after the filter, the impact of this is visible after decimation

# decimate -> IF frequency 
x_IF = ps.downsample(x_filt, int(fs_adc / fs_IF))
t_IF = np.arange(len(x_IF)) / fs_IF

# frequency shift and filter band #4

f_bands = f_sig - fc_sig  # input signal bands

f_shift_band = -f_bands[4]
nco = np.exp(1j * 2* np.pi * f_shift_band * t_IF) 
nco = np.repeat( nco[:, None], x_IF.shape[1], axis = 1)
x_IF_shift = x_IF * nco
b, a = butter(8, Wn=B_band/fs_IF, btype='low')  # need at least a 6th order filter to separate the bands
x_IF_filter = lfilter(b, a, x_IF_shift, axis=0)
x_IF_filter = ps.quantize(x_IF_filter, nbits_Band)

# decimate band output
x_band = ps.downsample(x_IF_filter, int(fs_IF / fs_band))


### PLOTTING

fig, ax = ps.subplots(3,2)

## plot input RF 

# better plot decoration
ps.axes(ax[0,0], f"input signal, PSD" )

ps.plot_PSD(x, fs, Nbins = 256)
plt.ylim(-140, -90)
ps.varrow(fs_adc, f'fs_adc {fs_adc/1e6:.1f}MHz')   # draw an arrow on ADC freq
plt.legend(['band0', 'band1', 'band2', 'band3', 'band4', 'band5', 'band6', 'input_noise'])

## plot after ADC sampling

ps.axes(ax[1,0], f"ADC output, nbits_adc={nbits_adc}")
ps.plot_PSD(x_adc, fs_adc, Nbins = 256)
plt.ylim(-140, -90)

## plot after freqency shift and filter

ps.axes(ax[2,0], f"after frequency shift and filter, nbits_IF={nbits_IF}")
ps.plot_PSD(x_shift, fs_adc, Nbins = 256)
plt.ylim(-140, -90)
ps.varrow(fs_IF, f'fs_adc {fs_IF/1e6:.1f}MHz')   # draw an arrow on ADC freq

## plot after decimation

ps.axes(ax[0,1], f"IF after decimation, nbits_IF={nbits_IF}")
ps.plot_PSD(x_IF, fs_IF, Nbins = 256)
plt.ylim(-140, -90)

## plot after IF shift and filter 

ps.axes(ax[1,1], f"after shift and filter, nbits_Band={nbits_Band}")
ps.plot_PSD(x_IF_filter, fs_IF, Nbins = 256)
plt.ylim(-140, -90)
ps.varrow(fs_band, f'fs_band {fs_band/1e6:.1f}MHz')   # draw an arrow on ADC freq


## plot after decimation

ps.axes(ax[2,1], f"band output, nbits_Band={nbits_Band}")
ps.plot_PSD(x_band, fs_band, Nbins = 256)
plt.ylim(-140, -90)





## 

if not plt.isinteractive(): plt.show()  
