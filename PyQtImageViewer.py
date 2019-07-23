from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import os
import sys

class ImageViewer(QWidget):
    """Play the image stream inside the image viewer"""
    
    def __init__(self, parent = None):
        super(ImageViewer, self).__init__(parent)
        #get the local directory
        if getattr(sys, 'frozen', False):
            # The application is frozen
            self.localDir = os.path.dirname(sys.executable)
        else:
            # The application is not frozen
            self.localDir = os.path.dirname(os.path.realpath(__file__)) 
        #set the default screen image 
        self.default_image = self.localDir + '/images/FaceRecRFRecognize.png'
        self.image = QImage(self.default_image,"PNG")
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
 
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0,0, self.image)
        self.image = QImage()
 
    @QtCore.pyqtSlot(QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")
        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()