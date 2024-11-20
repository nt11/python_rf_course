import pyvisa
import time
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

class SpectrumAnalyzer:
    def __init__(self, visa_address):
        """Initialize connection to spectrum analyzer."""
        try:
            self.rm = pyvisa.ResourceManager('@py')
            self.sa = self.rm.open_resource(visa_address)
            # Set timeout to 20 seconds for long sweeps
            self.sa.timeout = 20000
            # Clear the instrument status
            self.sa.write("*CLS")
            # Reset to known state
            self.sa.write("*RST")
            print(f"Connected to: {self.sa.query('*IDN?')}")
        except Exception as e:
            print(f"Error initializing instrument: {str(e)}")
            raise

    def setup_measurement(self, center_freq_mhz, span_mhz, rbw_hz):
        """Configure the spectrum analyzer settings."""
        try:
            # Set the trace to Clear/Write
            ## self.sa.write(":TRACe1:TYPE WRITe")
            # Set the detector to positive peak
            ##self.sa.write("sense:DETEctor:Trace1 POSitive")

            # Configure frequency settings
            self.sa.write(f":SENSe:FREQuency:CENTer {center_freq_mhz} MHz")
            self.sa.write(f":SENSe:FREQuency:SPAN {span_mhz} MHz")

            # Set Resolution Bandwidth
            self.sa.write(f":SENSe:BANDwidth:RESolution {rbw_hz} Hz")
            # Turn off auto RBW
            self.sa.write(":SENSe:BANDwidth:RESolution:AUTO OFF")

            # Set Video Bandwidth to be 3x RBW (common practice)
            self.sa.write(f":SENSe:BANDwidth:VIDeo {rbw_hz * 3} Hz")
            self.sa.write(":SENSe:BANDwidth:VIDeo:AUTO OFF")

            # Get and print the expected sweep time
            sweep_time = float(self.sa.query(":SENSe:SWEep:TIME?"))
            print(f"Expected sweep time: {sweep_time:.2f} seconds")

        except Exception as e:
            print(f"Error in setup: {str(e)}")
            raise

    def perform_single_sweep(self):
        """Perform a single sweep and wait for completion."""
        try:
            # Set to single sweep mode
            self.sa.write(":INITiate:CONTinuous OFF")

            # Clear data buffer and status
            self.sa.write(":ABORt") # Abort any ongoing sweep
            self.sa.write("*CLS")

            print("Starting sweep...")
            start_time = time.perf_counter()

            # Initiate sweep
            self.sa.write(":INITiate:IMMediate")

            # Wait for operation complete
            response = self.sa.query("*OPC?")

            sweep_duration = time.perf_counter() - start_time
            print(f"Sweep completed in {sweep_duration:.2f} seconds")

            return True

        except pyvisa.VisaIOError as e:
            if e.error_code == pyvisa.constants.StatusCode.error_timeout:
                print("Timeout occurred while waiting for sweep completion")
            else:
                print(f"VISA Error during sweep: {str(e)}")
            return False
        except Exception as e:
            print(f"Error during sweep: {str(e)}")
            return False

    def get_trace_data(self):
        """Read trace data after sweep completion."""
        try:
            # Query trace data PyVISA method for reading numerical data from instruments
            p = self.sa.query_ascii_values(":TRACe:DATA? TRACE1", container=np.array)
            # Build the frequency list
            start_freq  = float(self.sa.query(":FREQuency:START?" ).strip())*1e-6
            stop_freq   = float(self.sa.query(":FREQuency:STOP?"  ).strip())*1e-6
            num_points  =   int(self.sa.query(":SENSe:SWEep:POIN?").strip())
            freq        = np.linspace(start_freq, stop_freq, num_points)

            return p,freq
        except Exception as e:
            print(f"Error reading trace: {str(e)}")
            return None

    def close(self):
        """Close the connection to the instrument."""
        try:
            self.sa.write("*RST")  # Reset instrument before closing
            self.sa.close()
            self.rm.close()
            print("Connection closed")
        except Exception as e:
            print(f"Error closing connection: {str(e)}")


def main():
    # Example usage
    VISA_ADDRESS = "TCPIP0::10.0.0.14::inst0::INSTR"  # Update with your instrument address

    try:
        # Create spectrum analyzer instance
        sa = SpectrumAnalyzer(VISA_ADDRESS)

        # Setup measurement parameters
        CENTER_FREQ = 1111  # 1 GHz
        SPAN        = 50    # 10 MHz
        RBW         = 100   # 100 Hz (fine resolution)

        # Configure the analyzer
        sa.setup_measurement(CENTER_FREQ, SPAN, RBW)

        # Perform sweep and wait for completion
        if sa.perform_single_sweep():
            # Get the trace data
            p,f = sa.get_trace_data()

            # Plot the trace
            plt.plot(f, p)
            plt.xlabel("Frequency (MHz)")
            plt.ylabel("Power (dBm)")
            plt.title("Spectrum Analyzer")
            plt.grid(True)
            plt.show()

        # Clean up
        sa.close()

    except Exception as e:
        print(f"Program error: {str(e)}")


if __name__ == "__main__":
    import matplotlib
    matplotlib.use('TkAgg')
    plt.ion()

    main()