# Design a function that receives
# BW (bandwidth) Ntones (Number of tones) Fs (Sampling frequency) Nfft (FFT size)
# The function will design in the frequency domain and returns the multi-tone time domain signal.
# Thus, creating a multi-tone periodic signal in the time domain.

from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt

def mutitone(BW: float, Ntones: int, Fs: float, Nfft: int = 4096)->Tuple[np.ndarray, np.ndarray, np.ndarray]:
    # Generate the frequency vector (symmetric around DC)
    f = np.linspace(-BW / 2, BW / 2, Ntones)
    # Generate the amplitude vector
    A = np.ones(Ntones)
    # Generate a random phase vector
    phi = np.random.rand(Ntones) * 2 * np.pi
    # Initialize the frequency domain vector to zeros
    X = np.zeros(Nfft, dtype=complex)
    # Generate the frequency domain signal (with frequency f rounded to the nearest bin)
    for i in range(Ntones):
        # Calculate the bin index for the frequency f[i] whie the DC bin is at the center
        bin_index = int(np.round(f[i] / Fs * Nfft)) + Nfft // 2
        # Set the amplitude and phase
        X[bin_index] = A[i] * np.exp(1j * phi[i])
    # Generate the time domain signal
    x = np.fft.ifft(X)
    F = -Fs / 2 + Fs / Nfft * np.arange(Nfft)
    return x / np.max(np.abs(x)) , X , F

# Test the function
if __name__ == '__main__':
    BW      = 3 # MHz
    Ntones  = 5
    Fs      = 20 # MHz

    x, X, F = mutitone(BW, Ntones, Fs)

    plt.figure()
    plt.plot(F, np.abs(X))
    plt.title('Frequency Domain')
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Magnitude')
    plt.grid()

    plt.figure()
    # Plot the real part and the imaginary part
    # with x-axis as the periods spans from 0 to 3 (repeat the vector 3 times)
    p = np.arange(0, 3, 1 / len(x))
    plt.plot(p,np.real(np.tile(x, 3)), label='Real')
    plt.plot(p,np.imag(np.tile(x, 3)), label='Imaginary')
    plt.title('Time Domain')
    plt.xlabel('Periods')
    plt.grid()
    plt.show()
