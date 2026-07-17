## Roeland huys pysignal toolox
#
# signals.py: signal generators and signal info
#

import numpy as np
from scipy import signal

def print_power(x):
    """print the total power of signal(s)
        x : ndarray
            Shape (N,) or (N,M)    
    """
    # Power verification
    Px = np.mean(np.abs(x)**2, axis=0)

    print("P = ", Px)

def awgn(N: int, P: float, as_complex: bool = False):
    """generate a flat AWGN noise signal
    
    # to create a power spectral density:
    dB_Hz = -120  # dB per herz power density
    P = 10**(dB_Hz/10) * fs  # total signal power
    x = ps.awgn(N=N, P=P, as_complex = False)
    
    Args:
        N (int): Number of samples
        P (float): total signal power in Watt
        as_complex (bool, optional): set True if it has to be a as_complex signal. Defaults to False.

    Returns:
        y: time domain samples
    """        
    y = np.sqrt(P) *  np.random.randn(N)
    if as_complex:
       y = y + 1j * np.random.randn(N)
    
    # scale power
    y *= np.sqrt(P / np.mean(np.abs(y)**2))
        
    return y

def bandpass_noise(N: int, fs: float, fc: float, bw: float, P: float, as_complex: bool = False):
    """generate an ideal bandpass noise signal

    Args:
        N (int): Number of samples
        fs (float): simulation sampling frequency
        fc (float): center frequency in Hz
        bw (float): bandwidth in Hz
        P (float): total signal power in Watt
        as_complex (bool, optional): set False if it has to be a as_complex signal. Defaults to True.

    Returns:
        y: time domain samples
    """    
    f = np.fft.fftfreq(N, 1/fs)

    # as_complex white spectrum
    X = (
        np.random.randn(N)
        + 1j * np.random.randn(N)
    )

    # Ideal bandpass mask
    H = (
        (f >= fc - bw/2) &
        (f <= fc + bw/2)
    )

    X *= H

    y = np.fft.ifft(X)

    if not as_complex:
        y = np.real(y)   

    # scale power
    y *= np.sqrt(P / np.mean(np.abs(y)**2))

    return y
