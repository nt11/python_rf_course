import re
import sys
from signal import signal

import pyvisa
import pyarbtools as arb
import yaml
from PyQt6.QtWidgets    import QApplication, QMainWindow, QVBoxLayout
from PyQt6.uic          import loadUi
from PyQt6.QtCore       import QTimer, QThread, pyqtSignal
import time

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
        # Save the instrument attributes for recall at the end of the scan
        self.vsa.write("*SAV 1")
        # Hi-Res scan of the spectrum analyzer
        fc              = float(self.vsa.query(':sens:FREQ:CENT?').strip())*1e-6  # MHz Center Frequency
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
        self.vsa.write("INITiate:CONTinuous OFF"            )
        self.vsa.write("INITiate:IMMediate"                 )
        # Wait for the sweep to complete
        self.vsa.write("*OPC?")
        # Read the trace data
        # Query the instrument for the trace data
        trace_data  = self.vsa.query_ascii_values(':TRAC? TRACE1', container=np.array)
        max_level   = np.ceil( np.max(trace_data)/5 + 1)*5
        # Set the reference level
        self.vsa.write(f"DISP:WIND:TRAC:Y:RLEV {max_level}")

        # Set the hi-res scan attributes
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
            # Wait for the sweep to complete
            # time_start = time.perf_counter()
            self.vsa.query("*OPC?")
            # print(f"Sweep {i+1} completed in {time.perf_counter() - time_start:.2f} seconds")
            # Query the instrument for the trace data
            trace_data = self.vsa.query_ascii_values(':TRAC? TRACE1', container=np.array)

            # Get the current frequency settings
            start_freq  = float(self.vsa.query(':SENS:FREQ:START?'))
            stop_freq   = float(self.vsa.query(':SENS:FREQ:STOP?' ))
            num_points  =   int(self.vsa.query(':SENS:SWE:POIN?'  ))

            # Calculate frequency points
            f           = np.linspace(start_freq*1e-6, stop_freq*1e-6, num_points)

            # Append the data to the list (in a flattened format)
            all_data = np.concatenate([all_data, trace_data  ])
            all_freq = np.concatenate([all_freq, f           ])
            # Update the progress bar
            self.progress.emit(100 * (i + 1) // len(Fscan))

        # Recall the instrument settings
        self.vsa.write("*RCL 1")
        # Set continuous sweep mode
        self.vsa.write("INITiate:CONTinuous ON")

        # Emit the data signal
        self.data.emit(all_freq , all_data)


    def stop(self):
        pass

