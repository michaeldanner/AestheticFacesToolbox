import sys, csv
from PIL import Image
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QEvent
from datamatrix import DataMatrix


def rgb_to_hsv(r, g, b):
    r = float(r)
    g = float(g)
    b = float(b)
    high = max(r, g, b)
    low = min(r, g, b)
    h, s, v = high, high, high

    d = high - low
    s = 0 if high == 0 else d / high

    if high == low:
        h = 0.0
    else:
        h = {
            r: (g - b) / d + (6 if g < b else 0),
            g: (b - r) / d + 2,
            b: (r - g) / d + 4,
        }[high]
        h /= 6

    return h, s, v


class DsMainWindow(QMainWindow):
    quantity = 0
    id = []
    image_list = []
    attr = []
    ethnic = []
    age = []
    haircolor = []
    skincolor = []
    image_id = []

    def __init__(self, parent=None):
        super(DsMainWindow, self).__init__(parent)
        uic.loadUi('dataset.ui', self)
        qApp.installEventFilter(self)
        # self.tbl_dataset = QTableWidget()
        self.actionSave_Dataset.triggered.connect(self.file_save)
        self.actionGenerate_Dataset.triggered.connect(self.generate_data)
        self.actionLoad_Dataset.triggered.connect(self.load_data)
        self.actionExit.triggered.connect(sys.exit)
        self.show()

    def file_save(self):
        print("saving file")
        try:
            name = QFileDialog.getSaveFileName(self, 'Save File', '', 'CSV(*.csv)')
            stream = open(name[0], 'w')
            writer = csv.writer(stream)
            for row in range(self.tbl_dataset.rowCount()):
                rowdata = []
                for col in range(self.tbl_dataset.columnCount()):
                    if col == 1:
                        pass
                    else:
                        item = self.tbl_dataset.item(row, col)
                    if item is not None:
                        rowdata.append(item.text())
                    else:
                        rowdata.append('')
                writer.writerow(rowdata)
        except Exception as err:
            print("ERROR in File save: " + err)
        print("saving ends")

    def load_data(self):
        print("loading csv file")
        try:
            fname = QFileDialog.getOpenFileName(self, 'Save File', '', 'CSV(*.csv)')
        except Exception as err:
            print("Error in loading CSV File" + err)
        self.id = []
        self.image_list = []
        self.age = []
        self.attr = []
        self.ethnic = []
        self.haircolor = []
        self.skincolor = []
        self.image_id = []
        self.quantity = 0
        with open(fname[0]) as csvfile:
            stream = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in stream:
                if row:
                    self.id.append(row[1])
                    self.image_list.append(row[2])
                    self.age.append(row[3])
                    self.attr.append(row[4])
                    self.ethnic.append(row[5])
                    self.haircolor.append(row[6])
                    self.skincolor.append(row[7])
                    self.image_id.append(row[8])
                    self.quantity += 1
        csvfile.close()
        self.show_table()

    def generate_data(self):
        dm = DataMatrix('example/anno.dat', 'example/out2020/', 'example/Pictures2020/', 'example/', 'example/age.txt', 20)
        self.quantity, self.image_list = dm.load_dataset()
        print(self.quantity)
        self.attr = []
        self.id = []
        for row in range(self.quantity):
            self.id.append(row)
        file = open('example/scores.txt', 'r')
        for line in file:
            if line.strip().rstrip('\n') != '':
                self.attr.append(float(line.rstrip('\n')))
        file.close()
        self.ethnic = []
        file = open('example/ethnicity.txt', 'r')
        for line in file:
            if line.strip().rstrip('\n') != '':
                self.ethnic.append(float(line.rstrip('\n')))
        file.close()
        file = open('example/age.txt', 'r')
        for line in file:
            if line.strip().rstrip('\n') != '':
                self.age.append(float(line.rstrip('\n')))
        file.close()
        self.show_table()

    def show_table(self):
        self.tbl_dataset.setRowCount(self.quantity)
        for row in range(self.quantity):
            # ID
            item = str(self.id[row])
            self.tbl_dataset.setItem(row, 0, QTableWidgetItem(item))
            # Image 100x100
            pic = QPixmap('example/Pictures2020/' + self.image_list[row])
            label = QLabel()
            label.setPixmap(pic.scaled(100, 100))
            self.tbl_dataset.setCellWidget(row, 1, label)
            # Image name
            item = self.image_list[row]
            self.tbl_dataset.setItem(row, 2, QTableWidgetItem(item))
            # Age
            age = float(self.age[row])
            item = f"{age:.0f}"
            self.tbl_dataset.setItem(row, 3, QTableWidgetItem(item))
            # Aesthetic score
            attr = float(self.attr[row])
            item = f"{attr:.3f}"
            self.tbl_dataset.setItem(row, 4, QTableWidgetItem(item))
            # Ethnicity
            ethnicity = float(self.ethnic[row])
            item = f"{ethnicity:.3f}"
            self.tbl_dataset.setItem(row, 5, QTableWidgetItem(item))
            # Hair Color
            item = self.haircolor[row]
            # img = Image.open('example/Pictures2020/' + self.image_list[row])
            # img = img.crop((110, 10, 156, 46))
            # # img.save('example/tmp/tmp' + str(row) + '.jpg')
            # img2 = img.resize((1, 1))
            # # img2.save('example/tmp/tmp2' + str(row) + '.jpg')
#
            # color = img2.getpixel((0, 0))
            # h, s, v = rgb_to_hsv(color[0], color[1], color[2])
            # item = f"{h*100:.0f} {s*100:.0f} {v:.0f}"
            self.tbl_dataset.setItem(row, 6, QTableWidgetItem(item))
            # if v <= 20:
            #     self.tbl_dataset.setItem(row, 6, QTableWidgetItem("black"))
            # elif v > 50 and s > 0.5 and h < 0.1:
            #     self.tbl_dataset.setItem(row, 6, QTableWidgetItem("red"))
            # elif 20 < v <= 60:
            #     self.tbl_dataset.setItem(row, 6, QTableWidgetItem("dark brown"))
            # elif 60 < v <= 95:
            #     self.tbl_dataset.setItem(row, 6, QTableWidgetItem("light brown"))
            # elif v > 95 and s > 0.20:
            #     self.tbl_dataset.setItem(row, 6, QTableWidgetItem("blonde"))
            # elif v > 95 and s <= 0.2:
            #     self.tbl_dataset.setItem(row, 6, QTableWidgetItem("grey"))
            # # Skin color
            # try:
            #     _, item = self.image_list[row].split('_TEINT_')
            # except:
            #     item = self.image_list[row][-15:]
            # item, _ = item.split('.jpg')
            # Skin color
            item = self.skincolor[row]
            self.tbl_dataset.setItem(row, 7, QTableWidgetItem(item))
            # Image ID
            _, item = self.image_list[row].split('/')
            item, _ = item.split('dummy')
            self.tbl_dataset.setItem(row, 8, QTableWidgetItem(item))

            # Asian / Caucasian proof
            # _, item = self.image_list[row].split('ETHNICITY_')
            # try:
            #     item, _ = item.split('_TEINT')
            # except:
            #     self.tbl_dataset.item(row, 5).setBackground(QColor(255, 0, 0))
            # if float(ethnicity) < 0.5 and item == 'asian':
            #     self.tbl_dataset.item(row, 5).setBackground(QColor(222, 150, 0))
            # elif float(ethnicity) > 0.5 and item == 'caucasian':
            #     self.tbl_dataset.item(row, 5).setBackground(QColor(50, 50, 252))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ds = DsMainWindow()
    sys.exit(app.exec_())

