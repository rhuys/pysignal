## Roeland huys pysignal toolox
#
# signals.py: signal sampling
#

from scipy import signal
import numpy as np


def downsample(x, nsamples: int):
    """Downsample a signal by an integer factor.

    Args:
        x : ndarray Shape (N,) or (N,M), input data
        nsamples : int, Decimation factor

    Returns:
        y : ndarray, Downsampled signal
    """
    x = np.asarray(x)
    return x[::nsamples]


def upsample(x, nsamples: int, zoh = False):
    """Upsample a signal by an integer factor. 
    By default, insert zeros.  With zoh option, the samples are repeated

    Args:
        x : ndarray, Shape (N,) or (N,M) input data
        nsamples : int, Upsample factor
        zoh : bool, if True, the samples will be repeated, if false, zeros are inserted

    Returns:
        y : ndarray, Upsampled signal
    """
    
    x = np.asarray(x)
    return x[::nsamples]



### TODO: 
# add analog input bandwidth
# add clock jitter
# add DNL / INL
def adc(x, fs: float, nsamples: int, nbits: int, dither = False):
    """basic ADC model; sample an input signal with simulation sampling rate fs, to an ADC sampling rate fs/nsamples
    the full input amd output scale is assumed -1 ... +1
    the input signal is clipped.
    The output sampling rate will be fs / nsamples

    Args:
        x (_type_): Shape (N,) or (N,M), input data
        fs (float): sampling rate of the input signal [Hz]
        nsamples (int): decimation factor.  
        nbits (int): number of quantization nbits.
        dither (bool, optional): add quantization noise instead of perfrming actual quantization (default False). Defaults to False.

    Returns:
         y : ndarray, sampled signal
    """
    # make sure x is an array
    x = np.asarray(x)

    x = x[::nsamples]  # decimate
    x = np.clip(x, -1.0, 1.0) # clip the input data
    
    q = 2**nbits
    if dither:
        # add some quantization noise
        n = np.random.uniform(
            low  = -1/q,
            high = +1/q,
            size = x.shape
        )
        x =  x + n

    # perform actual quantization
    # move the scale to 0...1
    x = (x+1)/2
    # round to nbits-1
    x = np.round(x * (2**nbits-1)) / (2**nbits-1)
    # move the scale back to -1...+1
    x = 2*x - 1
    
    return x
    