import  sys
import  pyvisa
import  pyvisa_py
import  time
import  numpy as np


def read_max_peak(sa):
    # Set marker to maximum peak
    sa.write("CALC:MARK:MAX")
    time.sleep(0.01)
    # Query the marker frequency
    f = float(sa.query("CALC:MARK:X?").strip())*1e-6
    # Query the marker power
    y = float(sa.query("CALC:MARK:Y?").strip())

    return f, y


if __name__ == "__main__":
    # Connect to the instrument
    try:
        rm = pyvisa.ResourceManager('@py')
        ip = '10.0.0.16'
        sa = rm.open_resource(f'TCPIP0::{ip}::inst0::INSTR')
        # Query the signal generator name
        # <company_name>, <model_number>, <serial_number>,<firmware_revision>
        print(f'Connected to {','.join(sa.query("*IDN?").strip().split(',')[0:3])}')
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
    sa.write("INITiate:CONTinuous OFF")
    # Start the sweep
    sa.write("INITiate:IMMediate")
    # Wait for the sweep to complete
    sa.write("*OPC?")
    # Read the maximum peak (frequency and power)
    Fc, p = read_max_peak(sa)

    # Set the refrence level to the maximum
    max_level = np.ceil(np.max(p) / 5 + 1) * 5
    sa.write(f"DISP:WIND:TRAC:Y:RLEV {max_level}")

    # Set the span to 100 MHz, 10 MHz, 1 MHz, 100 kHz, 10 kHz
    Fspan = np.logspace(2, -2, 5)  # Span in MHz

    for span in Fspan:
        sa.write(f"sense:FREQuency:CENTer {Fc} MHz")
        sa.write(f"sense:FREQuency:SPAN {span} MHz")
        sa.write("INITiate:IMMediate")
        # Wait for the sweep to complete
        sa.write("*OPC?")
        Fc, p = read_max_peak(sa)
        print(f'Center Frequency: {Fc} MHz, Span: {span} MHz, Peak: {p} dBm')

    # print the last RBW
    rbw_fine = sa.query("sense:BANDwidth:RESolution?")
    print(f'Last RBW: {float(rbw_fine.strip()):.2f} Hz')

    # Close the connection
    sa.close()
    rm.close()