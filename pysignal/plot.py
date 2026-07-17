import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, AutoMinorLocator
from scipy.signal import periodogram


def subplots(nrows, ncols, **varargs):
    """wrapper function around plt.subplots
    use with (nrows, ncols) plot windows
    """
    
    # set default arguments
    args = { 'figsize' : (13, 6.5) }    
    args.update(varargs)

    # default settings
    plt.rcParams.update({
        'font.size': 8,
        'axes.titlesize': 9,
        'axes.labelsize': 8,
        'xtick.labelsize': 7,
        'ytick.labelsize': 7,
        'legend.fontsize': 7,
        'figure.titlesize': 10,
        'axes.labelpad': 1,
        'xtick.major.pad': 1,
        'ytick.major.pad': 1,
        'axes.titley': 0.99,
    })    
    
    fig, axes = plt.subplots(nrows, ncols, **args)
    
    fig.subplots_adjust(
        top=0.96,
        bottom=0.06,
        left=0.05,
        right=0.98,
        hspace=0.19,
        wspace=0.09,
    )

    return fig, axes

def axes(ax, title = ""):
    """select and decorate axes, a bit nicer than the default of Maplotlib
    example:
    
    fig, ax = plt.subplots(squeeze = False)
    ps.nice_axes(ax)
    """
    
    # set current axes
    plt.sca(ax)
    ax.minorticks_on()
    ax.grid(True)
    ax.legend()

    ax.xaxis.set_major_locator(
        MaxNLocator(
            nbins=14,                 # approximate number of major intervals
            steps=[1, 2, 5, 10]        # only allow nice engineering steps
        )
    )

    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.ticklabel_format(axis='x', style='sci', scilimits=(0, 0))

    ax.grid(True, which='major', linestyle='-', alpha=0.7)
    ax.grid(True, which='minor', linestyle=':', alpha=0.4)

    ax.tick_params(labelsize=8)
    ax.xaxis.label.set_size(8)
    ax.yaxis.label.set_size(8)
    
    if title:
        plt.title(title)

def varrow(x, text):
    """print a vertial arrow at position x, with a label text"""
        
    ax = plt.gca()
    ymin, ymax = ax.get_ylim()
    ymax = ymin + (ymax - ymin) * 0.95
    
    ax.annotate(
        "",
        xy=(x, ymax),
        xytext=(x, ymin),
        arrowprops=dict(
            color="black",
            arrowstyle="->",
            lw=2
        )
    )

    if text:
        ax.text(x, ymax, text, ha="center")

def plot_t(x, fs, **varargs):
    """
    Plot time domain singals

    Args:
    x : ndarray,  Shape (N,) or (N,M)
    fs : float, Sampling rate [Hz]
    varags:  other arguments are passed to the plot function    
    """

    x = np.asarray(x)
    # Convert (N,) -> (N,1)
    if x.ndim == 1:
        x = x[:, None]
    N, M = x.shape

    t = np.arange(N) / fs
    plt.plot(t,x, **varargs)
    plt.xlabel('t [s]')
        
def plot_fft(x, fs, **varargs):
    """
    Plot FFT as amplitude in dB for one or more signals

    Parameters
    ----------
    x : ndarray
        Shape (N,) or (N,M)
    fs : float
        Sampling rate [Hz]
    varags:  other arguments are passed to the plot function
    """

    x = np.asarray(x)

    # Convert (N,) -> (N,1)
    if x.ndim == 1:
        x = x[:, None]

    N, M = x.shape

    # FFT of all columns
    X = np.fft.fftshift(
        np.fft.fft(x, axis=0),
        axes=0
    )/N

    f = np.fft.fftshift(
        np.fft.fftfreq(N, d=1/fs)
    )

    for k in range(M):

        f_plot = f
        X_plot = X[:, k]

        plt.plot(
            f_plot,
            20 * np.log10(abs(X_plot) + 1e-30),
            **varargs
        )

    if np.all(np.isreal(x)):
        plt.xlim((0, fs/2))
    else:
        plt.xlim((-fs/2, fs/2))

    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Amplitude [dB]")



