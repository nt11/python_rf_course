from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QComboBox, QCheckBox, QSlider, QPushButton
from PyQt6.uic import loadUi

import yaml
import sys
import re

import pyvisa

class h_gui:
    def __init__(self, obj, event, callback):
        self.obj        = obj
        self.event      = event
        self.cb         = callback
        self.val_type   = None

        if self.cb is not None:
            getattr(self.obj, self.event).connect(self.cb)

    def set_val(self, value, is_callback = False):
        # if the value type is not set, set it to the type of the value
        # done only once (the first time the value is set i.e. on first load)
        if self.val_type is None:
            self.val_type = type(value)
        else:
            value = self.val_type(value)

        # read the blockSignal state
        block_state = self.obj.signalsBlocked()
        # block the signal for all widgets
        self.obj.blockSignals(True)
        # update the value (TBD need to cover all widgets)
        if isinstance(self.obj, QComboBox):
            self.obj.setCurrentIndex(value)
        elif isinstance(self.obj, QCheckBox):
            self.obj.setChecked(value)
        elif isinstance(self.obj, QSlider):
            self.obj.setValue(value)
        elif isinstance(self.obj, QPushButton):
            # if pushButton is used as a checkable button
            if self.obj.isCheckable():
                self.obj.setChecked(value)
        else: #  isinstance(self.obj, QLineEdit):
            self.obj.setText(str(value))

        if is_callback:
            getattr(self.obj,self.event).emit()

        # restore the blockSignal state
        self.obj.blockSignals(block_state)

    def get_val(self):
        if isinstance(self.obj, QComboBox):
            return self.obj.currentIndex()
        elif isinstance(self.obj, QCheckBox):
            return self.obj.isChecked()
        elif isinstance(self.obj, QSlider):
            return self.obj.value()
        else: #  isinstance(self.obj, QLineEdit):
            if self.val_type is None:
                return self.obj.text()
            else:
                return self.val_type(self.obj.text())

    def emit(self):
        getattr(self.obj,self.event).emit()

def is_valid_ip(ip:str) -> bool:
    # Regular expression pattern for matching IP address
    ip_pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return re.match(ip_pattern, ip) is not None

