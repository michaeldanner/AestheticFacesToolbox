import sys, os
import numpy as np
from datamatrix import DataMatrix
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QEvent

from mplwidget import MplWidget
from matplotlib import colors
from gallerypopup import GalleryPopup


class fr_MainWindow(QMainWindow):
    image_list = []
    age_data = None

    def __init__(self, parent=None):
        super(fr_MainWindow, self).__init__(parent)
        uic.loadUi('aesthetics.ui', self)
        qApp.installEventFilter(self)
        # self.setupUi(self)
        path = 'example/'
        path = 'C:/tmp/aesthetics/'

        self.btn_img_dir.clicked.connect(self.buttonClicked)
        self.btn_img_list.clicked.connect(self.buttonClicked)
        self.btn_anno_dir.clicked.connect(self.buttonClicked)
        self.btn_out_dir.clicked.connect(self.buttonClicked)
        self.btn_start.clicked.connect(self.buttonClicked)
        self.btn_ages_list.clicked.connect(self.buttonClicked)
        self.attr_widget.canvas.mpl_connect('button_press_event', self._on_press)
        self.ac_widget2.canvas.mpl_connect('button_press_event', self._on_press_ac)

        self.lbl_out_dir.setText(str(path) + '')
        self.lbl_img_dir.setText(str(path) + '')
        self.lbl_img_dir.setText(str(path) + 'Pictures2020')
        self.lbl_anno_dir.setText(str(path) + 'out2020')
        self.lbl_img_list.setText(str(path) + 'anno.dat')
        self.lbl_ages_list.setText(str(path) + 'age.txt')
        self.show()

    @pyqtSlot(QWidget)
    def _on_press(self, event):
        print(event)
        self.gpop = GalleryPopup(self)
        self.gpop.setGeometry(50, 50, 600, 400)
        self.gpop.populate(self.image_list, self.lbl_img_dir.text())
        self.gpop.show()

    @pyqtSlot(QWidget)
    def _on_press_ac(self, event):
        print(event)
        self.gpop = QDialog(self)
        # plot correlation of age and aesthetics
        min, max, attr, avg, var, ethnic = self.age_data
        x = list(range(min, max))
        self.acw = MplWidget(self.centralwidget)
        self.acw.setObjectName(u"ac_widget2")
        self.acw.setMinimumSize(QSize(100, 50))

        self.gpop.setLayout(QGridLayout(self))
        self.gpop.layout().addWidget(self.acw)
        self.acw.canvas.figure.clear()
        ax = self.acw.canvas.figure.subplots()
        ax.clear()
        ax.set_title('Correlation of Aesthetics and Age')

        for i in range(0, max - min):
            for score in range(len(attr[i])):
                co = ethnic[i][score]
                ax.plot(min + i, attr[i][score], '.', color=(co, .1, 1 - co))
        ax.plot(x, avg, '-', color='b')

        self.acw.canvas.draw()
        self.gpop.setGeometry(50, 50, 1200, 800)
        self.gpop.show()

    def showdialog(self, title, text, info, details):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText(text)
        msg.setInformativeText(info)
        msg.setWindowTitle(title)
        msg.setDetailedText(details)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        retval = msg.exec_()
        print("value of pressed message box button:", retval)

    def start_evaluation(self, tol):
        dm = DataMatrix(self.lbl_img_list.text(), self.lbl_anno_dir.text(), self.lbl_img_dir.text(),
                        self.lbl_out_dir.text(), self.lbl_ages_list.text(), tol)
        self.image_list = dm.image_list
        self.plainTextEdit.setPlainText(dm.get_dataset_properties())
        # insert data in table:
        tbl = dm.table_annodata

        self.tbl_anno_data.setRowCount(np.size(tbl, 0))
        self.tbl_anno_data.setColumnCount(np.size(tbl, 1))
        self.tbl_anno_data.setHorizontalHeaderLabels(['sc', 'matr', 'age', 'g', 'no.', 'a%', 'state', 'd0', 'd1',
                                                    'd0%', 'd1%'])
        try:
            self.tbl_anno_data.clearContents()
        except Exception as err:
            print(err)

        try:
            for row in range(np.size(tbl, 0)):
                for column in range(np.size(tbl, 1)):
                    try:
                        item = str(tbl[row][column].decode("utf-8"))
                        self.tbl_anno_data.setItem(row, column, QTableWidgetItem(item))
                    except Exception as err:
                        pass  # print("unknown error" + str(err))
        except Exception as err:
            print("unknown error in table" + str(err))

        # plot histogram 1
        self.hist1_widget.canvas.figure.clear()
        ax = self.hist1_widget.canvas.figure.subplots()
        ax.clear()
        ax.hist(dm.hist1_canvas, bins=8)
        self.hist1_widget.canvas.draw()

        # plot histogram 2
        self.hist2_widget.canvas.figure.clear()
        ax = self.hist2_widget.canvas.figure.subplots()
        ax.clear()
        ax.hist(dm.hist2_canvas, bins=30)
        self.hist2_widget.canvas.draw()

        # plot histogram 2
        self.hist3_widget.canvas.figure.clear()
        ax = self.hist3_widget.canvas.figure.subplots()
        ax.clear()
        ax.hist(dm.num_value_0_with_large_sc, bins=100)
        self.hist3_widget.canvas.draw()

        # plot histogram 2
        self.hist4_widget.canvas.figure.clear()
        ax = self.hist4_widget.canvas.figure.subplots()
        ax.clear()
        ax.hist(dm.num_value_1_with_small_sc, bins=100)
        self.hist4_widget.canvas.draw()

        # plot miss attractive
        self.attr_widget.canvas.figure.clear()
        ax = self.attr_widget.canvas.figure.subplots()
        ax.clear()
        ax.axis('off')
        ax.set_title('Miss Aesthetics')
        ax.imshow(dm.attr_canvas)
        self.attr_widget.canvas.draw()

        # plot histogram ethnicity aesthetics
        self.ac_widget.canvas.figure.clear()
        ax = self.ac_widget.canvas.figure.subplots()
        ax.clear()
        x = dm.ethnic
        y = dm.score_list

        x, y = zip(*sorted((xVal, np.mean([yVal for a, yVal in zip(x, y) if xVal == a])) for xVal in set(x)))
        ax.plot(x, y, '-', color='b')
        self.ac_widget.canvas.draw()

        # plot correlation of age and aesthetics
        self.age_data = dm.get_age_data()
        min, max, attr, avg, var, ethnic = self.age_data

        x = list(range(min, max))
        self.ac_widget2.canvas.figure.clear()
        ax = self.ac_widget2.canvas.figure.subplots()
        ax.clear()
        ax.set_title('Correlation of Aesthetics and Age')
        for i in range(0, max - min):
            for score in range(len(attr[i])):
                norm = colors.Normalize(0, 10)
                co = ethnic[i][score]
                ax.plot(min + i, attr[i][score], '.', color=(.99*co, .5-0.5*co, .8-.8*co))

        ax.plot(x, avg, '-', color='b')

        self.ac_widget2.canvas.draw()

    def buttonClicked(self):
        sender = self.sender()
        print(sender)

        if sender.text() == 'Image Textfile':
            # self.rot += 0.1
            fname = QFileDialog.getOpenFileName(self, 'Open file',
                                                filter="Aesthetics data file (*.dat *.txt)")
            self.lbl_img_list.setText(fname[0])

        elif sender.text() == 'Image directory':
            print("> you pressed " + sender.text())
            fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
            self.lbl_img_dir.setText(fname)

        elif sender.text() == 'Annotations directory':
            fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
            self.lbl_anno_dir.setText(fname)

        elif sender.text() == 'Output directory':
            fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
            self.lbl_out_dir.setText(fname)

        elif sender.text() == 'Ages Textfile':
            fname = QFileDialog.getOpenFileName(self, 'Open file',
                                                filter="Aesthetics data file (*.dat *.txt)")
            self.lbl_ages_list.setText(fname[0])

        elif sender.text() == 'Start Evaluation':
            tol = 0
            details = ''
            error = False
            try:
                tol = int(self.lineEdit.text())
            except:
                tol = None
            if not isinstance(tol, int) or tol > 99:
                error = True
                details += "Insert a valid integer to Tolerance input field\n"
            if not os.path.isfile(self.lbl_ages_list.text()):
                error = True
                details += "Select a valid Ages Textfile\n"
            if not os.path.isfile(self.lbl_img_list.text()):
                error = True
                details += "Select a valid Image Textfile\n"
            if not os.path.isdir(self.lbl_anno_dir.text()):
                error = True
                details += "Select a valid Annotation Directory\n"
            if not os.path.isdir(self.lbl_img_dir.text()):
                error = True
                details += "Select a valid Image Directory\n"
            if not os.path.isdir(self.lbl_out_dir.text()):
                error = True
                details += "Select a valid Output Directory\n"

            if error:
                self.showdialog("Evaluation Error", "Invalid value detected.", "Evaluation could not be started.",
                                details)
            else:
                self.start_evaluation(tol)


if __name__ == "__main__":
    # app = QApplication(sys.argv)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    # ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)
    fr = fr_MainWindow()
    # MainWindow.show()
    # ex = App()
    sys.exit(app.exec_())
else:
    # path = 'example/'
    path = 'c:/tmp/aesthetics/'
    f = path + 'out2020'
    load = path + 'anno.dat'
    image = path + ''
    image = path + 'Pictures2020/'
    out = path + ''
    age = path + 'age.txt'
    dm = DataMatrix(load, f, image, out, age, 9)
