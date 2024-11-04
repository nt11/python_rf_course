# create a controlled narrow bandwidth signal generator
# implement a function that generate a QPSK  (QAM4) symbols
# and interolate by a raised cosine filter
# The function receives the following parameters:
# Fs - sampling frequency
# BW - bandwidth
# N - number of symbols


from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.signal import upfirdn
import matpie as mp
import numpy as np


def rcosdesign(beta, span, sps, shape='sqrt'):
    """
    Design a raised cosine FIR filter, similar to MATLAB's rcosdesign.

    Parameters:
    -----------
    beta : float
        Roll-off factor (0 <= beta <= 1)
    span : int
        Number of symbols to span
    sps : int
        Number of samples per symbol (oversampling factor)
    shape : str
        'normal' for raised cosine, 'sqrt' for root raised cosine

    Returns:
    --------
    h : ndarray
        Filter coefficients
    """
    if not 0 <= beta <= 1:
        raise ValueError('Beta must be between 0 and 1')

    # Create time vector
    n = np.arange(-span * sps / 2, span * sps / 2 + 1)
    t = n / sps

    # Handle special cases
    if beta == 0:
        h = np.sinc(t)
    else:
        if shape.lower() == 'sqrt':
            # Root raised cosine
            with np.errstate(divide='ignore', invalid='ignore'):
                num = np.sin(np.pi * t * (1 - beta)) + 4 * beta * t * np.cos(np.pi * t * (1 + beta))
                den = np.pi * t * (1 - (4 * beta * t) ** 2)
                h = np.where(t == 0,
                             1 - beta + 4 * beta / np.pi,
                             np.where(np.abs(t) == 1 / (4 * beta),
                                      beta / np.sqrt(2) * ((1 + 2 / np.pi) * np.sin(np.pi / (4 * beta)) + \
                                                           (1 - 2 / np.pi) * np.cos(np.pi / (4 * beta))),
                                      num / den))
        else:
            # Normal raised cosine
            with np.errstate(divide='ignore', invalid='ignore'):
                h = np.where(np.abs(t) == 1 / (2 * beta),
                             np.pi / 4 * np.sinc(1 / (2 * beta)),
                             np.sinc(t) * np.cos(np.pi * beta * t) / (1 - (2 * beta * t) ** 2))

    # Normalize to unit energy
    return h / np.sqrt(np.sum(h ** 2))


def xrandn_bw(Fs: float, BW: float, N: int)->Tuple[np.ndarray, np.ndarray]:
    I   = np.floor(Fs/BW) # Interpolation factor used as the sps of the raised cosine filter
    # Generate the QPSK symbols
    sym = np.exp(1j*2*np.pi*np.random.randint(0,4,N)/4)
    # Interpolate the symbols by I by using the raised cosine filter
    # Design the raised cosine filter
    # Generate the raised cosine filter
    rc_filter = rcosdesign(beta=0.125, span=20, sps=I, shape='normal')

    # Interpolate (QPSK) symbols using the raised cosine filter
    y  = upfirdn(rc_filter, sym , I, 1)

    # Resample the signal to the desired sampling frequency
    if Fs/BW != I:
        y = mp.resample(y, Fs/BW, I)

    return y, sym


# Test the function
if __name__ == '__main__':
    # MATLAB Like behavior.
    matplotlib.use('TkAgg')
    plt.ion()
    Fs      = 20 # Hz
    BW      = 2.5  # Hz
    N       = 5000
    y, sym  = xrandn_bw(Fs, BW, N)
    mp.psa(y, Fs, 0.1, PLOT = True)


