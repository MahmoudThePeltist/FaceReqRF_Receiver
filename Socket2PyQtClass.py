from PyQt4 import QtCore
from PyQt4 import QtGui
import os

from socket import *
from CV2FacRecClass import *

class ShowReceivedVideo(QtCore.QObject):
 
    def __init__(self, parent = None):
        super(ShowReceivedVideo, self).__init__(parent)
        #facial recognission variables
        self.faceRec = facial_recognition()
        self.training_data_folder = 'training-data'
        self.face_recker = None
        #image recording variables
        self.record = False
        self.skip_value = 1
        self.skip_count = 0
        self.record_count = 0
        #Socket variables
        self.host = gethostbyname(gethostname())
        self.port = 4096
        self.buf = 1024
        self.fName = 'frames/frame3.jpg'
        #set the pause screen image
        self.pause_image = QtGui.QImage('images\FaceRecRFWait.png')

    
    video_signal = QtCore.pyqtSignal(QtGui.QImage, name = 'vidSig')
    label_signal = QtCore.pyqtSignal(int)
    
    @QtCore.pyqtSlot()
    def startVideo(self):
        #set the flag used to run the camera
        self.run_video = True
        #open a socket that communicates with Internet Protocol v4 addresses (AF_INET) using UDP (SOCK_DGRAM)
        s = socket()
        self.addr = (self.host, self.port)
        print "Reciving from: ", self.addr
        s.bind(self.addr)
        while self.run_video:
            f = open('frames/frame3.jpg', 'wb')
            s.listen(5)                    
            c, addr = s.accept()     # Establish connection with client.
            print 'Got connection from', addr
            print "Receiving..."
            l = c.recv(self.buf)
            while (l):
                f.write(l)
                l = c.recv(self.buf)
            f.close()   # Close the recived file
            print "Done Receiving"
            c.send('Thank you for connecting')
            c.close()    # Close the connection            
            frame = cv2.imread('frames/frame3.jpg')
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
            #Recording all predicted frames in recording folder after reconverting the color
            if self.record == True:
                self.skip_count += 1
                if self.skip_count > self.skip_value:                        
                    image2save = cv2.cvtColor(predicted_image, cv2.COLOR_RGB2BGR) 
                    cv2.imwrite("recording/img%d.jpg" % self.record_count,image2save)
                    self.record_count += 1
                    self.skip_count = 0
            
        #set the default image and transmit it
        self.emitted_signal = self.video_signal.emit(self.pause_image)
                    
    def prepare_pics(self, detMethod):
        self.faceRec.faceDetector = detMethod #Set the detector
        #create all training images
        self.faceRec.prepare_training_images(self.training_data_folder)

    def train_algorithm(self, recMethod):
        self.faceRec.faceRecognizer = recMethod #Set the recogizer
        #train and return recognizer
        self.face_recker = self.faceRec.train(self.training_data_folder)
        
    def unpause_video(self):
        #this is called if the signal is disconnected
        self.video_signal.emit(self.qt_image)
        
    def set_values(self, gottenMethod, gottenAddress, gottenPort, gottenBuffer):
        self.transMeth = gottenMethod
        self.host = gottenAddress
        self.port = gottenPort
        self.buf = gottenBuffer
        
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