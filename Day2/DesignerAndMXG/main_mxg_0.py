from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import loadUi

import sys


class LabDemoMxgControl(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the UI file into the Class (LabDemoMxgControl) object
        loadUi("BasicMxgControl.ui", self)

        self.setWindowTitle("MXG Control")



if __name__ == "__main__":
    app         = QApplication( sys.argv )
    controller  = LabDemoMxgControl()
    controller.show()
    app.exec()
    sys.exit()
