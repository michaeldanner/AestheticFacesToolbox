import sys, csv
from PIL import Image
import webcolors
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QEvent
from datamatrix import DataMatrix


def _reversedict(d: dict) -> dict:
    """
    Internal helper for generating reverse mappings; given a
    dictionary, returns a new dictionary with keys and values swapped.

    """
    return {value: key for key, value in d.items()}


HAIRCOLOR_NAMES_TO_HEX = {
    "black": "#000000",
    "blond": "#d2b48c",
    "brown": "#352118",
    "darkbrown": "#1d130e",
    "lightbrown": "#4a3014",
    "red": "#4a1414",
    "grey": "#606060",
    "snow": "#fffafa"
}

HAIRCOLOR_HEX_TO_NAMES = _reversedict(HAIRCOLOR_NAMES_TO_HEX)


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in HAIRCOLOR_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_colour_name(requested_colour):
    closest_name = closest_colour(requested_colour)

    return closest_name


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


def read_file(fname, dtype='float'):
    item_list = []
    file = open(fname, 'r')
    for line in file:
        if line.strip().rstrip('\n') != '':
            if dtype == 'float':
                item_list.append(float(line.rstrip('\n')))
            else:
                item_list.append(line.rstrip('\n'))
    file.close()
    return item_list


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
        self.tbl_dataset.clear()
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

    def generate_data(self, hair_color=True):
        self.tbl_dataset.clear()
        dm = DataMatrix('example/anno.dat', 'example/out2020/', 'example/Pictures2020/', 'example/', 'example/age.txt', 20)
        # filenames
        self.quantity, self.image_list = dm.load_dataset()
        print(self.quantity)
        self.attr = []
        # id
        self.id = []
        for row in range(self.quantity):
            self.id.append(row+1)

        # aesthetic score - attractiveness
        self.attr = read_file('example/scores.txt')

        # ethnicity
        self.ethnic = read_file('example/ethnicity.txt')

        # age
        self.age = read_file('example/age.txt')

        # haircolor
        if True:
            self.haircolor = read_file('example/haircolor.txt', dtype='string')
        else:
            self.haircolor = []
            for row in range(self.quantity):

                img = Image.open('example/Pictures2020/' + self.image_list[row])
                img = img.crop((110, 10, 156, 46))
                img.save('example/tmp/tmp_' + str(row) + '.jpg')
                img2 = img.resize((1, 1))
                img2.save('example/tmp/tmp2_' + str(row) + '.jpg')
                color = img2.getpixel((0, 0))
                h, s, v = rgb_to_hsv(color[0], color[1], color[2])
                item = f"{h*100:.0f} {s*100:.0f} {v:.0f}"
                if v <= 20:
                    self.haircolor.append("black " + item)
                elif v > 50 and s > 0.5 and h < 0.1:
                    self.haircolor.append("red " + item)
                elif 20 < v <= 60:
                    self.haircolor.append("dark brown " + item)
                elif 60 < v <= 95:
                    self.haircolor.append("light brown " + item)
                elif v > 95 and s > 0.20:
                    self.haircolor.append("blond " + item)
                elif v > 95 and s <= 0.2:
                    self.haircolor.append("grey " + item)

        # Skin color
        # try:
        #     _, item = self.image_list[row].split('_TEINT_')
        # except:
        #     item = self.image_list[row][-15:]
        # item, _ = item.split('.jpg')

        self.skincolor = []
        for row in range(self.quantity):
            self.skincolor.append("1")
        # show the table
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

            # Image filename
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
            b, g, r = item.split('/')
            r, _ = r.split(' ')
            cname = get_colour_name((int(r), int(g), int(b)))
            item += ' '
            self.tbl_dataset.setItem(row, 6, QTableWidgetItem(item))
            self.tbl_dataset.setItem(row, 11, QTableWidgetItem(cname))

            # Skin color
            item = self.skincolor[row]
            self.tbl_dataset.setItem(row, 7, QTableWidgetItem(item))

            # Image ID
            _, item = self.image_list[row].split('/')
            item, _ = item.split('dummy')
            self.tbl_dataset.setItem(row, 8, QTableWidgetItem(item))

            # Image 100x100
            pic = QPixmap('example/tmp/tmp_' + str(row) + '.jpg')
            label = QLabel()
            label.setPixmap(pic.scaled(100, 100))
            self.tbl_dataset.setCellWidget(row, 9, label)

            if row < 0:
                # Image Histogram 100x100
                pic = QPixmap('example/tmp/tmp3_' + str(row) + '.jpg')
                label = QLabel()
                label.setPixmap(pic.scaled(300, 100))
                self.tbl_dataset.setCellWidget(row, 8, label)

            # Image 100x100
            try:
                pic = QPixmap(100, 100)
                r,g,b = self.haircolor[row].split('/')
                b, _ = b.split(' ')
                pic.fill(QColor(int(b), int(g), int(r)))
                label = QLabel()
                label.setPixmap(pic.scaled(100, 100))
                self.tbl_dataset.setCellWidget(row, 10, label)

            except Exception as err:
                print("ERROR in haircolor: " + err)

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

