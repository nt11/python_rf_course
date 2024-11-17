import re
import sys
from signal import signal

import pyvisa
import pyarbtools as arb
import yaml
from PyQt6.QtWidgets    import QApplication, QMainWindow, QVBoxLayout
from PyQt6.uic          import loadUi
from PyQt6.QtCore       import QTimer, QThread, pyqtSignal
from time               import sleep, time

import numpy as np

from pyqt2python import h_gui
from plot_widget import PlotWidget
from pyqtgraph.examples.optics import trace


class LongProcess(QThread):
    # Define signals as class attributes (for progressbar and returned data)
    progress    = pyqtSignal(int)
    data        = pyqtSignal(np.ndarray, np.ndarray)

    def __init__(self, vsa):
        super().__init__()
        self.vsa = vsa

    def run(self):
        # Query the instrument attributes to restore them at the end of the scan
        save_rbw        = self.vsa.query("sense:BANDwidth:RESolution?"  )
        save_span       = self.vsa.query("sense:FREQuency:SPAN?"        )
        save_center     = self.vsa.query("sense:FREQuency:CENTer?"      )
        save_trace      = self.vsa.query(":TRACe1:TYPE?"                )
        save_detector   = self.vsa.query("sense:DETEctor?"              )
        # Hi-Res scan of the spectrum analyzer
        fc              = float(save_center.strip())*1e-6 # MHz Center Frequency
        rbw             = 0.01      # MHz Resolution Bandwidth
        span            = 5.0      # MHz Span
        Fstart          = fc -100.0 # MHz Start center Frequency
        Fstop           = fc +100.0 # MHz Stop center Frequency
        Fscan           = np.arange(Fstart, Fstop, span)

        # Calculate the refrence level
        # set the RBW to maximum
        self.vsa.write("sense:BANDwidth:RESolution 8 MHz"   )
        self.vsa.write(f"sense:FREQuency:SPAN {Fstop - Fstart} MHz"     )
        self.vsa.write(":TRACe1:TYPE MAXHold"               )
        self.vsa.write("sense:DETEctor POS"                 )
        sleep(.1)
        # Read the trace data
        # Query the instrument for the trace data
        self.vsa.write(':FORM:DATA ASCII')
        self.vsa.write(':TRAC? TRACE1')
        # Read the ascii data
        raw_data = self.vsa.read()
        # Convert the string data to a numpy array
        trace_data  = np.array([float(x) for x in raw_data.split(',')])
        max_level   = np.ceil( np.max(trace_data)/5 + 1)*5
        # Set the reference level
        self.vsa.write(f"DISP:WIND:TRAC:Y:RLEV {max_level}")

        # Set the scan attributes
        self.vsa.write(f"sense:BANDwidth:RESolution {rbw} MHz"          )
        self.vsa.write(f"sense:FREQuency:SPAN {span} MHz"               )
        self.vsa.write(":TRACe1:TYPE WRITe"                             )
        self.vsa.write("sense:DETEctor AVERage"                         )
        # Set single sweep mode
        self.vsa.write("INITiate:CONTinuous OFF"                        )

        # Create a list to store the scan data
        all_data = []
        all_freq = []
        for i, f in enumerate(Fscan):
            # Set the center frequency
            self.vsa.write(f"sense:FREQuency:CENTer {f} MHz")
            # Initiate a single sweep
            self.vsa.write("INITiate:IMMediate")
            # Wait for the scan to complete by checking the status
            if not self.wait_for_sweep():
                print("Timeout waiting for sweep")
                break

            # Query the instrument for the trace data
            self.vsa.write(':FORM:DATA ASCII')
            self.vsa.write(':TRAC? TRACE1')
            # Read the ascii data
            raw_data = self.vsa.read()

            # Convert the string data to a numpy array
            trace_data = np.array([float(x) for x in raw_data.split(',')])

            # Get the current frequency settings
            start_freq  = float(self.vsa.query(':SENS:FREQ:START?'))
            stop_freq   = float(self.vsa.query(':SENS:FREQ:STOP?' ))
            num_points  =   int(self.vsa.query(':SENS:SWE:POIN?'  ))

            # Calculate frequency points
            f           = np.linspace(start_freq*1e-6, stop_freq*1e-6, num_points)

            # Append the data to the list (in a flattened format)
            all_data = np.concatenate([all_data,trace_data])
            all_freq = np.concatenate([all_freq,f])
            # Update the progress bar
            self.progress.emit(100 * (i + 1) // len(Fscan))

        # Restore the instrument settings
        self.vsa.write(f"sense:BANDwidth:RESolution {save_rbw}"        )
        self.vsa.write(f"sense:FREQuency:SPAN {save_span}"             )
        self.vsa.write(f"sense:FREQuency:CENTer {save_center}"         )
        self.vsa.write(":TRACe1:TYPE {save_trace}"                     )
        self.vsa.write("sense:DETEctor {save_detector}"                )
        # Set continuous sweep mode
        self.vsa.write("INITiate:CONTinuous ON"                        )

        # Emit the data signal
        self.data.emit(all_freq , all_data)


    def stop(self):
        pass

    def wait_for_sweep(self, timeout_seconds=10):
        """
        Wait for a single sweep to complete on a Keysight Signal Analyzer

        Args:
            timeout_seconds: Maximum time to wait for sweep completion

        Returns:
            bool: True if sweep completed, False if timeout occurred
        """
        # enable sweep bit monitoring (bit 4) for a single sweep
        self.vsa.write(":STAT:OPER:ENAB 16")  # Enable bit 4 (sweep bit)

        # Clear registers
        self.vsa.query(":STAT:OPER:EVEN?")  # Clear by reading
        self.vsa.write("*CLS")  # Clear all status registers

        # Start the sweep
        self.vsa.write(":INIT:IMM")
        self.vsa.write("*WAI")

        start_time = time()
        while (time() - start_time) < timeout_seconds:
            # Query the Operation Event Register
            status = int(self.vsa.query(":STAT:OPER:EVEN?"))

            # Check if bit 4 (sweep complete) is set (16 in decimal)
            if status & 16:
                return True

            # Wait a short time before polling again
            time.sleep(0.1)

        return False
