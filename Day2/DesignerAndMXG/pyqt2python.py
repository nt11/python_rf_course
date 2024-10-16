from PyQt6.QtWidgets import QComboBox, QCheckBox, QSlider, QPushButton

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
