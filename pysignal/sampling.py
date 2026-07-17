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
    #make sure x is an array with dimension (N, M)
    x = np.asarray(x)
    if x.ndim == 1:  x = x[:, None]
    return x[::nsamples]  # downsample

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
    #make sure x is an array with dimension (N, M)
    x = np.asarray(x)
    if x.ndim == 1:  x = x[:, None]
    
    N, M = x.shape
    if zoh:
        y = np.repeat(x, nsamples, axis=0)
    else:
        y = np.zeros((N * nsamples, M), dtype=x.dtype)
        y[::nsamples] = x
    return y


def quantize(x, nbits: int, x_range = (-1.0, 1.0), int_out: bool = False, dither = False):
    """Quantize and clip a signal

    Args:
        x : ndarray, Shape (N,) or (N,M) input data
        nbits (int): number of quantization nbits.
        x_range (float, float): (minimum, maximum) input range of x, outside range will be clipped.  
        int_out (bool, optional): if True, then the output will be simple integers from 0 ... 2**nbits-1
        signed (bool, optional): _description_. Defaults to True.
        dither (bool, optional): add quantization noise before actual quantization (default False).  
    """

    #make sure x is an array with dimension (N, M)
    x = np.asarray(x)
    if x.ndim == 1:  x = x[:, None]
    
    steps = 2**nbits-1 
    rng = x_range[1] - x_range[0]
    scale = steps / rng
    shift = -x_range[0]*scale
    
    if dither:
        # add some quantization noise
        n = np.random.uniform(
            low  = x_range[0]/steps,
            high = x_range[1]/steps,
            size = x.shape
        )
        x =  x + n
        
    # clip the input data
    x = np.clip(x, x_range[0], x_range[1]) 
    
    # round to integer
    x = np.round(x*scale + shift) - shift
    
    if int_out:
        return x.astype(int)
    else: 
        return x /scale

### TODO: 
# add analog input bandwidth
# add analog input noise
# add clock jitter
# add DNL / INL
def adc(x, fs: float, fs_adc: float, nbits: int, dither = False):
    """basic ADC model; sample an input signal with simulation sampling rate fs, to an ADC sampling rate fs/nsamples
    the full input amd output scale is assumed -1 ... +1
    the input signal is clipped.
    The output sampling rate will be fs / nsamples
    dither is useful in case harmonic signals are used, this spreads out the quantization noise floor better
    
    Args:
        x : ndarray, Shape (N,) or (N,M) input data
        fs (float): sampling rate of the input signal [Hz]
        fs_adc (float): sampling rate of the adc.  fs / fs_adc must be integer.
        nbits (int): number of quantization nbits.
        dither (bool, optional): add quantization noise before actual quantization (default False).

    Returns:
         y : ndarray, sampled signal
    """
   
    nsamples = fs / fs_adc
    assert int(nsamples)>=1 and np.isclose(nsamples, int(nsamples)), "the ADC sampling rate must be so 'fs_adc = fs / nsamples' where nsamples is an integer"
    nsamples = int(nsamples)

    x = downsample(x, nsamples)    
    return quantize(x, nbits, x_range = (-1.0, 1.0), int_out = False, dither=dither)

### TODO: 
# add analog output bandwidth
# add analog output noise
# add clock jitter
# add DNL / INL
def dac(x, fs_dac: float, fs: float, nbits: int, dither = False):
    """basic DAC model; sample an input signal with simulation sampling rate fs, to an ADC sampling rate fs/nsamples
    the full input amd output scale is assumed -1 ... +1
    the input signal is clipped.
    dither is useful in case harmonic signals are used, this spreads out the quantization noise floor better

    Args:
        x : ndarray, Shape (N,) or (N,M) input data
        fs_dac (float): sampling rate of the input signal.  
        fs (float): sampling rate of the oputput signal [Hz].  fs / fs_dac must be integer.
        nbits (int): number of quantization nbits.
        zoh : bool, if True, the samples will be repeated, if false, zeros are inserted
        dither (bool, optional): add quantization noise before actual quantization (default False).

    Returns:
         y : ndarray, sampled signal
    """
    #make sure x is an array with dimension (N, M)
    x = np.asarray(x)
    if x.ndim == 1:  x = x[:, None]
    
    nsamples = fs / fs_dac
    assert int(nsamples)>=1 and np.isclose(nsamples, int(nsamples)), "the DAC sampling rate must be so 'fs_adc = fs / nsamples' where nsamples is an integer"
    nsamples = int(nsamples)

    x = quantize(x, nbits, x_range = (-1.0, 1.0), int_out = False, dither=dither)
    
    return upsample(x, nsamples, zoh = True)
    
