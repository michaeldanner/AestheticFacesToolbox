from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap


class ImageLabel(QLabel):
    """ This widget displays an ImagePopup when the mouse enters its region """
    def enterEvent(self, event):
        #self.p = GalleryPopup(self)
        #print(self.p)
        # self.p.populate()
        #self.p.show()
        event.accept()


class GalleryPopup(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self)
        self.setWindowTitle("Image Gallery")
        self.setLayout(QGridLayout(self))

    def populate(self, pics, img_dir):
        row = 0
        col = 0
        print(pics)
        for pic in pics[:200]:
            label = ImageLabel("")
            pixmap = QPixmap(img_dir + '/' + pic.split(' ')[0])
            # print(img_dir + '/' + pic)
            pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatioByExpanding)
            label.setPixmap(pixmap)
            self.layout().addWidget(label, row, col)
            col += 1
            if col % 20 == 0:
                row += 1
                col = 0
