import re

import  yaml
from    PyQt6.QtWidgets    import QApplication, QMainWindow, QVBoxLayout
from    PyQt6.uic          import loadUi
from    PyQt6.QtCore       import QTimer

import numpy as np

from python_rf_course.utils.pyqt2python     import h_gui
from python_rf_course.utils.plot_widget     import PlotWidget
from python_rf_course.utils.logging_widget  import setup_logger
from python_rf_course.utils.SCPI_wrapper    import *
from python_rf_course.utils.multitone       import multitone

from pa_app_thread import PaScan

import pyvisa
import pyvisa_py
import pyarbtools as arb

import logging
import time

def is_valid_ip(ip:str) -> bool:
    # Regular expression pattern for matching IP address
    ip_pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return re.match(ip_pattern, ip) is not None


# The GUI controller clas inherit from QMainWindow object as defined in the ui file
class PA_App(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the UI file into the Class (LabDemoVsaControl) object
        loadUi("pa_app.ui", self)
        # Create Logger
        self.log = setup_logger(text_browser=self.textBrowser,name='pa_log', level=logging.INFO,is_console=True)
        logging.getLogger('pa_log').propagate = True
        self.scpi = None

        self.setWindowTitle("PA Analyzer")

        # Interface of the GUI Widgets to the Python code
        self.h_gui = dict(
            Connect             = h_gui(self.pushButton         , self.cb_connect           ),
            TestPa              = h_gui(self.pushButton_2       , self.cb_testpa            ),
            TestPaProgress      = h_gui(self.progressBar        , None              ),
            IP_SG               = h_gui(self.lineEdit           , self.cb_ip_sg             ),
            IP_SA               = h_gui(self.lineEdit_2         , self.cb_ip_sa             ),
            Ptx                 = h_gui(self.dial               , self.cb_ptx              ),
            Fstart              = h_gui(self.lineEdit_3         , self.cb_scan              ),
            Fstop               = h_gui(self.lineEdit_4         , self.cb_scan              ),
            Npoints             = h_gui(self.lineEdit_5         , self.cb_scan              ),
            FreezeYAxis         = h_gui(self.checkBox           , None              ),
            ScanG               = h_gui(self.lcdNumber          , None              ),
            ScanOP1dB           = h_gui(self.lcdNumber_2        , None              ),
            ScanOIP3            = h_gui(self.lcdNumber_3        , None              ),
            ScanOIP5            = h_gui(self.lcdNumber_4        , None              ),
            ScanPout            = h_gui(self.lcdNumber_5        , None              ),
            Save                = h_gui(self.actionSave         , self.cb_save              ),
            Load                = h_gui(self.actionLoad         , self.cb_load              ))

        # Create a Resource Manager object
        self.rm         = pyvisa.ResourceManager('@py')
        self.sa         = None
        self.sg         = None
        self.arb        = None

        # Load the configuration/default values from the YAML file
        self.Params     = None
        self.file_name  = "pa_defaults.yaml"
        self.h_gui['Load'].emit() #  self.cb_load

        self.file_name = "last.yaml"
        try:
            self.h_gui['Load'].callback()  # self.cb_load
        except FileNotFoundError:
            self.log.warning("No last.yaml file found")

        self.h_gui['Save'].emit() #  self.cb_save
        self.h_gui['Ptx'].set_val(self.h_gui['Ptx'].get_val()) #  Update the signal (event)

        # Create a widget for the Spectrum Analyzer plot
        self.plot_sa        = PlotWidget()
        layout              = QVBoxLayout(self.widget)
        layout.addWidget(self.plot_sa)

        # Iinitilize the freq and power arrays to empty
        self.f_scan = np.array([])
        self.Fspan  = None
        self.thread = None

        # Create a timer for the Spectrum Analyzer plot
        self.timer          = QTimer()
        self.timer.timeout.connect(self.cb_timer_trace)
        self.timer.start(250)


    # Callback function for the Connect button
    # That is a checkable button
    def cb_connect(self):
        if self.sender().isChecked(): # self.h_gui['Connect'].obj.isChecked():
            self.log.info("Connect button Checked")
            # Open the connection to the signal generator
            try:
                ip_sa          = self.h_gui['IP_SA'].get_val()
                ip_sg          = self.h_gui['IP_SG'].get_val()
                self.sa        = self.rm.open_resource(f"TCPIP0::{ip_sa}::inst0::INSTR")
                self.sg        = self.rm.open_resource(f"TCPIP0::{ip_sg}::inst0::INSTR")
                self.arb       = arb.instruments.VSG(ip_sg, timeout=5)
                self.sa.timeout = 5000
                self.sg.timeout = 5000
                self.scpi_sa    = SCPIWrapper(instr=self.sa, log= self.log, name='SA')
                self.scpi_sg    = SCPIWrapper(instr=self.sg, log= self.log, name='SG')

                self.log.info(f"Connected to {ip_sa=} and {ip_sg=}")

                # Query the signal generator name
                # <company_name>, <model_number>, <serial_number>,<firmware_revision>
                idn_sa      = ','.join( self.scpi_sa.query("*IDN?").split(',')[1:3])
                idn_sg      = ','.join( self.scpi_sg.query("*IDN?").split(',')[1:3])
                # Remove the firmware revision
                self.setWindowTitle('SA:' + idn_sa + " | SG:" + idn_sg)
                # Reset and clear all status (errors) of the spectrum analyzer
                self.scpi_sa.write("*RST")
                self.scpi_sa.write("*CLS")
                self.scpi_sg.write("*RST")
                self.scpi_sg.write("*CLS")
                # Load the arb with a two tone signal
                sig = multitone(BW=self.Params['ArbFd'], Ntones=2,
                                Fs=self.Params['ArbFs'], Nfft=2048)

                self.arb.configure(fs=self.Params['ArbFs']*1e6, iqScale=70 )
                self.arb.download_wfm(sig, wfmID='TwoTones')
                self.arb.set_alcState(0) # ALC Off (DO not use bool)
                self.arb.play('TwoTones')
                # Set the signal generator to output power
                self.scpi_sg.write(f":POW:LEV {self.h_gui["Ptx"].get_val()} dBm")
                # Set the spectrum analyzer span and RBW detector AVG and trace to clear/write
                self.Fspan = self.Params['ArbFd']*5.0 + 2.0 # Contains the 5th harmonic
                self.scpi_sa.write(f"freq:span {self.Fspan} MHz")
                self.scpi_sa.write(f"sense:BANDwidth:RESolution {self.Params['ArbFd']/8.0} MHz") # Maximal RBW for the scan
                self.scpi_sa.write("sense:DETEctor AVERage")
                self.scpi_sa.write("TRACe:MODE WRITe")
                self.scpi_sa.write("INITiate:CONTinuous On")
                # Set the spectrum analyzer center frequency and the signal generator frequency
                self.scpi_sa.write(f"freq:cent {self.Params['Fnominal']} MHz")
                self.scpi_sg.write(f"freq {     self.Params['Fnominal']} MHz")
                # Save the signal generator and spectrum analyzer state
                self.scpi_sa.write("*SAV 1")
                self.scpi_sg.write("*SAV 1")
                time.sleep(0.01)
            except Exception:
                self.log.error("Connection failed")
                if self.sa is not None:
                    self.sa.close()
                    self.sa = None
                if self.sg is not None:
                    self.sg.close()
                    self.sg = None
                # Clear Button state
                self.h_gui['Connect'].set_val(False, is_callback=True)
        else:
            self.log.info("Connect button Cleared")
            # Close the connection to the signal generator
            if self.sa is not None:
                self.sa.close()
                self.sa = None
            if self.sg is not None:
                self.sg.close()
                self.sg = None
                
            self.scpi = None

    def cb_ptx(self):
        ptx = self.h_gui['Ptx'].get_val()
        if self.sg is not None:
            self.scpi_sg.write(f":POW:LEV {ptx} dBm")


    # Callback function for the IP lineEdit
    def cb_ip_sa(self):
        ip          = self.h_gui['IP_SA'].get_val()
        # Check if the ip is a valid
        if not is_valid_ip(ip):
            self.log.error(f"Invalid SA IP address: {ip}, Resetting to default")
            ip = self.Params["IP_SA"]
            # Set the default value to the GUI object
            self.h_gui['IP_SA'].set_val(ip)

        self.log.info(f"SA IP = {ip}")

    def cb_ip_sg(self):
        ip          = self.h_gui['IP_SG'].get_val()
        # Check if the ip is a valid
        if not is_valid_ip(ip):
            self.log.error(f"Invalid SG IP address: {ip}, Resetting to default")
            ip = self.Params["IP_SG"]
            # Set the default value to the GUI object
            self.h_gui['IP_SG'].set_val(ip)

        self.log.info(f"SG IP = {ip}")

    def sa_read_trace(self):
        if self.sa is not None:
            # Query trace data PyVISA method for reading numerical data from instruments
            p           = self.sa.query_ascii_values(":TRACe:DATA? TRACE1", container=np.array)
            # Calculate frequency points
            f           = np.linspace(self.Params['Fnominal'] - self.Fspan/2, self.Params['Fnominal'] + self.Fspan/2, len(p))

            return p, f

    def cb_timer_trace(self):
        if self.sa is not None:
            # Get the trace from the spectrum analyzer
            trace, freq = self.sa_read_trace()
            # Check if checkbox of freeze Y axis is checked
            if self.h_gui['FreezeYAxis'].get_val():
                # Get the Y axis current limits
                y_min, y_max = self.plot_sa.get_y_range()
                # Round to the nearest 10 dB
                y_min = np.ceil( y_min/10.0)*10.0
                y_max = np.floor(y_max/10.0)*10.0
            else:
                # Set the Y axis limits to the trace
                y_min = None
                y_max = None


            # Plot the trace
            self.plot_sa.plot(freq, trace, line='b-', line_width=3.0,
                              y_lim_min=y_min       , y_lim_max=y_max,
                              xlabel='Frequency (MHz)', ylabel='Power dBm',
                              title='Spectrum Analyzer', xlog=False, clf=True)

    # thread callback functions
    def tcb_progress(self, i):
        self.h_gui['TestPaProgress'].set_val(i)

    # thread callback functions
    def tcb_plot(self, freq, power, clf= True,legend='Gain',color='b-'):
        freq_v  = self.f_scan
        power_v = np.concatenate((power, np.ones(len(freq_v)-len(power))*power[0]))
        self.plot_sa.plot( freq_v , power_v,
                           line=color , line_width=3.0,
                           xlabel='Frequency (MHz)', ylabel='Power dBm',
                           title='Filter response', xlog=False, clf=clf, legend=legend)

    def tcb_dump_csv(self, freq, gain, op1dB, oip3, oip5):
        # Create a CSV file name with date and time
        # Get the current date and time
        current_time = time.strftime("%Y%m%d_%H%M%S")
        # Create the CSV file name
        # Use the current time to create a unique file name
        csv_file = f"PA_Scan_{current_time}.csv"
        # Save the data to a CSV file
        with open(csv_file, "w") as f:
            f.write("Frequency (MHz), Gain (dB), OP1dB (dBm), OIP3 (dBm), OIP5 (dBm)\n")
            for i in range(len(freq)):
                f.write(f"{freq[i]},{gain[i]},{op1dB[i]},{oip3[i]},{oip5[i]}\n")
        self.log.info(f"Data saved to {csv_file}")


    def cb_testpa(self):
        if self.sender().isChecked():
            if self.sa is not None:
                self.timer.stop()
                self.log.info("Initialize scan params")
                self.f_scan = np.linspace(self.h_gui['Fstart' ].get_val(),
                                          self.h_gui['Fstop'  ].get_val(),
                                          self.h_gui['Npoints'].get_val())


                # Create the thread object
                self.thread = PaScan(f_scan=self.f_scan, scpi_sa=self.scpi_sa,scpi_sg=self.scpi_sg, loss= self.Params['Loss']) # Create the thread object
                self.thread.progress.connect(self.tcb_progress  )
                self.thread.data    .connect(self.tcb_plot      )
                self.thread.log     .connect(self.log.info      )
                self.thread.csv     .connect(self.tcb_dump_csv  )
                # Connect to LCD real time display
                self.thread.lcd_g    .connect(self.h_gui['ScanG'     ].set_val)
                self.thread.lcd_op1dB.connect(self.h_gui['ScanOP1dB' ].set_val)
                self.thread.lcd_oip3 .connect(self.h_gui['ScanOIP3'  ].set_val)
                self.thread.lcd_oip5 .connect(self.h_gui['ScanOIP5'  ].set_val)
                self.thread.lcd_p_out .connect(self.h_gui['ScanPout' ].set_val)

                self.thread.start() # Start the thread calling the run method
        else:
            self.log.info("Stop the thread")
            if self.thread is not None:
                self.thread.stop()
                self.thread.wait()
                self.thread = None
                # Recall signal generator and spectrum analyzer state
                self.scpi_sa.write("*RCL 1")
                self.scpi_sg.write("*RCL 1")
                self.timer.start()


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
                params = yaml.safe_load(f)

            if self.Params is not None:
                for key in self.Params.keys():
                    if key in params:
                        self.Params[key] = params[key]
                    else:
                        self.log.error(f"Key not found: {key}")
            else:
                self.Params = params

        except FileNotFoundError:
            self.log.info(f"File not found: {self.file_name}")
            raise



        # Set the default values to the GUI objects
        for key, value in self.Params.items():
            if key in self.h_gui:
                self.h_gui[key].set_val(value, is_callback=True)

    def cb_scan(self):
        # Check that the input is a valid number
        try:
            f_start = float(self.h_gui['Fstart'].get_val())
            f_stop  = float(self.h_gui['Fstop' ].get_val())
            n_points= int(  self.h_gui['Npoints'].get_val())
        except ValueError:
            self.log.error("Invalid input, Resetting to default")
            self.h_gui['Fstart'].set_val( self.Params["Fstart"] )
            self.h_gui['Fstop' ].set_val( self.Params["Fstop" ] )
            self.h_gui['Npoints'].set_val( self.Params["Npoints"])

    def closeEvent(self, event):
        self.log.info("Exiting the application")
        self.timer.stop()
        # Clean up the resources
        # Close the connection to the signal generator
        if self.sa is not None:
            self.sa.close()
        if self.sg is not None:
            self.sg.close()
        # Close the Resource Manager
        self.rm.close()

if __name__ == "__main__":
    # Initializes the application and prepares it to run a Qt event loop
    #  it is necessary to create an instance of this class before any GUI elements can be created
    app         = QApplication( sys.argv )
    # Create the LabDemoVsaControl object
    controller  = PA_App()
    # Show the GUI
    controller.show()
    # Start the Qt event loop (the sys.exit is for correct exit status to the OS)
    sys.exit(app.exec())
