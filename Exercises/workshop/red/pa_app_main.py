# WSR_1 Import everything you need
#

from python_rf_course.utils.pyqt2python     import h_gui
from python_rf_course.utils.plot_widget     import PlotWidget
from python_rf_course.utils.logging_widget  import setup_logger
from python_rf_course.utils.SCPI_wrapper    import *
from python_rf_course.utils.multitone       import multitone

# WSR_2 Import the worker thread class
#



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
        #WSR_3: Set up the logger for the application (slide 4-30, example 310)
        #self.log = ...
        logging.getLogger('pa_log').propagate = True
        self.scpi = None

        self.setWindowTitle("PA Analyzer")

        # Interface of the GUI Widgets to the Python code
        self.h_gui = dict(
            Connect             = h_gui(self.pushButton         , self.cb_connect           ),
            TestPa              = h_gui(self.pushButton_2       , self.cb_testpa            ),
            TestPaProgress      = h_gui(self.progressBar        , None                      ),
            IP_SG               = h_gui(self.lineEdit           , self.cb_ip_sg             ),
            IP_SA               = h_gui(self.lineEdit_2         , self.cb_ip_sa             ),
            Ptx                 = h_gui(self.dial               , self.cb_ptx               ),
            Fstart              = h_gui(self.lineEdit_3         , self.cb_scan              ),
            Fstop               = h_gui(self.lineEdit_4         , self.cb_scan              ),
            Npoints             = h_gui(self.lineEdit_5         , self.cb_scan              ),
            ScanG               = h_gui(self.lcdNumber          , None                      ),
            ScanOP1dB           = h_gui(self.lcdNumber_2        , None                      ),
            ScanOIP3            = h_gui(self.lcdNumber_3        , None                      ),
            ScanOIP5            = h_gui(self.lcdNumber_4        , None                      ),
            Save                = h_gui(self.actionSave         , self.cb_save              ),
            Load                = h_gui(self.actionLoad         , self.cb_load              ))

        # Create a Resource Manager object
        #WSR_4: Create the Resource Manager object (slide 2-54, example 109)
        #self.rm         = ...
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
        #WSR_5: Create a widget for the Spectrum Analyzer plot (slide 4-23, example 310)
        #self.plot_sa        = ...
        #
        #

        # Initilize the freq and power arrays to empty
        self.f_scan = np.array([])
        self.Fspan  = None
        self.thread = None

        #WS_1 - Create a timer for the Spectrum Analyzer plot, connect it to cb_timer_trace and start it for 250ms (slide 4-24, example 310)
        #
        #
        #


    # Callback function for the Connect button
    # That is a checkable button
    def cb_connect(self):
        if self.sender().isChecked(): # self.h_gui['Connect'].obj.isChecked():
            self.log.info("Connect button Checked")
            # Open the connection to the signal generator
            try:
                #WSR_6: Obtain the IP values from the GUI
                #ip_sa          = ...
                #ip_sg          = ...

                #WSR_7: Open the resources for the spectrum analyzer and signal generator (slide 2-54, example 109)
                #self.sa        = ...
                #self.sg        = ...

                #WSR_8: Create the arb object (slide 3-51, example 219)
                #self.arb       = ...

                self.sa.timeout = 5000
                self.sg.timeout = 5000

                #WSR_9: Create the SCPIWrapper objects for the spectrum analyzer and signal generator (slide 4-40)
                #self.scpi_sa    = ...
                #self.scpi_sg    = ...

                self.log.info(f"Connected to {ip_sa=} and {ip_sg=}")

                # Query the signal generator name
                # <company_name>, <model_number>, <serial_number>,<firmware_revision>
                idn_sa      = ','.join( self.scpi_sa.query("*IDN?").split(',')[1:3])
                idn_sg      = ','.join( self.scpi_sg.query("*IDN?").split(',')[1:3])
                # Remove the firmware revision
                self.setWindowTitle('SA:' + idn_sa + " | SG:" + idn_sg)
                #WSR_10: Send reset, clear to both sa and sg (slide 4-11)
                #
                #
                #
                #

                # Load the arb with a two tone signal


                #WS_2 - configure the multitone for a 2 tone signal with the bandwidth of the PA and the sampling frequency of the arb
                # and play the signal on the arb (slide 3-51, example 219). Use ArbFd as BW and ArbFS as Fs (from the yaml),
                # remember that the configure function of the arb object takes the sampling frequency in Hz
                #sig = multitone(...
                #self.arb.configure(...
                #self.arb.download_wfm(...
                self.arb.set_alcState(0) # ALC Off (DO not use bool)
                #self.arb.play(...


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
                # WS_3 Save the signal generator and spectrum analyzer state for the spectrum analyzer and signal generator (slide 4-11)
                #
                #
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
        #WSR_11: Set the signal generator power level to the value of the dial. Get the ptx from the GUI and send it to the SG
        #
        if self.sg is not None:
            #


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
            # Plot the trace
            # WSR_12: Plot the trace from the spectrum analyzer (slide 4-21, example 310),
            # set the x and y labels, title, line width to 3.0 and clear the plot
            #


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

    def cb_testpa(self):
        if self.sender().isChecked():
            if self.sa is not None:
                #WSR_13: Stop the timer (slide 4-23)
                #
                self.log.info("Initialize scan params")
                self.f_scan = np.linspace(self.h_gui['Fstart' ].get_val(),
                                          self.h_gui['Fstop'  ].get_val(),
                                          self.h_gui['Npoints'].get_val())


                #WSR_14: Create the thread object and connect it to signals, connect progress to tcb_progress, data to tcb_plot and log to self.log.info
                #self.thread = ...
                #
                #
                #
                # Connect to LCD real time display
                self.thread.lcd_g    .connect(self.h_gui['ScanG'    ].set_val)
                self.thread.lcd_op1dB.connect(self.h_gui['ScanOP1dB'].set_val)
                self.thread.lcd_oip3 .connect(self.h_gui['ScanOIP3' ].set_val)
                self.thread.lcd_oip5 .connect(self.h_gui['ScanOIP5' ].set_val)
                # WSR_15: Start the thread (slide 4-26)
                #
        else:
            # WS_4: Stop the thread/wait and recall the signal generator and spectrum analyzer state  (slide 4-26, example 310)
            self.log.info("Stop the thread")
            if self.thread is not None:
                #
                #
                self.thread = None
                # Recall signal generator and spectrum analyzer state (slide 4-12) and start the timer (slide 4-24, example 310)
                #
                #
                #


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
