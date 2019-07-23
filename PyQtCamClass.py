import cv2
import os
from PyQt4 import QtCore
from PyQt4 import QtGui

from CV2FacRecClass import *
    
class ShowVideo(QtCore.QObject):
 
    def __init__(self, parent = None):
        super(ShowVideo, self).__init__(parent)
        #get the local directory
        self.localDir = os.path.dirname(os.path.realpath(__file__)) 
        #facial recognission variables
        self.faceRec = facial_recognition()
        self.training_data_folder = 'training-data'
        self.face_recker = None    
        #set the pause screen image
        self.pauseImageDir = self.localDir + '\images\FaceRecRFWait.png'
        self.pause_image = QtGui.QImage(self.pauseImageDir)
        #variables 4 image recording
        self.record = False
        self.recordingFolder = self.localDir + "/recording/"
        self.skip_value = 1
        self.skip_count = 0
        self.record_count = 0
        #variables 4 image recording for training
        self.folderName = "j_ERROR" #folder for captured training images
        self.captureImage = False
        self.captureCount = 0
        #initialize camera
        self.webcamPort = None
        self.camera = None

    video_signal = QtCore.pyqtSignal(QtGui.QImage, name = 'vidSig')
    label_signal = QtCore.pyqtSignal(int)
    
    @QtCore.pyqtSlot()
    def startVideo(self):
        #set the flag used to run the camera
        self.run_video = True
        while self.run_video:
            ret, frame = self.camera.read()
            if ret:                
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
                #Saving a frame for training (this is used by the add face menu)
                if self.captureImage == True:
                    image2save = cv2.cvtColor(predicted_image, cv2.COLOR_RGB2BGR) 
                    cv2.imwrite(self.localDir + "/training-data/" + self.folderName + "/%d.jpg" % self.captureCount,image2save)
                    self.captureCount += 1
                    print "captured image "+ str(self.captureCount) + ".jpg"
                    self.captureImage = False
                        
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
        
class ImageViewer(QtGui.QWidget):
    def __init__(self, parent = None):
        super(ImageViewer, self).__init__(parent)
        #set the default screen image
        self.localDir = os.path.dirname(os.path.realpath(__file__)) 
        self.default_image = self.localDir + '/images/FaceRecRFRecognize.png'
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