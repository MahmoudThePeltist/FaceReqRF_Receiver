from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import sys
from socket import *

from CV2FacRecClass import *
from DialogError import *

class ShowReceivedVideo(QtCore.QObject):
 
    def __init__(self, parent = None):
        super(ShowReceivedVideo, self).__init__(parent)
        #get the local directory
        if getattr(sys, 'frozen', False):
            # The application is frozen
            self.localDir = os.path.dirname(sys.executable)
        else:
            # The application is not frozen
            self.localDir = os.path.dirname(os.path.realpath(__file__))    
        #facial recognission variables
        self.faceRec = facial_recognition()
        self.training_data_folder = 'training-data'
        self.detMethod = 1
        self.recMethod = 2
        self.face_recker = None
        #image recording variables
        self.record = False
        self.recordingFolder = self.localDir + "/recording/"
        self.skip_value = 1
        self.skip_count = 0
        self.record_count = 0
        #Socket variables
        self.host = gethostbyname(gethostname())
        self.port = 4096
        self.buf = 1024
        self.fName = self.localDir + '/frames/frame.jpg'
        #set the pause screen image
        self.pauseImageDir = self.localDir + '\images\FaceRecRFWait.png'
        self.pause_image = QImage(self.pauseImageDir)
        self.useXML = 0
    
    video_signal = QtCore.pyqtSignal(QImage, name = 'vidSig')
    label_signal = QtCore.pyqtSignal(tuple)
    
    @QtCore.pyqtSlot()
    def startVideo(self):
        self.faceRec.faceDetector = self.detMethod
        self.faceRec.faceRecognizer = self.recMethod
        print("\nWe are using face detector: " + str(self.faceRec.faceDetector))
        print("We are using face recognizer: " + str(self.faceRec.faceRecognizer))
        #set the flag used to run the camera
        self.run_video = True
        #open a socket that communicates with Internet Protocol v4 addresses (AF_INET) using UDP (SOCK_DGRAM)
        s = socket()
        self.addr = (self.host, self.port)
        print("Reciving from: ", self.addr)
        s.bind(self.addr)
        while self.run_video:
            f = open(self.localDir + '/frames/frame.jpg', 'wb')
            s.listen(5)                    
            c, addr = s.accept()     # Establish connection with client.
            print('Got connection from', addr)
            print("Receiving...")
            l = c.recv(self.buf)
            while (l):
                f.write(l)
                l = c.recv(self.buf)
            f.close()   # Close the recived file
            print("Done Receiving")
            c.send('Thank you for connecting')
            c.close()    # Close the connection            
            frame = cv2.imread(self.localDir + '/frames/frame.jpg')
            #convert the BGR used by openCV to RGB used by PyQt
            color_swapped_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #set default image label ("UNKNOWN")
            image_label = (0,0)
            #load a pretrained recognizer XML file
            if self.face_recker is None and self.useXML is 1:
                print("No recognizer found, attepting to load one.")
                self.face_recker = self.faceRec.load_recognizer(self.recMethod)
            #perform recognition if recognizer exists
            if self.face_recker is not None:
                predicted_image, image_label = self.faceRec.predict(self.face_recker,color_swapped_image)
            else:
                predicted_image = self.faceRec.justDetect(color_swapped_image)
            height, width, _ = predicted_image.shape
            
            self.qt_image = QImage(predicted_image.data,
                                    width,
                                    height,
                                    predicted_image.strides[0],
                                    QImage.Format_RGB888)
            #resize pause image
            self.pause_image = self.pause_image.scaled(width,height)
            #emit the detection QImage
            self.emitted_signal = self.video_signal.emit(self.qt_image)
            self.another_signal = self.label_signal.emit(image_label)
            #Recording all predicted frames in recording folder after reconverting the color
            if self.record == True:
                self.skip_count += 1
                if self.skip_count > self.skip_value:                        
                    image2save = cv2.cvtColor(predicted_image, cv2.COLOR_RGB2BGR) 
                    cv2.imwrite(self.recordingFolder + "img%d.jpg" % self.record_count,image2save)
                    self.record_count += 1
                    self.skip_count = 0
            
        #set the default image and transmit it
        self.emitted_signal = self.video_signal.emit(self.pause_image)
                    
    def prepare_pics(self, detMethod):
        try:
            self.faceRec.faceDetector = detMethod #Set the detector
            self.faceRec.prepare_training_images(self.training_data_folder)#create all training images
        except Exception as e:
            print("Training exception check settings.\nException:" + str(e))
            errorBox("Writing exception check settings.\nException:" + str(e))
        
    def train_algorithm(self, recMethod):
        try:
            self.faceRec.faceRecognizer = recMethod #Set the recogizer
            self.face_recker = self.faceRec.train(self.training_data_folder)#train and return recognizer
        except Exception as e:
            print("Training exception check settings.\nException:" + str(e))
            errorBox("Writing exception check settings.\nException:" + str(e))
        
    def unpause_video(self):
        #this is called if the signal is disconnected
        self.video_signal.emit(self.qt_image)
        
    def set_values(self, gottenMethod, gottenAddress, gottenPort, gottenBuffer, gottenUseXML):
        self.transMeth = gottenMethod
        self.host = gottenAddress
        self.port = gottenPort
        self.buf = gottenBuffer
        self.useXML = gottenUseXML