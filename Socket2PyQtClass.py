from PyQt4 import QtCore
from PyQt4 import QtGui

from socket import *
from CV2FacRecClass import *

class ShowReceivedVideo(QtCore.QObject):
 
    def __init__(self, parent = None):
        super(ShowReceivedVideo, self).__init__(parent)
        self.faceRec = facial_recognition()
        self.training_data_folder = 'training-data'
        self.face_recker = None
        #set the pause screen image
        self.pause_image = QtGui.QImage('images\FaceRecRFWait.png')
        self.host = "127.0.0.1"
        self.port = 4096
        self.buf = 1024
        self.fName = 'frames/frame3.jpg'
        self.timeOut = 0.05
        self.addr = (self.host, self.port)

    
    video_signal = QtCore.pyqtSignal(QtGui.QImage, name = 'vidSig')
    label_signal = QtCore.pyqtSignal(int)
    
    @QtCore.pyqtSlot()
    def startVideo(self):
        #set the flag used to run the camera
        self.run_video = True
        while self.run_video:
            s = socket(AF_INET, SOCK_DGRAM)
            s.bind(self.addr)
            
            data, address = s.recvfrom(self.buf)
            f = open(data, 'wb')
            
            data, address = s.recvfrom(self.buf)
            
            try:
                while(data):
                    f.write(data)
                    s.settimeout(self.timeOut)
                    data, address = s.recvfrom(self.buf)
            except timeout:
                f.close()
                s.close()
            frame = cv2.imread(self.fName)
            #convert the BGR used by openCV to RGB used by PyQt   
            color_swapped_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
            #set default image label ("UNKNOWN")
            image_label = [0]
            if self.face_recker is not None:
                predicted_image, image_label = self.faceRec.predict(self.face_recker,color_swapped_image)
            else:
                predicted_image = color_swapped_image
            height, width, _ = predicted_image.shape
            
            self.qt_image = QtGui.QImage(predicted_image.data,
                                    width,
                                    height,
                                    predicted_image.strides[0],
                                    QtGui.QImage.Format_RGB888)
                                        
            self.emitted_signal = self.video_signal.emit(self.qt_image)
            self.another_signal = self.label_signal.emit(image_label[0])
            
        #set the default image and transmit it
        self.emitted_signal = self.video_signal.emit(self.pause_image)
                    
        
    def prepare_pics(self):
        #create all training images
        self.faceRec.prepare_training_images(self.training_data_folder)

    def train_algorithm(self):        
        #train and return recognizer
        self.face_recker = self.faceRec.train(self.training_data_folder)
        
    def unpause_video(self):
        #this is called if the signal is disconnected
        self.video_signal.emit(self.qt_image)
        
    def set_values(self, gottenMethod, gottenAddress, gottenPort, gottenBuffer, gottenTimeout):
        self.transMeth = gottenMethod
        self.host = gottenAddress
        self.port = gottenPort
        self.buf = gottenBuffer
        self.timeOut = gottenTimeout
        
class ReceivedImageViewer(QtGui.QWidget):
    def __init__(self, parent = None):
        super(ReceivedImageViewer, self).__init__(parent)
        #set the default screen image
        self.default_image = 'images\FaceRecRFRecognize.png'
        self.image = QtGui.QImage(self.default_image,"PNG")
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
 
 
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0,0, self.image)
        self.image = QtGui.QImage()
 
    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")
 
        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()