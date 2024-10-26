from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import loadUi

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
        
        # Object.Event.connect(callback)
        # or alternatively:
        # getattr(self.Object, 'Event').connect(callback)
        # Connect GUI objects to callback functions for events
        # Object = self.pushButton, Event = 'clicked', callback = self.cb_connect
        self.pushButton .clicked.connect(self.cb_connect   )

    def cb_connect(self):
        if self.pushButton.isChecked():
            print("Connect button Checked")
        else:
            print("Connect button Cleared")

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
