from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QComboBox, QCheckBox, QSlider, QPushButton, QSpinBox, QLineEdit, QDoubleSpinBox, QDial


class h_gui:
    def __init__(self, obj, callback, event = None):
        self.obj        = obj
        self.callback   = callback
        self.val_type   = None

        if self.callback is not None:
            if event is None:
                if isinstance(obj, QComboBox):
                    self.event = "currentIndexChanged"
                elif isinstance(obj, QCheckBox):
                    self.event = "stateChanged"
                elif isinstance(obj, (QSlider, QSpinBox, QDoubleSpinBox,QDial)):
                    self.event = "valueChanged"
                elif isinstance(obj, QPushButton):
                    self.event = "clicked"
                elif isinstance(obj, QAction):
                    self.event = "triggered"
                elif isinstance(obj, QLineEdit):
                    self.event = "editingFinished"
                else:
                    # Report an error
                    self.event = None
                    raise ValueError(f"Error: Unknown widget type {obj}")
            else:
                self.event = event

            getattr(self.obj, self.event).connect(self.callback)

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
        elif isinstance(self.obj, (QSlider, QSpinBox, QDoubleSpinBox,QDial) ):
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

    def call_widget_method(self, method,is_callback = False, *args):
        # read the blockSignal state
        block_state = self.obj.signalsBlocked()

        # block the signal for all widgets
        self.obj.blockSignals(True)
        # call
        r = getattr(self.obj, method)(*args)
        if is_callback:
            getattr(self.obj,self.event).emit()

        # restore the blockSignal state
        self.obj.blockSignals(block_state)

        return r

    def get_val(self):
        if isinstance(self.obj, QComboBox):
            return self.obj.currentIndex()
        elif isinstance(self.obj, QCheckBox):
            return self.obj.isChecked()
        elif isinstance(self.obj, (QSlider, QSpinBox, QDoubleSpinBox,QDial)):
            return self.obj.value()
        else: #  isinstance(self.obj, QLineEdit):
            if self.val_type is None:
                return self.obj.text()
            else:
                return self.val_type(self.obj.text())

    def emit(self):
        getattr(self.obj,self.event).emit()
