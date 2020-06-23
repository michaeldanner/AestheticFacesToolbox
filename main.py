import sys

from datamatrix import DataMatrix
from PyQt5.QtCore import QCoreApplication, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets

from mplwidget import MplWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1089, 681)
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.log_grid = QGridLayout()
        self.log_grid.setObjectName(u"log_grid")
        self.output_log = QPlainTextEdit(self.centralwidget)
        self.output_log.setObjectName(u"output_log")
        self.output_log.setMinimumSize(QSize(450, 0))

        self.log_grid.addWidget(self.output_log, 0, 1, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(-1, -1, 0, -1)
        self.hist1_widget = MplWidget(self.centralwidget)
        self.hist1_widget.setObjectName(u"hist1_widget")
        self.hist1_widget.setMinimumSize(QSize(100, 50))

        self.verticalLayout.addWidget(self.hist1_widget)

        self.hist2_widget = MplWidget(self.centralwidget)
        self.hist2_widget.setObjectName(u"hist2_widget")
        self.hist2_widget.setMinimumSize(QSize(100, 50))

        self.verticalLayout.addWidget(self.hist2_widget)

        self.attr_widget = MplWidget(self.centralwidget)
        self.attr_widget.setObjectName(u"attr_widget")
        self.attr_widget.setMinimumSize(QSize(100, 50))

        self.verticalLayout.addWidget(self.attr_widget)


        self.log_grid.addLayout(self.verticalLayout, 0, 4, 1, 1)

        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setMinimumSize(QSize(120, 0))
        self.plainTextEdit.setMaximumSize(QSize(460, 16777215))
        self.plainTextEdit.setFrameShape(QFrame.StyledPanel)
        self.plainTextEdit.setFrameShadow(QFrame.Sunken)
        self.plainTextEdit.setMidLineWidth(1)
        self.plainTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.plainTextEdit.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.plainTextEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.plainTextEdit.setTextInteractionFlags(Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.log_grid.addWidget(self.plainTextEdit, 0, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, -1, 0, -1)
        self.ac_widget2 = MplWidget(self.centralwidget)
        self.ac_widget2.setObjectName(u"ac_widget2")
        self.ac_widget2.setMinimumSize(QSize(100, 50))

        self.verticalLayout_2.addWidget(self.ac_widget2)


        self.log_grid.addLayout(self.verticalLayout_2, 0, 5, 1, 1)


        self.gridLayout_2.addLayout(self.log_grid, 2, 0, 1, 1)

        self.load_grid = QGridLayout()
        self.load_grid.setObjectName(u"load_grid")
        self.load_grid.setSizeConstraint(QLayout.SetFixedSize)
        self.lbl_anno_dir = QLabel(self.centralwidget)
        self.lbl_anno_dir.setObjectName(u"lbl_anno_dir")

        self.load_grid.addWidget(self.lbl_anno_dir, 1, 2, 1, 1)

        self.btn_out_dir = QPushButton(self.centralwidget)
        self.btn_out_dir.setObjectName(u"btn_out_dir")

        self.load_grid.addWidget(self.btn_out_dir, 0, 3, 1, 1)

        self.btn_anno_dir = QPushButton(self.centralwidget)
        self.btn_anno_dir.setObjectName(u"btn_anno_dir")

        self.load_grid.addWidget(self.btn_anno_dir, 0, 2, 1, 1)

        self.lbl_out_dir = QLabel(self.centralwidget)
        self.lbl_out_dir.setObjectName(u"lbl_out_dir")

        self.load_grid.addWidget(self.lbl_out_dir, 1, 3, 1, 1)

        self.btn_img_list = QPushButton(self.centralwidget)
        self.btn_img_list.setObjectName(u"btn_img_list")

        self.load_grid.addWidget(self.btn_img_list, 0, 0, 1, 1)

        self.btn_img_dir = QPushButton(self.centralwidget)
        self.btn_img_dir.setObjectName(u"btn_img_dir")

        self.load_grid.addWidget(self.btn_img_dir, 0, 1, 1, 1)

        self.lbl_img_list = QLabel(self.centralwidget)
        self.lbl_img_list.setObjectName(u"lbl_img_list")

        self.load_grid.addWidget(self.lbl_img_list, 1, 0, 1, 1)

        self.lbl_img_dir = QLabel(self.centralwidget)
        self.lbl_img_dir.setObjectName(u"lbl_img_dir")

        self.load_grid.addWidget(self.lbl_img_dir, 1, 1, 1, 1)

        self.btn_start = QPushButton(self.centralwidget)
        self.btn_start.setObjectName(u"btn_start")

        self.load_grid.addWidget(self.btn_start, 0, 4, 1, 1)


        self.gridLayout_2.addLayout(self.load_grid, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1089, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionSave)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.lbl_anno_dir.setText(QCoreApplication.translate("MainWindow", u"not available", None))
        self.btn_out_dir.setText(QCoreApplication.translate("MainWindow", u"Output directory", None))
        self.btn_anno_dir.setText(QCoreApplication.translate("MainWindow", u"Annotations directory", None))
        self.lbl_out_dir.setText(QCoreApplication.translate("MainWindow", u"not available", None))
        self.btn_img_list.setText(QCoreApplication.translate("MainWindow", u"Image Textfile", None))
        self.btn_img_dir.setText(QCoreApplication.translate("MainWindow", u"Image directory", None))
        self.lbl_img_list.setText(QCoreApplication.translate("MainWindow", u"not available", None))
        self.lbl_img_dir.setText(QCoreApplication.translate("MainWindow", u"not available", None))
        self.btn_start.setText(QCoreApplication.translate("MainWindow", u"Start Evaluation", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi


class fr_MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(fr_MainWindow, self).__init__(parent)
        qApp.installEventFilter(self)
        self.setupUi(self)
        path = 'c:\\tmp\\Attractiveness\\'

        self.btn_img_dir.clicked.connect(self.buttonClicked)
        self.btn_img_list.clicked.connect(self.buttonClicked)
        self.btn_anno_dir.clicked.connect(self.buttonClicked)
        self.btn_out_dir.clicked.connect(self.buttonClicked)
        self.btn_start.clicked.connect(self.buttonClicked)

        self.lbl_out_dir.setText(str(path) + 'Output')
        self.lbl_img_dir.setText(str(path) + 'olympicstomato')
        self.lbl_anno_dir.setText(str(path) + 'attractivenesssurveysolympics')
        self.lbl_img_list.setText(str(path) + 'Output\\images.txt')
        self.show()

    def buttonClicked(self):
        sender = self.sender()

        if sender.text() == 'Image Textfile':
            # self.rot += 0.1
            print("< you pressed " + sender.text())
            fname = QFileDialog.getOpenFileName(self, 'Open file',
                                                'c:\\', "Aesthetics data file (*.dat *.txt)")
            print(fname)
            self.lbl_img_list.setText(fname[0])

        elif sender.text() == 'Image directory':
            print("> you pressed " + sender.text())
            fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
            print(fname)
            self.lbl_img_dir.setText(fname)

        elif sender.text() == 'Annotations directory':
            print("> you pressed " + sender.text())
            fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
            print(fname)
            self.lbl_anno_dir.setText(fname)

        elif sender.text() == 'Output directory':
            print("> you pressed " + sender.text())
            fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
            print(fname)
            self.lbl_out_dir.setText(fname)

        elif sender.text() == 'Start Evaluation':
            dm = DataMatrix(self.lbl_img_list.text(), self.lbl_anno_dir.text(), self.lbl_img_dir.text(),
                            self.lbl_out_dir.text(), 50)
            self.plainTextEdit.setPlainText(dm.get_dataset_properties())
            self.output_log.setPlainText(dm.output_log)
            # plot histogram 1
            self.hist1_widget.canvas.figure.clear()
            ax = self.hist1_widget.canvas.figure.subplots()
            ax.clear()
            ax.hist(dm.hist1_canvas)
            self.hist1_widget.canvas.draw()
            # plot histogram 2
            self.hist2_widget.canvas.figure.clear()
            ax = self.hist2_widget.canvas.figure.subplots()
            ax.clear()
            ax.hist(dm.hist2_canvas)
            self.hist2_widget.canvas.draw()
            # plot miss attractive
            self.attr_widget.canvas.figure.clear()
            ax = self.attr_widget.canvas.figure.subplots()
            ax.clear()
            ax.axis('off')
            ax.set_title('Miss Aesthetics')
            ax.imshow(dm.attr_canvas)
            self.attr_widget.canvas.draw()

            # plot miss attractive
            min, max, attr, avg, var = dm.get_age_data()
            x = list(range(min, max))
            self.ac_widget2.canvas.figure.clear()
            ax = self.ac_widget2.canvas.figure.subplots()
            ax.clear()
            ax.set_title('Correlation of Aesthetics and Age')
            for i in range(0, max-min):
                for score in attr[i]:
                    ax.plot(min+i, score, '.')
                    print(str(min+i) + ' ' + str(score))
            ax.plot(x, avg, '-', color='b')

            self.ac_widget2.canvas.draw()


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


if __name__ == 'x__main__':
    path = 'c:\\tmp\\Attractiveness\\'
    f = str(path) + 'attractivenesssurveysolympics'
    load = str(path) + 'Output\\images.txt'
    image = str(path) + 'olympicstomato'
    out = str(path) + 'Output'
    dm = DataMatrix(load, f, image, out, 50)
