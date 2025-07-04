import re
import sys

import  pyvisa
import  pyvisa_py

import  yaml
from    PyQt6.QtWidgets    import QApplication, QMainWindow, QVBoxLayout, QTextBrowser
from    PyQt6.uic          import loadUi
from    PyQt6.QtCore       import QTimer

from    time               import sleep

import numpy as np
import logging # for pyinstaller

from python_rf_course.utils.pyqt2python     import h_gui
from python_rf_course.utils.plot_widget     import PlotWidget
from python_rf_course.utils.logging_widget  import setup_logger

from o310_long_process import LongProcess


def is_valid_ip(ip:str) -> bool:
    # Regular expression pattern for matching IP address
    ip_pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return re.match(ip_pattern, ip) is not None


# Suppress logging of specified modules (only show errors)
def suppress_external_logging():
    # List of modules you want to suppress
    suppress_modules = ['pyvisa']

    for module in suppress_modules:
        logging.getLogger(module).setLevel(logging.CRITICAL)
        logging.getLogger(module).propagate = False

# The GUI controller clas inherit from QMainWindow object as defined in the ui file
class LabDemoVsaControl(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the UI file into the Class (LabDemoVsaControl) object
        loadUi("BasicVsaControl_5.ui", self)
        # Change the background color of the main window to grey
        # self.setStyleSheet("background-color: grey;")
        # Create Logger
        self.log = setup_logger(text_browser=self.textBrowser,name='sa_log', level=logging.INFO,is_console=True)
        logging.getLogger('sa_log').propagate = True
        #suppress_external_logging()

        self.setWindowTitle("SA Control")

        # Interface of the GUI Widgets to the Python code
        self.h_gui = dict(
            Connect             = h_gui(self.pushButton_2       , self.cb_connect           ),
            IP                  = h_gui(self.lineEdit_4         , self.cb_ip                ),
            Fc                  = h_gui(self.lineEdit           , self.cb_fc                ),
            RBW                 = h_gui(self.lineEdit_2         , self.cb_rbw               ),
            Span                = h_gui(self.lineEdit_3         , self.cb_span              ),
            Trace               = h_gui(self.comboBox           , self.cb_trace             ),
            Detector            = h_gui(self.comboBox_2         , self.cb_detector          ),
            AutoScale           = h_gui(self.pushButton         , self.cb_autoscale         ),
            HiResSnapshot       = h_gui(self.pushButton_3       , self.cb_hires_snapshot    ),
            HiResProgress       = h_gui(self.progressBar        , None              ),
            Save                = h_gui(self.actionSave         , self.cb_save              ),
            Load                = h_gui(self.actionLoad         , self.cb_load              ),
            Refresh             = h_gui(self.horizontalSlider   , self.cb_refresh           ))

        # Create a Resource Manager object
        self.rm         = pyvisa.ResourceManager('@py')
        self.vsa        = None

        # Load the configuration/default values from the YAML file
        self.Params     = None
        self.file_name  = "vsa_defaults.yaml"
        self.h_gui['Load'].emit() #  self.cb_load

        self.file_name = "last.yaml"
        try:
            self.h_gui['Load'].callback()  # self.cb_load
        except FileNotFoundError:
            self.log.warning("No last.yaml file found")

        self.h_gui['Save'].emit() #  self.cb_save

        # Create a widget for the Spectrum Analyzer plot
        self.plot_sa        = PlotWidget()
        layout              = QVBoxLayout(self.widget)
        layout.addWidget(self.plot_sa)
        # Set the background color of the plot widget to white
        self.plot_sa.set_background_color('white')

        # Create a timer for the Spectrum Analyzer plot
        self.timer          = QTimer()
        self.timer.timeout.connect(self.timer_refresh_plot)
        self.timer.start(self.h_gui['Refresh'].get_val())

    def cb_refresh(self):
        self.timer.setInterval(self.h_gui['Refresh'].get_val())

    def vsa_write(self, cmd:str):
        if self.vsa is not None:
            # Add logging to the write command (Debug Level)
            self.log.debug(f"VSA Write: {cmd}")
            self.vsa.write(cmd)
            # Check for errors
            e = self.vsa.query('SYST:ERR?').strip().split(',')
            if int(e[0]) != 0:
                self.log.error(f"Error: {e[1]}")

    def vsa_query(self, cmd:str):
        if self.vsa is not None:
            # Add logging to the query command (Debug Level)
            self.log.debug(f"VSA Query: {cmd}")
            return self.vsa.query(cmd).strip()

    def vsa_read_trace(self):
        if self.vsa is not None:
            # Query the instrument for the trace data
            trace_id = 1
            # Query trace data PyVISA method for reading numerical data from instruments
            p           = self.vsa.query_ascii_values(":TRACe:DATA? TRACE1", container=np.array)
            # Build the frequency list

            # Get the current frequency settings
            start_freq  = float(self.vsa_query(":FREQuency:START?" ))*1e-6
            stop_freq   = float(self.vsa_query(":FREQuency:STOP?"  ))*1e-6
            num_points  =   int(self.vsa_query(":SENSe:SWEep:POIN?"))
            # Calculate frequency points
            f           = np.linspace(start_freq, stop_freq, num_points)

            return p, f


    # Callback function for the Connect button
    # That is a checkable button
    def cb_connect(self):
        if self.sender().isChecked(): # self.h_gui['Connect'].obj.isChecked():
            self.log.info("Connect button Checked")
            # Open the connection to the signal generator
            try:
                ip              = self.h_gui['IP'].get_val()
                self.vsa        = self.rm.open_resource(f"TCPIP0::{ip}::inst0::INSTR")
                self.vsa.timeout = 60000
                self.log.info(f"Connected to {ip}")
                # Read the signal generator status and update the GUI (RF On/Off, Modulation On/Off,Pout and Fc)
                # Query the signal generator name
                idn         = self.vsa_query("*IDN?")
                # <company_name>, <model_number>, <serial_number>,<firmware_revision>
                # Remove the firmware revision
                idn         = idn.split(',')[0:3]
                idn         = ', '.join(idn)
                self.setWindowTitle(idn)
                # Reset and clear all status (errors) of the spectrum analyzer
                self.vsa_write("*RST")
                self.vsa_write("*CLS")
                sleep(.1)
                # Aligned the spectrum analyzer to the GUI values
                self.cb_fc()
                self.cb_rbw()
                self.cb_span()
                self.cb_trace()
                self.cb_detector()
                # Sweep mode to continuous
                self.vsa_write(":INITiate:CONTinuous ON")

            except Exception:
                self.log.error("Connection failed")
                if self.vsa is not None:
                    self.vsa.close()
                    self.vsa = None
                # Clear Button state
                self.h_gui['Connect'].set_val(False, is_callback=True)
        else:
            self.log.info("Connect button Cleared")
            # Close the connection to the signal generator
            if self.vsa is not None:
                self.vsa.close()
                self.vsa = None


    # Callback function for the IP lineEdit
    def cb_ip(self):
        ip          = self.h_gui['IP'].get_val()
        # Check if the ip is a valid
        if not is_valid_ip(ip):
            self.log.error(f"Invalid IP address: {ip}, Resetting to default")
            ip = self.Params["IP"]
            # Set the default value to the GUI object
            self.h_gui['IP'].set_val(ip)

        self.log.info(f"IP = {ip}")

    # Callback function for the Fc lineEdit
    def cb_fc(self):
        # Check if the frequency is a valid float number
        try:
            frequency_mhz = self.h_gui['Fc'].get_val()
        except ValueError:
            self.log.info(f"Invalid Frequency: Resetting to default")
            frequency_mhz = self.Params["Fc"]
            # Set the default value to the GUI object
            self.h_gui['Fc'].set_val(frequency_mhz)

        self.vsa_write(f"sense:FREQuency:CENTer {frequency_mhz} MHz") # can replace the '} MHz' with '}e6'
        self.log.info(f"Fc = {frequency_mhz} MHz")

    def cb_rbw(self):
        # Check if the frequency is a valid float number
        try:
            rbw = self.h_gui['RBW'].get_val()
        except ValueError:
            self.log.info(f"Invalid RBW: Resetting to default")
            rbw = self.Params["RBW"]
            # Set the default value to the GUI object
            self.h_gui['RBW'].set_val(rbw)

        self.vsa_write(f"sense:BANDwidth:RESolution {rbw} MHz")
        self.log.info(f"RBW = {rbw} MHz")

    def cb_span(self):
        # Check if the frequency is a valid float number
        try:
            span = self.h_gui['Span'].get_val()
        except ValueError:
            self.log.info("Invalid Span: Resetting to default")
            span = self.Params["Span"]
            # Set the default value to the GUI object
            self.h_gui['Span'].set_val(span)

        self.vsa_write(f"sense:FREQuency:SPAN {span} MHz")
        self.log.info(f"Span = {span} MHz")

    def cb_trace(self):
        trace_id = self.h_gui['Trace'].get_val()
        '''
        - 0 - "WRIT" or "CLEAR": Clear Write
        - 1 - "AVER": Average
        - 2 - "MAXH": Maximum hold
        - 3 - "MINH": Minimum hold

        - "VIEW": View
        - "BLAN": Blank
        '''
        trace_number = 1
        trace_mode = ["WRIT", "AVER", "MAXH", "MINH", "VIEW", "BLAN"]
        self.vsa_write(f":TRACe{trace_number}:TYPE {trace_mode[trace_id]}")

    def cb_detector(self):
        detector_id = self.h_gui['Detector'].get_val()
        '''
        detector_type: String specifying the detector type:
        - 0 - "AVER": Average (RMS) detector
        - 1 - "NORM": Normal detector (positive peak for even bins, negative peak for odd bins)
        - 2 - "SAMP": Sample detector
        - "POS": Positive peak detector
        - "NEG": Negative peak detector
        - "QPEAK": Quasi-peak detector (if available)
        - "EAV": EMI Average detector (if available)
        - "RAV": RMS Average detector
        '''
        trace_number = 1
        detector_type = ["AVER", "NORM", "SAMP", "POS", "NEG", "QPEAK", "EAV", "RAV"]
        self.vsa_write(f":DETector:TRACe{trace_number} {detector_type[detector_id]}")

    def cb_autoscale(self):
        """Executes an amplitude autorange in VSA and waits for it to complete using SCPI commands."""
        if self.vsa is not None:
            y_max = -1000
            y_min = 1000
            for i in range(10):
                y,f     = self.vsa_read_trace()
                y_max   = max(y_max, np.max(y))
                y_min   = min(y_min, np.min(y))

            ref_level   = np.ceil(( y_max + 5.0 ) / 5.0) * 5.0
            scale2div   = np.round((ref_level - y_min)/10.0) + 1

            self.vsa_write( f"DISP:WIND:TRAC:Y:PDIV {scale2div}")
            self.vsa_write( f"DISP:WIND:TRAC:Y:RLEV {ref_level}")

    def cb_hires_scan(self,i):
        self.h_gui['HiResProgress'].set_val(i)

    def cb_hires_snapshot(self):
        if self.vsa is not None:
            if self.sender().isChecked():
                self.log.info("HiResSnapshot button Checked")
                self.thread = LongProcess(self.vsa)
                self.thread.progress.connect(self.cb_hires_scan)
                self.thread.data.connect(self.cb_hi_res_plot)

                self.timer.stop()
                self.thread.start() # Start the thread calling the run method
            else:
                self.log.info("HiResSnapshot button Cleared")
                self.thread.stop()
                self.thread.wait()
                self.h_gui['HiResProgress'].set_val(0)
                self.timer.start()


    def timer_refresh_plot(self):
        if self.vsa is not None:
            y,x = self.vsa_read_trace()
            self.plot_sa.plot( x , y ,
                               line='b-' , line_width=4.0,
                               xlabel='Frequency (MHz)', ylabel='Power dBm',
                               title='PSA', xlog=False, clf=True)

    def cb_hi_res_plot(self, freq, power):
            self.plot_sa.plot( freq , power ,
                               line='b-' , line_width=4.0,
                               xlabel='Frequency (MHz)', ylabel='Power dBm',
                               title='Hi-Res PSA', xlog=False, clf=True)

    def cb_save(self):
        self.log.info("Save")
        # Read the values from the GUI objects and save them to the Params dictionary
        for key, value in self.Params.items():
            if key in self.h_gui:
                self.Params[key] = self.h_gui[key].get_val()

        with open(self.file_name, "w") as f:
            yaml.dump(self.Params, f)

    def cb_load(self):
        self.log.info("Load")
        try:
            with open(self.file_name, "r") as f:
                self.Params = yaml.safe_load(f)
        except FileNotFoundError:
            self.log.info(f"File not found: {self.file_name}")
            raise


        # Set the default values to the GUI objects
        for key, value in self.Params.items():
            if key in self.h_gui:
                self.h_gui[key].set_val(value, is_callback=True)

        # Additional configuration parameters


    def closeEvent(self, event):
        self.log.info("Exiting the application")
        # Clean up the resources
        # Close the connection to the signal generator
        if self.vsa is not None:
            self.vsa.close()
        # Close the Resource Manager
        self.rm.close()

if __name__ == "__main__":
    # Initializes the application and prepares it to run a Qt event loop
    #  it is necessary to create an instance of this class before any GUI elements can be created
    app         = QApplication( sys.argv )
    # Create the LabDemoVsaControl object
    controller  = LabDemoVsaControl()
    # Show the GUI
    controller.show()
    # Start the Qt event loop (the sys.exit is for correct exit status to the OS)
    sys.exit(app.exec())
