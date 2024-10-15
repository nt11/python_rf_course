from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import loadUi

import sys


class LabDemoMxgControl(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the UI file into the Class (LabDemoMxgControl) object
        loadUi("BasicMxgControl.ui", self)

        self.setWindowTitle("MXG Control")

        # Object.Event.connect(callback)
        # Connect GUI objects to callback functions for events
        # Object = self.pushButton, Event = 'clicked', callback = self.cb_connect
        self.pushButton.clicked.connect(self.cb_connect)
        # or alternatively:
        # getattr(self.pushButton, 'clicked').connect(self.cb_connect)

    def cb_connect(self):
        if self.pushButton.isChecked():
            print("Connect button Checked")
        else:
            print("Connect button Cleared")

if __name__ == "__main__":
    app         = QApplication( sys.argv )
    controller  = LabDemoMxgControl()
    controller.show()
    app.exec()
    sys.exit()
