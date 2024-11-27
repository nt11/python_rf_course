# Loading the VSG ARB module with a custom waveform
import pyarbtools as arb

# Test the function
if __name__ == '__main__':
    # Generate an iqdata signal
    iqdata = ...
    name = 'name_of_signal'
    Fs      = 20e6 # Hz Sampling frequency

    # Create ARB object
    mxg_ip  = '10.0.0.14'

    # Generate
    sigarb  = arb.instruments.VSG(mxg_ip, timeout=3)
    sigarb.configure(fs=Fs, iqScale=70 )
    sigarb.download_wfm(iqdata, wfmID='name')

    sigarb.set_cf(1e9)
    sigarb.set_fs(Fs)
    sigarb.set_alcState(0)

    sigarb.play(name)