# Load the UI file into the Class (LabDemoMxgControl) object
# The UI file (BasicMxgControl.ui) is created using Qt Designer
# The UI file is located in the same directory as this Python script
# The GUI controller clas inherit from QMainWindow object as defined in the ui file
class LabDemoMxgControl(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the UI file into the Class (LabDemoMxgControl) object
        loadUi("BasicMxgControl.ui", self)

        self.setWindowTitle("MXG Control")

        # Interface of the GUI Widgets to the Python code
        self.h_gui = dict(
            Connect     = h_gui(self.pushButton         , 'clicked'         , self.cb_connect       ),
            RF_On_Off   = h_gui(self.pushButton_2       , 'clicked'         , self.cb_rf_on_off     ),
            Mod_On_Off  = h_gui(self.pushButton_3       , 'clicked'         , self.cb_mod_on_off    ),
            IP          = h_gui(self.lineEdit           , 'editingFinished' , self.cb_ip            ),
            Fc          = h_gui(self.lineEdit_2         , 'editingFinished' , self.cb_fc            ),
            Pout        = h_gui(self.horizontalSlider   , 'valueChanged'    , self.cb_pout_slider   ),
            Save        = h_gui(self.actionSave         , 'triggered'       , self.cb_save          ),
            Load        = h_gui(self.actionLoad         , 'triggered'       , self.cb_load          ))

        # Create a Resource Manager object
        self.rm         = pyvisa.ResourceManager()
        self.sig_gen    = None

        # Load the configuration/default values from the YAML file
        self.Params = None
        self.h_gui['Load'].emit() # self.cb_load()


    # Callback function for the Connect button
    # That is a checkable button
    def cb_connect(self):
        if self.sender().isChecked():
            print("Connect button Checked")
            # Open the connection to the signal generator
            try:
                ip           = self.h_gui['IP'].get_val()
                self.sig_gen = self.rm.open_resource(f"TCPIP0::{ip}::inst0::INSTR")
                print(f"Connected to {ip}")
                # Read the signal generator status and update the GUI (RF On/Off, Modulation On/Off,Pout and Fc)
                # Query RF On/Off mode
                self.sig_gen.write(":OUTPUT:STATE?")
                rf_state    = bool(int(self.sig_gen.read().strip()))
                # Query Modulation On/Off mode
                self.sig_gen.write(":OUTPUT:MOD:STATE?")
                mod_state   = bool(int(self.sig_gen.read().strip()))
                # Query Output Power
                self.sig_gen.write(":POWER?")
                output_power_dbm = float(self.sig_gen.read())
                # Query Frequency
                self.sig_gen.write(":FREQ?")
                fc          = float(self.sig_gen.read()) * 1e-6

                # Update the GUI
                # in pushButton the callback is not triggered when calling setChecked
                self.h_gui['RF_On_Off'  ].set_val( rf_state)
                self.h_gui['Mod_On_Off' ].set_val(mod_state)
                self.h_gui['Pout'       ].set_val(output_power_dbm)
                self.h_gui['Fc'         ].set_val(fc)
            except Exception:
                if self.sig_gen is not None:
                    self.sig_gen.close()
                    self.sig_gen = None
                # Clear Button state
                self.sender().setChecked(False)
        else:
            print("Connect button Cleared")
            # Close the connection to the signal generator
            if self.sig_gen is not None:
                self.sig_gen.close()
                self.sig_gen = None

    # Callback function for the RF On/Off button
    # That is a checkable button
    def cb_rf_on_off(self):
        if self.sender().isChecked():
            if self.sig_gen is not None:
                self.sig_gen.write(":OUTPUT:STATE ON")
            print("RF On")
        else:
            if self.sig_gen is not None:
                self.sig_gen.write(":OUTPUT:STATE OFF")
            print("RF Off")

    # Callback function for the Modulation On/Off button
    # That is a checkable button
    def cb_mod_on_off(self):
        if self.sender().isChecked():
            if self.sig_gen is not None:
                self.sig_gen.write(":OUTPUT:MOD:STATE ON")
            print("Modulation On")
        else:
            if self.sig_gen is not None:
                self.sig_gen.write(":OUTPUT:MOD:STATE OFF")
            print("Modulation Off")

    # Callback function for the IP lineEdit
    def cb_ip(self):
        ip          = self.h_gui['IP'].get_val()
        # Check if the ip is a valid
        if not is_valid_ip(ip):
            print(f"Invalid IP address: {ip}, Resetting to default")
            ip = self.Params["IP"]
            # Set the default value to the GUI object
            self.h_gui['IP'].set_val(ip)

        print(f"IP = {ip}")

    # Callback function for the Fc lineEdit
    def cb_fc(self):
        # Check if the frequency is a valid float number
        try:
            frequency_mhz = self.h_gui['Fc'].get_val()
        except ValueError:
            print(f"Invalid Frequency: Resetting to default")
            frequency_mhz = self.Params["Fc"]
            # Set the default value to the GUI object
            self.h_gui['Fc'].set_val(frequency_mhz)

        if self.sig_gen is not None:
            self.sig_gen.write(f":FREQuency {frequency_mhz} MHz") # can replace the '} MHz' with '}e6'
        print(f"Fc = {frequency_mhz} MHz")

    def cb_pout_slider( self ):
        val = self.h_gui['Pout'].get_val()
        if self.sig_gen is not None:
            self.sig_gen.write(f":POWER {val}dBm")

        print(f"Pout = {val} dBm")

    def cb_save(self):
        print("Save")
        # Read the values from the GUI objects and save them to the Params dictionary
        self.Params["IP"]   = self.h_gui['IP'  ].get_val()
        self.Params["Fc"]   = self.h_gui['Fc'  ].get_val()
        self.Params["Pout"] = self.h_gui['Pout'].get_val()

        with open("sig_gen_defaults.yaml", "w") as f:
            yaml.dump(self.Params, f)

    def cb_load(self):
        print("Load")
        with open("sig_gen_defaults.yaml", "r") as f:
            self.Params = yaml.safe_load(f)

        # Set the default values to the GUI objects
        self.h_gui['IP'  ].set_val(     self.Params["IP"]  ) # consider to verify if IP is changed then disconnect and disconnect
        self.h_gui['Fc'  ].set_val(     self.Params["Fc"]  , is_callback=True)
        self.h_gui['Pout'].set_val(     self.Params["Pout"], is_callback=True)

        self.h_gui['Pout'].obj.setMaximum( self.Params["PoutMax"] )
        self.h_gui['Pout'].obj.setMinimum( self.Params["PoutMin"] )

if __name__ == "__main__":
    # Initializes the application and prepares it to run a Qt event loop
    #  it is necessary to create an instance of this class before any GUI elements can be created
    app         = QApplication( sys.argv )
    # Create the LabDemoMxgControl object
    controller  = LabDemoMxgControl()
    # Show the GUI
    controller.show()
    # Start the Qt event loop (the sys.exit is for correct exit status to the OS)
    sys.exit(app.exec())
