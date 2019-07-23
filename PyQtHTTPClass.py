import cv2
import os
from PyQt4 import QtCore
from PyQt4 import QtGui
import urllib 
import numpy as np

from CV2FacRecClass import *
    
class ShowIPVideo(QtCore.QObject):
 
    def __init__(self, parent = None):
        super(ShowIPVideo, self).__init__(parent)
        #get the local directory
        self.localDir = os.path.dirname(os.path.realpath(__file__))
        #facial recognission variables
        self.faceRec = facial_recognition()
        self.training_data_folder = 'training-data'
        self.face_recker = None  
        #image recording variables
        self.record = False
        self.recordingFolder = self.localDir + "/recording/"
        self.skip_value = 1
        self.skip_count = 0
        self.record_count = 0  
        #IP Camera variables
        self.httpAddress = 'http://192.168.23.2:4747/mjpegfeed'
        self.stream = 0
        self.bytes = ''
        #set the pause screen image
        self.pauseImageDir = self.localDir + '\images\FaceRecRFWait.png'
        self.pause_image = QtGui.QImage(self.pauseImageDir)
    
    video_signal = QtCore.pyqtSignal(QtGui.QImage, name = 'vidSig')
    label_signal = QtCore.pyqtSignal(int)
    
    @QtCore.pyqtSlot()
    def startVideo(self):
        if self.stream == 0:
            print "Connecting to: ",self.httpAddress
            self.stream = urllib.urlopen(str(self.httpAddress))
        #set the flag used to run the camera
        self.run_video = True
        while self.run_video:
            self.bytes += self.stream.read(1024)
            a = self.bytes.find('\xff\xd8')
            b = self.bytes.find('\xff\xd9')
            if a != -1 and b != -1:
                jpg = self.bytes[a:b+2]
                self.bytes = self.bytes[b+2:]
                frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
                #convert the BGR used by openCV to RGB used by PyQt   
                color_swapped_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
                #set default image label ("UNKNOWN")
                image_label = [0]
                if self.face_recker is not None:
                    predicted_image, image_label = self.faceRec.predict(self.face_recker,color_swapped_image)
                else:
                    predicted_image = self.faceRec.justDetect(color_swapped_image)
                height, width, _ = predicted_image.shape
                
                self.qt_image = QtGui.QImage(predicted_image.data,
                                        width,
                                        height,
                                        predicted_image.strides[0],
                                        QtGui.QImage.Format_RGB888)
                #resize pause image
                self.pause_image = self.pause_image.scaled(width,height)
                #emit the detection QImage
                self.emitted_signal = self.video_signal.emit(self.qt_image)
                self.another_signal = self.label_signal.emit(image_label[0])
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
        