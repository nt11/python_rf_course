import re

import  yaml
from    PyQt6.QtWidgets    import QApplication, QMainWindow, QVBoxLayout
from    PyQt6.uic          import loadUi

import numpy as np

from python_rf_course.utils.pyqt2python     import h_gui
from python_rf_course.utils.plot_widget     import PlotWidget
from python_rf_course.utils.logging_widget  import setup_logger
from python_rf_course.utils.SCPI_wrapper    import *

from pa_app_scan import PaScan


def is_valid_ip(ip:str) -> bool:
    # Regular expression pattern for matching IP address
    ip_pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return re.match(ip_pattern, ip) is not None


# The GUI controller clas inherit from QMainWindow object as defined in the ui file
class LabNetworkControl(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the UI file into the Class (LabDemoVsaControl) object
        loadUi("pa_app.ui", self)
        # Create Logger
        self.log = setup_logger(text_browser=self.textBrowser,name='pa_log', level=logging.DEBUG,is_console=True)
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
            Fstart              = h_gui(self.lineEdit_3         , self.cb_scan              ),
            Fstop               = h_gui(self.lineEdit_4         , self.cb_scan              ),
            Npoints             = h_gui(self.lineEdit_5         , self.cb_scan              ),
            ScanG               = h_gui(self.lcdNumber          , None              ),
            ScanOP1dB           = h_gui(self.lcdNumber_2        , None              ),
            ScanOIP3            = h_gui(self.lcdNumber_3        , None              ),
            ScanOIP5            = h_gui(self.lcdNumber_4        , None              ),
            Save                = h_gui(self.actionSave         , self.cb_save              ),
            Load                = h_gui(self.actionLoad         , self.cb_load              ))

        # Create a Resource Manager object
        self.rm         = pyvisa.ResourceManager('@py')
        self.sa         = None
        self.sg         = None

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

        # Create a widget for the Spectrum Analyzer plot
        self.plot_sa        = PlotWidget()
        layout              = QVBoxLayout(self.widget)
        layout.addWidget(self.plot_sa)

        # Iinitilize the freq and power arrays to empty
        self.f_scan = np.array([])
        self.thread = None

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

    # thread callback functions
    def tcb_progress(self, i):
        self.h_gui['TestPaProgress'].set_val(i)

    # thread callback functions
    def tcb_plot(self, freq, power, clf,legend):
        freq_v  = self.f_scan
        power_v = np.concatenate((power, np.ones(len(freq_v)-len(power))*-100)) - self.Params['Ptx']
        self.plot_sa.plot( freq_v , power_v,
                           line='b-' , line_width=1.5,
                           xlabel='Frequency (MHz)', ylabel='Power dBm',
                           title='Filter response', xlog=False, clf=clf, legend=legend)

    def cb_testpa(self):
        if self.sa is not None:
            self.log.info("Start scan")
            self.f_scan = np.linspace(self.h_gui['Fstart'].get_val(),
                                      self.h_gui['Fstop'  ].get_val(),
                                      self.h_gui['Npoints'].get_val())
            # Set the signal generator to output power (self.Params["Ptx"]))
            self.scpi_sg.write(f":OUTP:STAT OFF")
            self.scpi_sg.write(f":POW:LEV {self.Params['Ptx']} dBm")
            # initialize the freq and power arrays to empty
            self.freq = np.array([])
            self.power = np.array([])
            # Create the thread object
            self.thread = PaScan(f_scan=self.f_scan, scpi_sa=self.scpi_sa,scpi_sg=self.scpi_sg) # Create the thread object
            self.thread.progress.connect(self.tcb_progress)
            self.thread.data.connect(self.tcb_plot)
            self.thread.log.connect( self.log.info)

            self.thread.start() # Start the thread calling the run method


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
    controller  = LabNetworkControl()
    # Show the GUI
    controller.show()
    # Start the Qt event loop (the sys.exit is for correct exit status to the OS)
    sys.exit(app.exec())
