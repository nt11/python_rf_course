import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import time

if __name__ == '__main__':
    # TkAgg is the backend for matplotlib
    import matplotlib
    matplotlib.use('TkAgg')
    plt.ion()

    print("Results")
    print("-------")
    rm = pyvisa.ResourceManager('@py')

    try:
        # Connect to instrument
        instr = rm.open_resource('TCPIP::10.0.0.7::INSTR')
        instr.timeout = 5000

        # Basic IEEE-488.2 commands
        idn = instr.query('*IDN?')  # Get ID
        manufacturer, model, serial, firmware = idn.strip().split(',')

        print(f"Manufacturer: {manufacturer}")
        print(f"Model: {model}")
        print(f"Serial Number: {serial}")
        print(f"Firmware Version: {firmware}")

        instr.write('FREQ:CENT 1 GHz'               ) # Set center frequency to 1 GHz
        instr.write('FREQ:SPAN 30 MHz'              ) # Set span to 30 MHz
        instr.write('DISP:WIND:TRAC:Y:RLEV -40'     ) # Set reference level to 0 dBm
        instr.write('BAND:RES 0.1 MHz'              ) # Set RBW to 0.1 MHz
        instr.write(':DETector:TRACe1 AVERage'      ) # Set detector to average
        instr.write(':TRACe1:TYPE WRIT'             ) # Set trace to write
        instr.write('SWE:POIN 3001'                 ) # Set number of points to 3 001

        # Read all the above settings and print them
        cf_ghz      = float(instr.query('FREQ:CENT?'            ).strip())*1e-9
        span_mhz    = float(instr.query('FREQ:SPAN?'            ).strip())*1e-6
        ref_level   = float(instr.query('DISP:WIND:TRAC:Y:RLEV?').strip())
        rbw_mhz     = float(instr.query('BAND:RES?'             ).strip())*1e-6
        detector    =       instr.query(':DETector:TRACe1?'     ).strip()
        trace       =       instr.query(':TRACe1:TYPE?'         ).strip()

        print(f"Center Frequency: {cf_ghz:.2f} GHz")
        print(f"Span: {span_mhz:.2f} MHz")
        print(f"Reference Level: {ref_level:.2f} dBm")
        print(f"RBW: {rbw_mhz:.2f} MHz")
        print(f"Detector: {detector}")
        print(f"Trace: {trace}")

        time.sleep(1)

        # Get trace data in ascii format
        instr.write(':FORM:DATA ASCII')
        instr.write(':TRAC? TRACE1')
        data_str = instr.read()
        data_list = data_str.split(',')
        data_list = [float(val) for val in data_list]
        # define frequency axis
        freq = np.linspace(cf_ghz*1e-3 - span_mhz/2, cf_ghz*1e-3 + span_mhz/2, len(data_list))

        # Plot the trace
        plt.plot(freq, data_list)
        plt.xlabel('Frequency (MHz)')
        plt.ylabel('Amplitude (dBm)')
        plt.title('Spectrum Analyzer Trace')
        plt.show()

    except pyvisa.errors.VisaIOError as e:
        print(f"Error: {e}")
    finally:
        print("Closing connection")
        instr.write('*CLS')
        instr.close()
        rm.close()

