import sys
import pyvisa
from time import sleep, time
import numpy as np
import matplotlib.pyplot as plt


def set_defaults(sa):
    # Reset and clear all status (errors) of the spectrum analyzer
    sa.write("*RST")
    sa.write("*CLS")
    # Set auto resolution bandwidth
    sa.write("sense:BANDwidth:RESolution:AUTO ON")
    # Set the trace to max hold
    sa.write(":TRACe1:TYPE MAXHold")
    # Set the detector to positive peak
    sa.write("sense:DETEctor POSitive")
    # Set the sweep mode to single sweep
    sa.write("INITiate:CONTinuous OFF")

def wait_for_sweep(sa, timeout_seconds=10):
    """
    Wait for a single sweep to complete on a Keysight Signal Analyzer

    Args:
        timeout_seconds: Maximum time to wait for sweep completion

    Returns:
        bool: True if sweep completed, False if timeout occurred
    """
    # enable sweep bit monitoring (bit 4) for a single sweep
    sa.write(":STAT:OPER:ENAB 16")  # Enable bit 4 (sweep bit)

    # Clear registers
    sa.query(":STAT:OPER:EVEN?")  # Clear by reading
    sa.write("*CLS")  # Clear all status registers

    # Start the sweep
    sa.write(":INIT:IMM")
    sa.write("*WAI")

    start_time = time()
    while (time() - start_time) < timeout_seconds:
        # Query the Operation Event Register
        # catch any errors
        try:
            message = sa.query(":STAT:OPER:EVEN?").strip()
        except pyvisa.errors.VisaIOError:
            sleep(.1)
            set_defaults(sa)
            message = '0'
            continue

        status = int(message)

        # Check if bit 4 (sweep complete) is set (16 in decimal)
        if status & 16:
            return True

        # Wait a short time before polling again
        sleep(.1)

    return False


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
    import matplotlib

    matplotlib.use('TkAgg')
    plt.ion()

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


    # Set the spectrum analyzer to maximal span
    sa.write("sense:FREQuency:SPAN:FULL")
    set_defaults(sa)

    # Wait for the sweep to complete
    if not wait_for_sweep(sa):
        print("Timeout waiting for sweep")
        sys.exit(1)

    Fc, p = read_max_peak(sa)

    # Set the refrence level to the maximum
    max_level = np.ceil(np.max(p) / 5 + 1) * 5
    sa.write(f"DISP:WIND:TRAC:Y:RLEV {max_level}")

    Fspan = np.logspace(2, -1, 4)  # Span in MHz

    for span in Fspan:
        sa.write(f"sense:FREQuency:CENTer {Fc} MHz")
        sa.write(f"sense:FREQuency:SPAN {span} MHz")

        # Wait for the sweep to complete
        if not wait_for_sweep(sa):
            print("Timeout waiting for sweep")
            sys.exit(1)

        Fc, p = read_max_peak(sa)
        print(f'Center Frequency: {Fc} MHz, Span: {span} MHz, Peak: {p} dBm')

    # Close the connection
    sa.close()
    rm.close()