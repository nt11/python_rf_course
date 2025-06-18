from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt
import pyqtgraph as pg
import numpy as np


class PlotWidget(QWidget):
    def __init__(self, parent=None, x_zoom=True, y_zoom=True, rect_zoom=False, downsampling=True):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)

        self.ax = None
        self.legend = []
        self.plot()  # Call plot function to initially populate the plot

        self.plot_widget.setMouseEnabled(x=x_zoom, y=y_zoom)
        self.plot_widget.showGrid(x=True, y=True)

        # Ginput related attributes
        self.ginput_active = False
        self.ginput_points = []
        self.ginput_scatter = None
        self.ginput_n_points = None
        self.current_mouse_mode = pg.ViewBox.PanMode  # Track current mouse mode

        if rect_zoom:
            self.set_rect_zoom_mode()

        if downsampling:
            self.plot_widget.setDownsampling(auto=True, mode='peak')

    def clear(self):
        self.plot_widget.clear()
        self.legend = []

    def plot(self, x=None, y=None, line='b-', y_lim_max=None, y_lim_min=None,
             clf=False, legend=None, xlabel='X', ylabel='Y', line_width=2,
             title='Title', xlog=False, symbol = None):
        # Your existing plot method remains the same
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

        just_markers = False
        # add an option for marker
        if len(line) == 1:
            if symbol is not None:
                just_markers = True
            else:
                line += '-'

        style_dict = {
            '-': Qt.PenStyle.SolidLine,
            '--': Qt.PenStyle.DashLine,
            ':': Qt.PenStyle.DotLine,
            '-.': Qt.PenStyle.DashDotLine}
        self.plot_widget.addLegend()

        if not just_markers:
            self.plot_widget.plot(x.flatten(), y.flatten(),
                                  pen=pg.mkPen(line[0], width=line_width, style=style_dict[line[1:]]),
                                  name=legend, symbol=symbol)
        else:
            self.plot_widget.plot(x.flatten(), y.flatten(),
                                  pen=None,
                                  name=legend, symbol=symbol)

        self.plot_widget.setLabel('bottom', xlabel)
        self.plot_widget.setLabel('left', ylabel)
        self.plot_widget.setTitle(title)

        external_y_lim = False
        if y_lim_max is not None:
            temp_y_lim_max = y_lim_max
            external_y_lim = True
        else:
            temp_y_lim_max = self.plot_widget.getAxis('left').range[1]

        if y_lim_min is not None:
            temp_y_lim_min = y_lim_min
            external_y_lim = True
        else:
            temp_y_lim_min = self.plot_widget.getAxis('left').range[0]

        if external_y_lim:
            self.plot_widget.setYRange(temp_y_lim_min, temp_y_lim_max)
        else:
            self.plot_widget.enableAutoRange(axis='y')

        self.plot_widget.repaint()

    def ginput(self, n_points=None):
        """
        Collect mouse input points from the plot.

        Parameters:
        -----------
        n_points : int, optional
            Number of points to collect. If None, collect until Enter is pressed.

        Returns:
        --------
        points : numpy.ndarray
            Array of shape (n, 2) containing the collected (x, y) coordinates
        """
        # Store current mouse mode and set to PanMode for point selection
        self.plot_widget.getViewBox().setMouseMode(pg.ViewBox.PanMode)

        # Initialize ginput state
        self.ginput_active = True
        self.ginput_points = []
        self.ginput_n_points = n_points

        # Create scatter plot for showing selected points
        self.ginput_scatter = pg.ScatterPlotItem(size=10, pen=pg.mkPen('r'), brush=pg.mkBrush('r'))
        self.plot_widget.addItem(self.ginput_scatter)

        # Connect signals
        self.plot_widget.scene().sigMouseClicked.connect(self._ginput_click)
        self.setFocus()  # Ensure widget can receive key events

        # Start event loop
        while self.ginput_active:
            QApplication.processEvents()

        # Clean up
        self.plot_widget.scene().sigMouseClicked.disconnect(self._ginput_click)
        if self.ginput_scatter is not None:
            self.plot_widget.removeItem(self.ginput_scatter)

        # Restore original mouse mode
        self.plot_widget.getViewBox().setMouseMode(self.current_mouse_mode)

        return np.array(self.ginput_points)

    def _ginput_click(self, event):
        """Handle mouse clicks during ginput collection."""
        if event.button() == Qt.MouseButton.LeftButton and self.ginput_active:
            pos = self.plot_widget.getPlotItem().vb.mapSceneToView(event.scenePos())
            self.ginput_points.append((pos.x(), pos.y()))

            # Update scatter plot
            x = [p[0] for p in self.ginput_points]
            y = [p[1] for p in self.ginput_points]
            self.ginput_scatter.setData(x=x, y=y)

            # Check if we've collected enough points
            if self.ginput_n_points is not None and len(self.ginput_points) >= self.ginput_n_points:
                self.ginput_active = False

    def keyPressEvent(self, event):
        """Handle key press events."""
        if self.ginput_active and (event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter):
            self.ginput_active = False
        else:
            super().keyPressEvent(event)

    def set_rect_zoom_mode(self):
        self.current_mouse_mode = pg.ViewBox.RectMode
        self.plot_widget.getViewBox().setMouseMode(pg.ViewBox.RectMode)

    def set_pan_mode(self):
        self.current_mouse_mode = pg.ViewBox.PanMode
        self.plot_widget.getViewBox().setMouseMode(pg.ViewBox.PanMode)

    def set_y_range(self, y_min, y_max):
        self.plot_widget.setYRange(y_min, y_max)

    def set_x_range(self, x_min, x_max):
        self.plot_widget.setXRange(x_min, x_max)

    def get_y_range(self):
        return self.plot_widget.getAxis('left').range

    def get_x_range(self):
        return self.plot_widget.getAxis('bottom').range