def plot_PSD(x, fs: float, Nbins: int =None, window='flattop', scaling = 'density', return_onesided: bool = True, **varargs):
    """plot a power spectral density (periodogram)
        
    real data will be plotted single-sided, and the power of the negative frequencies are added

    Args:
        x : ndarray,  Shape (N,) or (N,M)
        fs : float, Sampling rate [Hz]
        Nbins : int, Displayed number of bins.  The power will be averaged inside the bins. If None, use the native periodogram resolution.
        window: 'flattop', 'boxcar', Window passed to scipy.signal.periodogram()
        scaling: 'density' or 'spectrum'
        return_onesided: bool:  if True return only positive frequencies.  Will be overridden by False if the data is complex
        varags:  other arguments are passed to the plot function    
        
    Return:
        df: frequency bin width
    """
    #Nbins=512
    x = np.asarray(x)
    
    if x.ndim == 1:
        x = x[:, None]

    if all(np.iscomplex(x)):
        return_onesided = False

    f, Pxx = periodogram(
        x,
        fs,
        window = window,
        scaling = scaling,
        return_onesided = return_onesided,
        axis=0
    )
    Nfreq, M = Pxx.shape

    if Nbins is not None and Nbins <= (Nfreq//2):

        group = Nfreq // Nbins  # number of samples per group

        # discard incomplete final group
        Nuse = (Nfreq // group) * group

        f = f[:Nuse].reshape(-1, group).mean(axis=1)

        # average linear powers (never average dB values)
        Pxx = Pxx[:Nuse].reshape(-1, group, M).mean(axis=1)

    df = f[1] - f[0]
    
    if not return_onesided:
        Pxx = np.fft.fftshift(Pxx)
        f = np.fft.fftshift(f)

    plt.plot(f, 10*np.log10(Pxx), **varargs)
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("PSD [dB/Hz]")

    return df


# def plot_psd(x, fs, Nbins=500, **varargs):
#     """
#     Plot PSD of one or more signals.

#     Parameters
#     ----------
#     x : ndarray
#         Shape (N,) or (N,M)
#     fs : float
#         Sampling rate [Hz]
#     Nbins : int
#         Number of displayed points.
#     varags:  other arguments are passed to the plot function
#     """

#     x = np.asarray(x)

#     # Convert (N,) -> (N,1)
#     if x.ndim == 1:
#         x = x[:, None]

#     N, M = x.shape

#     # FFT of all columns
#     X = np.fft.fftshift(
#         np.fft.fft(x, axis=0),
#         axes=0
#     )

#     f = np.fft.fftshift(
#         np.fft.fftfreq(N, d=1/fs)
#     )

#     # PSD [W/Hz]
#     Pxx = np.abs(X)**2 / (N * fs)

#     for k in range(M):

#         f_plot = f
#         P_plot = Pxx[:, k]

#         # Re-bin for display only
#         group = len(P_plot) // Nbins

#         if group > 1:
#             n = group * Nbins

#             f_plot = (
#                 f_plot[:n]
#                 .reshape(Nbins, group)
#                 .mean(axis=1)
#             )

#             P_plot = (
#                 P_plot[:n]
#                 .reshape(Nbins, group)
#                 .mean(axis=1)
#             )

#         plt.plot(
#             f_plot,
#             10 * np.log10(P_plot + 1e-30),
#             label=f"Signal {k}",
#             **varargs
#         )

#     if np.all(np.isreal(x)):
#         plt.xlim((0, fs/2))
#     else:
#         plt.xlim((-fs/2, fs/2))

#     plt.xlabel("Frequency [Hz]")
#     plt.ylabel("PSD [dB/Hz]")

