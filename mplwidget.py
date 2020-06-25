from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.fig = Figure()
        self.canvas = FigureCanvasQTAgg(self.fig)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        # THESE TWO LINES WERE ADDED
        self.canvas.setFocusPolicy(Qt.ClickFocus)
        self.canvas.setFocus()

        self.canvas.axes = self.fig.add_subplot(111)
        self.setLayout(vertical_layout)

    def on_press(self, event):
        print("press")
        print("event.xdata", event.xdata)
        print("event.ydata", event.ydata)
        print("event.inaxes", event.inaxes)
        print("x", event.x)
        print("y", event.y)

    def on_release(self, event):
        print("release:")
        print("event.xdata", event.xdata)
        print("event.ydata", event.ydata)
        print("event.inaxes", event.inaxes)
        print("x", event.x)
        print("y", event.y)
