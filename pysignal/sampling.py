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
    return x[::nsamples]

def quantize(x, nbits: int, x_range = (-1.0, 1.0), int_out: bool = False):
    """Quantize and clip a signal

    Args:
        x : ndarray, Shape (N,) or (N,M) input data
        nbits (int): number of quantization nbits.
        x_range (float, float): (minimum, maximum) input range of x, outside range will be clipped.  
        int_out (bool, optional): if True, then the output will be simple integers from 0 ... 2**nbits-1
        signed (bool, optional): _description_. Defaults to True.
    """
    #make sure x is an array with dimension (N, M)
    x = np.asarray(x)
    if x.ndim == 1:  x = x[:, None]
    
    # clip the input data
    x = np.clip(x, x_range[0], x_range[1]) 
    
    steps = 2**nbits-1 
    rng = x_range[1] - x_range[0]
    scale = steps / rng
    shift = -x_range[0]*scale
    
    # round to integer
    x = np.round(x*scale + shift) - shift
    
    if int_out:
        return x.astype(int)
    else: 
        return x /scale

### TODO: 
# add analog input bandwidth
# add clock jitter
# add DNL / INL
def adc(x, fs: float, fs_adc: float, nbits: int, dither = False):
    """basic ADC model; sample an input signal with simulation sampling rate fs, to an ADC sampling rate fs/nsamples
    the full input amd output scale is assumed -1 ... +1
    the input signal is clipped.
    The output sampling rate will be fs / nsamples

    Args:
        x : ndarray, Shape (N,) or (N,M) input data
        fs (float): sampling rate of the input signal [Hz]
        fs_adc (float): sampling rate of the adc.  fs / fs_adc must be integer.
        nbits (int): number of quantization nbits.
        dither (bool, optional): add quantization noise instead of perfrming actual quantization (default False). Defaults to False.

    Returns:
         y : ndarray, sampled signal
    """
    #make sure x is an array with dimension (N, M)
    x = np.asarray(x)
    if x.ndim == 1:  x = x[:, None]
    
    nsamples = fs / fs_adc
    assert int(nsamples)>=1 and np.isclose(nsamples, int(nsamples)), "the ADC sampling rate must be so 'fs_adc = fs / nsamples' where nsamples is an integer"
    
    nsamples = int(nsamples)

    x = x[::nsamples]  # decimate
    
    q = 2**nbits
    if dither:
        # add some quantization noise
        n = np.random.uniform(
            low  = -1/q,
            high = +1/q,
            size = x.shape
        )
        x =  x + n
    
    return quantize(x, nbits)
    
