from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import loadUi

import yaml
import sys

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

        # Load the configuration/default values from the YAML file
        self.Params = None
        self.cb_load()

    # Callback function for the Connect button
    # That is a checkable button
    def cb_connect(self):
        if self.sender().isChecked():
            print("Connect button Checked")
        else:
            print("Connect button Cleared")

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
        print(f"IP = {ip}")

    # Callback function for the Fc lineEdit
    def cb_fc(self):
        # Using the sender() method of PyQt6 to get the object that triggered the event
        obj_caller = self.sender()
        frequency_mhz = obj_caller.text()
        print(f"Fc = {frequency_mhz} MHz")

    def cb_pout_slider( self ):
        # Using the sender() method of PyQt6 to get the object that triggered the event
        obj_caller  = self.sender()
        value       = obj_caller.value()
        print(f"Pout = {value} dBm")

    def cb_save(self):
        print("Save")
        # Read the values from the GUI objects and save them to the Params dictionary
        self.Params["IP"]     = self.lineEdit.text()
        self.Params["Fc"]     = float(self.lineEdit_2.text())
        self.Params["Pout"]   = self.horizontalSlider.value()

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
