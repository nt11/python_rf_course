from PyQt6.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg
import numpy     as np

class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout              = QVBoxLayout()
        self.setLayout(layout)
        self.plot_widget    = pg.PlotWidget()
        layout.addWidget(self.plot_widget)

        self.ax             = None
        self.legend         = []
        self.plot()  # Call plot function to initially populate the plot

        self.plot_widget.setMouseEnabled(x=True, y=True)
        self.plot_widget.showGrid(x=True, y=True)

    def clear(self):
        self.plot_widget.clear()
        self.legend = []

    def plot(self                   ,
             x              = None  ,
             y              = None  ,
             line           = 'b-'  ,
             y_lim_max      = None  ,
             y_lim_min      = None  ,
             clf            = False ,
             legend         = None  ,
             xlabel         = 'X',
             ylabel         = 'Y',
             title          = 'Title' ,
             xlog           = False ):

        # Example plot
        if y is None:
            y = [0, 0, 0, 0, 0]
            y = np.array(y)

        if x is None:
            x = [0, 1, 2, 3, 4]
            x = np.array(x)

        if clf:
            self.plot_widget.clear()
            self.legend = []

        if xlog:
            self.plot_widget.setLogMode(x=True, y=False)
        else:
            self.plot_widget.setLogMode(x=False, y=False)


        # line is a character array with the first element being the color and the second being the line style
        line += '-'
        self.plot_widget.plot(x.flatten(), y.flatten(), pen=line[0], width=2, style=line[1])

        self.plot_widget.setLabel('bottom'  , xlabel)
        self.plot_widget.setLabel('left'    , ylabel)
        self.plot_widget.setTitle(title)

        # Set Y axis to a maximum value if specified
        external_y_lim      = False
        if y_lim_max is not None:
            temp_y_lim_max  = y_lim_max
            external_y_lim  = True
        else:
            # get the current y limit of the sys
            temp_y_lim_max  = self.plot_widget.getAxis('left').range[1]

        if y_lim_min is not None:
            temp_y_lim_min  = y_lim_min
            external_y_lim  = True
        else:
            temp_y_lim_min  = self.plot_widget.getAxis('left').range[0]

        if external_y_lim:
            self.plot_widget.setYRange(temp_y_lim_min, temp_y_lim_max)
        else:
            # set Y axis to auto scale
            self.plot_widget.enableAutoRange(axis='y')

        if legend is not None:
            self.legend.append(legend)
            self.plot_widget.setLegend(self.legend)

        # draw the plot
        self.plot_widget.repaint()
