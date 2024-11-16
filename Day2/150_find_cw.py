import sys
import pyvisa
from   time      import sleep,time
import numpy as np
import matplotlib.pyplot as plt

def read_trace(sa):
    # Query the instrument for the trace data
    sa.write(':FORM:DATA ASCII')
    sa.write(':TRAC? TRACE1')
    # Read the ascii data
    raw_data = sa.read()
    # Convert the string data to a numpy array
    y = np.array([float(x) for x in raw_data.split(',')])

    # Get the current frequency settings
    start_freq = float(sa.query(':SENS:FREQ:START?'))
    stop_freq = float(sa.query(':SENS:FREQ:STOP?'))
    num_points = int(sa.query(':SENS:SWE:POIN?'))

    # Calculate frequency points
    f = np.linspace(start_freq * 1e-6, stop_freq * 1e-6, num_points)

    plt.plot(f,y)
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Power (dBm)')
    plt.title('Spectrum Analyzer')
    plt.grid()
    plt.show()

    ii  = np.argmax(y)
    f   = f[ii]
    y   = y[ii]
    return f, y

if __name__ == "__main__":
    import matplotlib
    matplotlib.use('TkAgg')
    plt.ion()

    # Connect to the instrument
    try:
        rm      = pyvisa.ResourceManager('@py')
        ip      = '10.0.0.14'
        sa      = rm.open_resource(f'TCPIP0::{ip}::inst0::INSTR')

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
    f,p = read_trace(sa)

    # Set the refrence level to the maximum
    max_level = np.ceil(p/5 + 1)*5
    sa.write(f"DISP:WIND:TRAC:Y:RLEV {max_level}")

    # Find the center frequency
    Fc  = f    # Center frequency in MHz

    Fspan = np.logspace(2, -1, 4) # Span in MHz

    for span in Fspan:
        sa.write(f"sense:FREQuency:CENTer {Fc} MHz")
        sa.write(f"sense:FREQuency:SPAN {span} MHz")
        sleep(2)
        f,p = read_trace(sa)
        Fc  = f
        print(f'Center Frequency: {Fc} MHz, Span: {span} MHz, Peak: {p} dBm')

    # print the last RBW
    rbw_fine = sa.query("sense:BANDwidth:RESolution?")
    print(f'Last RBW: {float(rbw_fine.strip()):.2f} Hz')

    # Close the connection
    sa.close()
    rm.close()

        
