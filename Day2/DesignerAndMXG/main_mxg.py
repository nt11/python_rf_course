from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPalette
from PyQt6.uic import loadUi

import pyvisa
import re
import yaml
import sys

def is_valid_ip(ip:str) -> bool:
    # Regular expression pattern for matching IP address
    ip_pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return re.match(ip_pattern, ip) is not None

def is_valid_number(s):
    # Regular expression pattern for matching numbers
    number_pattern = r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$'
    return re.match(number_pattern, s) is not None


class LabDemoMxgControl(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the UI file into the Class (LabDemoMxgControl) object
        loadUi("BasicMxgControl.ui", self)

        self.setWindowTitle("MXG Control")

        # Create a GUI handles dictionary with friendly names keys
        # and tuples with the GUI object, event (that triggers the callback) and callback function
        self.h_gui = dict(Connect    = (self.pushButton      ,'clicked'          ,self.cb_connect       ),
                          IP         = (self.lineEdit        ,'editingFinished'  ,self.cb_ip            ),
                          RfOnOff    = (self.pushButton_2    ,'clicked'          ,self.cb_rf_on_off     ),
                          ModOnOff   = (self.pushButton_3    ,'clicked'          ,self.cb_mod_on_off    ),
                          Fc         = (self.lineEdit_2      ,'editingFinished'  ,self.cb_fc            ),
                          PoutSlider = (self.horizontalSlider,'valueChanged'     ,self.cb_pout_slider   ),
                          Save       = (self.actionSave      ,'triggered'        ,self.cb_save          ),
                          Load       = (self.actionLoad      ,'triggered'        ,self.cb_load          ))

        # Connect GUI objects to callback functions for events
        # equivalent for example to:
        #       self.pushButton.clicked.connect(self.cb_connect)
        for key, value_tuple in self.h_gui.items():
            h, event, cb = value_tuple
            if cb is not None:
                getattr(h,event).connect( cb )

        # Create a Resource Manager object
        self.rm = pyvisa.ResourceManager()

        with open("sig_gen_defaults.yaml", "r") as f:
            self.Param = yaml.safe_load(f)

        self.h_gui['PoutSlider'][0].setMaximum(self.Param['MxgSliderPmax'])
        self.h_gui['PoutSlider'][0].setMinimum(self.Param['MxgSliderPmin'])

        self.siggen = None

        if is_valid_ip( self.Param["MxgIP"] ):
            self.mxg_ip = self.Param["MxgIP"]
            self.h_gui["IP"][0].setText(self.Param["MxgIP"])
        else:
            self.mxg_ip = None

        self.is_connect_mxg = False


    def cb_connect(self):
        # the pushButton is checkable. So, read the state to determine if it is connected or not
        button_state = self.h_gui["Connect"][0].isChecked()
        if button_state:
            if self.mxg_ip  is not None:
                try:
                    self.siggen         = self.rm.open_resource(f"TCPIP0::{self.mxg_ip}::inst0::INSTR")
                    self.is_connect_mxg = True
                except Exception:
                    self.is_connect_mxg = False
                    # Clear Button state
                    self.h_gui["Connect"][0].setChecked(False)
                    return

            # Query RF On/Off mode
            self.siggen.write(":OUTPUT:STATE?")
            rf_state    = self.siggen.read()
            self.siggen.write(":OUTPUT:MOD:STATE?")
            mod_state   = self.siggen.read()
            self.siggen.write(":POWER?")
            output_power_dbm = float(self.siggen.read())
            self.siggen.write(":FREQ?")
            fc          = float(self.siggen.read())*1e-6

            # Convert response to a meaningful value
            if rf_state.strip() == '0':
                self.h_gui['RfOnOff'][0].setChecked(False)
            elif rf_state.strip() == '1':
                self.h_gui['RfOnOff'][0].setChecked(True)
            else:
                print("Unknown RF Output state")

            if mod_state.strip() == '0':
                self.h_gui['ModOnOff'][0].setChecked(False)
            elif mod_state.strip() == '1':
                self.h_gui['ModOnOff'][0].setChecked(True)
            else:
                print("Unknown MOD Output state")

            self.h_gui["PoutSlider"][0].setValue(int(output_power_dbm))
            self.h_gui["Fc"][0].setText(f"{fc}")
        else:
            self.is_connect_mxg = False

    def cb_ip(self):
        if is_valid_ip(self.h_gui['IP'][0].text()):
            self.mxg_ip = self.h_gui['IP'][0].text()
        else:
            self.mxg_ip = None

    def cb_rf_on_off( self ):
        state = self.h_gui["RfOnOff"][0].isChecked()
        if self.is_connect_mxg:
            if state:
                self.siggen.write(":OUTP:STAT ON")
            else:
                self.siggen.write(":OUTP:STAT OFF")

    def cb_mod_on_off(self):
        state = self.h_gui["ModOnOff"][0].isChecked()
        if self.is_connect_mxg:
            if state:
                self.siggen.write("OUTPUT:MOD:STAT ON")
            else:
                self.siggen.write(":OUTPUT:MOD:STAT OFF")

    def cb_fc(self):
        frequency_mhz = self.h_gui['Fc'][0].text()
        if is_valid_number(frequency_mhz):
            if self.is_connect_mxg:
                self.siggen.write(f":FREQuency {frequency_mhz} MHz")
            else:
                print(f"Fc = {frequency_mhz} MHz")

    def cb_pout_slider( self ):
        value = self.h_gui["PoutSlider"][0].value()
        if self.is_connect_mxg:
            self.siggen.write(f":POWER { value }dBm")
        else:
            print(f"Pout = {value} dBm")

    def cb_save(self):
        if self.is_connect_mxg:
            self.Params['MxgIP'] = self.mxg_ip
            with open("sig_gen_defaults.yaml", "w") as f:
                yaml.dump(self.Params, f)
        else:
            print("MXG not connected")

    def cb_load(self):
        with open("sig_gen_defaults.yaml", "r") as f:
            self.Params = yaml.safe_load(f)
        self.h_gui['PoutSlider'][0].setMaximum(self.Params['MxgSliderPmax'])
        self.h_gui['PoutSlider'][0].setMinimum(self.Params['MxgSliderPmin'])
        self.h_gui['IP'][0].setText(self.Params['MxgIP'])

if __name__ == "__main__":
    app         = QApplication( sys.argv )
    controller  = LabDemoMxgControl()
    controller.show()
    app.exec()
    if controller.is_connect_mxg is not None:
        controller.siggen.close()

    sys.exit()
