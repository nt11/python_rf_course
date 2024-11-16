
import re
import sys

import pyvisa
import yaml
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import loadUi


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

        # Object.Event.connect(callback)
        # or alternatively:
        # getattr(self.Object, 'Event').connect(callback)
        # Connect GUI objects to callback functions for events
        # Object = self.pushButton, Event = 'clicked', callback = self.cb_connect
        self.pushButton  .clicked.connect(self.cb_connect   )
        self.pushButton_2.clicked.connect(self.cb_rf_on_off )
        self.pushButton_3.clicked.connect(self.cb_mod_on_off)
        # lineEdit
        self.lineEdit  .editingFinished.connect(self.cb_ip)
        self.lineEdit_2.editingFinished.connect(self.cb_fc)
        # horizontalSlider
        self.horizontalSlider.valueChanged.connect(self.cb_pout_slider)
        # actionSave
        self.actionSave.triggered.connect(self.cb_save)
        # actionLoad
        self.actionLoad.triggered.connect(self.cb_load)

        # Create a Resource Manager object
        self.rm         = pyvisa.ResourceManager('@py')
        self.sig_gen    = None

        # Load the configuration/default values from the YAML file
        self.Params = None
        self.cb_load()


    # Callback function for the Connect button
    # That is a checkable button
    def cb_connect(self):
        if self.sender().isChecked():
            print("Connect button Checked")
            # Open the connection to the signal generator
            ip           = self.lineEdit.text()
            try:
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
                self.pushButton_2   .setChecked( rf_state)
                self.pushButton_3   .setChecked(mod_state)
                # in Slider the callback is triggered when calling setValue (so BlockSignals is used)
                self.horizontalSlider.blockSignals(True)
                self.horizontalSlider.setValue(int(output_power_dbm))
                self.horizontalSlider.blockSignals(False)
                # in lineEdit the callback is not triggered when calling setText
                self.lineEdit_2     .setText(f"{fc}")
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
            print("RF On")
        else:
            print("RF Off")

    # Callback function for the Modulation On/Off button
    # That is a checkable button
    def cb_mod_on_off(self):
        if self.sender().isChecked():
            print("Modulation On")
        else:
            print("Modulation Off")

    # Callback function for the IP lineEdit
    def cb_ip(self):
        # Using the sender() method of PyQt6 to get the object that triggered the event
        obj_caller  = self.sender()
        ip          = obj_caller.text()
        # Check if the ip is a valid
        if not is_valid_ip(ip):
            print(f"Invalid IP address: {ip}, Resetting to default")
            ip = self.Params["IP"]
            # Set the default value to the GUI object
            obj_caller.setText(ip)

        print(f"IP = {ip}")

    # Callback function for the Fc lineEdit
    def cb_fc(self):
        # Using the sender() method of PyQt6 to get the object that triggered the event
        obj_caller = self.sender()
        frequency_mhz = obj_caller.text()
        # Check if the frequency is a valid float number
        try:
            frequency_mhz = float(frequency_mhz)
        except ValueError:
            print(f"Invalid Frequency: {frequency_mhz}, Resetting to default")
            frequency_mhz = self.Params["Fc"]
            # Set the default value to the GUI object
            obj_caller.setText(str(frequency_mhz))

        print(f"Fc = {frequency_mhz} MHz")

    def cb_pout_slider( self ):
        # Using the sender() method of PyQt6 to get the object that triggered the event
        obj_caller  = self.sender()
        value       = obj_caller.value()
        print(f"Pout = {value} dBm")

    def cb_save(self):
        print("Save")
        # Read the values from the GUI objects and save them to the Params dictionary
        self.Params["IP"]   = self.lineEdit.text()
        self.Params["Fc"]   = float(self.lineEdit_2.text())
        self.Params["Pout"] = self.horizontalSlider.value()

        with open("sig_gen_defaults.yaml", "w") as f:
            yaml.dump(self.Params, f)

    def cb_load(self):
        print("Load")
        with open("sig_gen_defaults.yaml", "r") as f:
            self.Params = yaml.safe_load(f)

        # Set the default values to the GUI objects
        self.lineEdit  .setText(     self.Params["IP"]  )
        self.lineEdit_2.setText( str(self.Params["Fc"]) )
        self.horizontalSlider.setValue( self.Params["Pout"] )
        self.horizontalSlider.setMaximum( self.Params["PoutMax"] )
        self.horizontalSlider.setMinimum( self.Params["PoutMin"] )

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
