from PyQt6.QtCore       import QThread, pyqtSignal
import numpy as np


class LongProcess(QThread):
    # Define signals as class attributes (for progressbar and returned data)
    progress    = pyqtSignal(int)
    data        = pyqtSignal(np.ndarray, np.ndarray)
    log         = pyqtSignal(str)

    def __init__(self, sa , sg, f_scan):
        super().__init__()
        self.sa         = sa
        self.sg         = sg
        self.f_scan     = f_scan

        self.running    = False

    def run(self):
        # Save the instrument attributes for recall at the end of the scan
        self.running = True
        self.log.emit("Thread: Starting scan")

        # Set RF output on
        self.sg.write(":OUTPUT:STATE ON")
        self.sg.write(":OUTPUT:MOD:STATE OFF")
        # set the RBW
        self.sa.write("sense:BANDwidth:RESolution 0.1 MHz")
        self.sa.write("sense:DETEctor AVERage")
        # Trace Clear/write mode
        self.sa.write("TRACe:MODE WRITe")
        self.sa.write("INITiate:CONTinuous OFF")

        # Create a list to store the scan data
        power = np.array([])
        freq  = np.array([])
        for i, f in enumerate(self.f_scan):
            # Set the SG to the frequency of the current scan point
            self.sg.write(f"freq {f} MHz")
            # Set the SA center frequency
            self.sa.write(f"sense:FREQuency:CENTer {f} MHz")
            # Set the span
            self.sa.write(f"sense:FREQuency:SPAN 5 MHz")
            # Initiate a single sweep
            self.sa.write("INITiate:IMMediate")
            self.sa.query("*OPC?")
            # Set marker to peak
            self.sa.write("CALCulate:MARKer:MAXimum")
            # Get the peak value
            peak_value = float(self.sa.query("CALCulate:MARKer:Y?").strip())
            # Set the reference level
            max_level  = np.ceil( peak_value/10 + 1)*10
            set_level  = float(self.sa.query(f"DISP:WIND:TRAC:Y:RLEV?").strip() )
            if set_level != max_level:
                self.log.emit(f"Thread: Setting reference level to {max_level}")
            self.sa.write(f"DISP:WIND:TRAC:Y:RLEV {max_level}")
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

