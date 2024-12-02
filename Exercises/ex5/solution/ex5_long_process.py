from PyQt6.QtCore       import QThread, pyqtSignal
import numpy as np


class LongProcess(QThread):
    # Define signals as class attributes (for progressbar and returned data)
    progress    = pyqtSignal(int)
    data        = pyqtSignal(np.ndarray, np.ndarray)
    log         = pyqtSignal(str)

    def __init__(self, f_scan,scpi_sa, scpi_sg):
        super().__init__()
        self.f_scan     = f_scan
        self.scpi_sa    = scpi_sa
        self.scpi_sg    = scpi_sg
        
        self.running    = False

    def run(self):
        # Save the instrument attributes for recall at the end of the scan
        self.running = True
        self.log.emit("Thread: Starting scan")

        # Set RF output on
        self.scpi_sg.write(":OUTPUT:STATE ON")
        self.scpi_sg.write(":OUTPUT:MOD:STATE OFF")
        # set the RBW
        self.scpi_sa.write("sense:BANDwidth:RESolution 0.1 MHz")
        self.scpi_sa.write("sense:DETEctor AVERage")
        # Trace Clear/write mode
        self.scpi_sa.write("TRACe:MODE WRITe")
        self.scpi_sa.write("INITiate:CONTinuous OFF")

        # Create a list to store the scan data
        power = np.array([])
        freq  = np.array([])
        for i, f in enumerate(self.f_scan):
            # Set the SG to the frequency of the current scan point
            self.scpi_sg.write(f"freq {f} MHz")
            # Set the SA center frequency
            self.scpi_sa.write(f"sense:FREQuency:CENTer {f} MHz")
            # Set the span
            self.scpi_sa.write(f"sense:FREQuency:SPAN 5 MHz")
            # Initiate a single sweep
            self.scpi_sa.write("INITiate:IMMediate")
            try:
                self.scpi_sa.query("*OPC?")
            except pyvisa.errors.VisaIOError:
                self.log.emit(f"Thread: OPC Failed at {f} MHz")

            # Set marker to peak
            self.scpi_sa.write("CALCulate:MARKer:MAXimum")
            # Get the peak value
            peak_value = float(self.scpi_sa.query("CALCulate:MARKer:Y?").strip())
            # Set the reference level
            max_level  = np.ceil( peak_value/10 + 1)*10
            set_level  = float(self.scpi_sa.query(f"DISP:WIND:TRAC:Y:RLEV?").strip() )
            if set_level != max_level:
                self.log.emit(f"Thread: Setting reference level to {max_level}")
                self.scpi_sa.write(f"DISP:WIND:TRAC:Y:RLEV {max_level}")
            # save the peak value and frequency
            power = np.append(power, peak_value)
            freq  = np.append(freq, f)

            if i%20==0:
                self.data.emit(freq, power)

            # Update the progress bar
            self.progress.emit(100 * (i + 1) // len(self.f_scan))
            if not self.running:
                break

        # Emit the data signal
        self.data.emit(freq, power)


    def stop(self):
        self.running = False

