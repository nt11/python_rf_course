import sys
import pyvisa
from time import sleep, time
import numpy as np

def read_max_peak(sa):
    # Set marker to maximum peak
    sa.write("CALC:MARK:MAX")
    sleep(0.1)
    # Query the marker frequency
    f = float(sa.query("CALC:MARK:X?").strip())*1e-6
    # Query the marker power
    y = float(sa.query("CALC:MARK:Y?").strip())

    return f, y


if __name__ == "__main__":
    # Connect to the instrument
    try:
        rm = pyvisa.ResourceManager('@py')
        ip = '10.0.0.14'
        sa = rm.open_resource(f'TCPIP0::{ip}::inst0::INSTR')

        # Query the signal generator name
        sa.write("*IDN?")
        idn = sa.read().strip()
        # <company_name>, <model_number>, <serial_number>,<firmware_revision>
        # Remove the firmware revision
        idn = idn.split(',')[0:3]
        idn = ', '.join(idn)
        print(f'Connected to {idn}')
    except pyvisa.errors.VisaIOError:
        print(f'Failed to connect to the instrument at {ip}')
        sys.exit(1)

    # Reset and clear all status (errors) of the spectrum analyzer
    sa.write("*RST")
    sa.write("*CLS")
    # Set the spectrum analyzer to maximal span
    sa.write("sense:FREQuency:SPAN:FULL")
    # Set auto resolution bandwidth
    sa.write("sense:BANDwidth:RESolution:AUTO ON")
    # Set the trace to max hold
    sa.write(":TRACe1:TYPE WRITe")
    # Set the detector to positive peak
    sa.write("sense:DETEctor POSitive")
    # Set the sweep mode to single sweep
    sa.write("INITiate:CONTinuous ON")

    # Wait for the sweep to complete
    sleep(2)

    f, p = read_max_peak(sa)

    # Set the refrence level to the maximum
    max_level = np.ceil(np.max(p) / 5 + 1) * 5
    sa.write(f"DISP:WIND:TRAC:Y:RLEV {max_level}")

    # Find the center frequency
    Fc = f  # Center frequency in MHz

    Fspan = np.logspace(2, -2, 5)  # Span in MHz

    for span in Fspan:
        sa.write(f"sense:FREQuency:CENTer {Fc} MHz")
        sa.write(f"sense:FREQuency:SPAN {span} MHz")
        sleep(2)
        f, p = read_max_peak(sa)

        ii = np.argmax(p)
        Fc = f
        print(f'Center Frequency: {Fc} MHz, Span: {span} MHz, Peak: {p} dBm')

    # print the last RBW
    rbw_fine = sa.query("sense:BANDwidth:RESolution?")
    print(f'Last RBW: {float(rbw_fine.strip()):.2f} Hz')

    # Close the connection
    sa.close()
    rm.close()