# create a controlled narrow bandwidth signal generator
# implement a function that generate a QPSK  (QAM4) symbols
# and interolate by a raised cosine filter
# The function receives the following parameters:
# Fs - sampling frequency
# BW - bandwidth
# N - number of symbols


from typing import Tuple
import matpie as mp
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import upfirdn

def rcosdesign(beta:float, span:float, sps:int, shape:str='sqrt') -> np.ndarray:
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
    '''
    Generate a cyclic narrow band (controlled) signal
    '''
    I   = int(np.floor(Fs/BW)) # Interpolation factor used as the sps of the raised cosine filter
    # Generate the QPSK symbols
    sym_in = np.exp(1j * 2 * np.pi * np.random.randint(0, 4, N) / 4)
    # Interpolate the symbols by I by using the raised cosine filter
    # Design the raised cosine filter
    # Generate the raised cosine filter
    rc_filter = rcosdesign(beta:=0.125, span:=30, sps:=int(I), shape='normal')

    # Interpolate (QPSK) symbols using the raised cosine filter
    sym_cyc = np.concatenate((sym_in[-span*3-1:-1], sym_in, sym_in[0:span*3]))
    y  = upfirdn(rc_filter, sym_cyc, I, 1)
    ii = (len(y) - len(sym_in)*I)//2 + 8*I
    y  = y[ii: ii + len(sym_in)*I]
    # Resample the signal to the desired sampling frequency
    if Fs/BW != I:
        y = mp.resample(y, Fs/BW, I)

    return y


# Test the function
if __name__ == '__main__':
    # MATLAB Like behavior.
    #mp.matlab_like()
    import matplotlib
    matplotlib.use('TkAgg')
    plt.ion()

    Fs      = 20 # Hz
    BW      = 3.33  # Hz
    N       = 5000
    y       = xrandn_bw(Fs, BW, N)
    mp.psa(np.tile(y,10), Fs, 0.1, PLOT = True)




