from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.fig = Figure()
        self.canvas = FigureCanvasQTAgg(self.fig)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.fig.add_subplot(111)
        self.setLayout(vertical_layout)
