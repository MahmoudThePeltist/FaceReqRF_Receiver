import win32gui
import win32ui
import os
import sys
from ctypes import windll
from PIL import Image
from PyQt4 import QtCore
from PyQt4 import QtGui
import numpy 
import cv2

from CV2FacRecClass import *
from DialogError import *

class windowCapture(QtCore.QObject):
    
    def __init__(self, parent = None):
        super(windowCapture, self).__init__(parent)
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
        self.face_recker = None
        #set the pause screen image
        self.pauseImageDir = self.localDir + '\images\FaceRecRFWait.png'
        self.pause_image = QtGui.QImage(self.pauseImageDir)
        #image recording variables
        self.record = False
        self.recordingFolder = self.localDir + "/recording/"
        self.skip_value = 1
        self.skip_count = 0
        self.record_count = 0
        #screen capture values
        self.capWindowName = '440'
        self.capWindowResize = 1
        self.cropX1 = 0
        self.cropY1 = 30
        self.cropX2 = 0
        self.cropY2 = 0
        self.toplist, self.winlist = [], []
        self.hwnd = 0
        self.windowHeight = 700
        
    video_signal = QtCore.pyqtSignal(QtGui.QImage, name = 'vidSig')
    label_signal = QtCore.pyqtSignal(int)
    
    @QtCore.pyqtSlot()
    def startVideo(self):
        #set the flag used to run the camera
        self.run_video = True
        while self.run_video:
            try:
                ret, frame = self.getImage()
            except Exception as e:
                print "Image get exception check window name.\nException:" + str(e)
                errorBox("Writing exception check window name.\nException:" + str(e))               
            if ret:            
                self.newY2 = frame.shape[0] - self.cropY2 #image height - pixels to crop
                self.newX2 = frame.shape[1] - self.cropX2 #image width - pixels to crop
                cropFrame = frame[int(self.cropY1):self.newY2, int(self.cropX1):self.newX2] #crop
                height, width = cropFrame.shape[:2]
                if 900 > height > 600:
                    cropFrame = cv2.resize(cropFrame,(0,0),fx=0.6,fy=0.6)
                elif height > 900:
                    cropFrame = cv2.resize(cropFrame,(0,0),fx=0.4,fy=0.4)
                #resize image
                newFrame = cv2.resize(cropFrame,(0,0),fx=self.capWindowResize,fy=self.capWindowResize)
                #set default image label ("UNKNOWN")
                image_label = [0]
                if self.face_recker is not None:
                    predicted_image, image_label = self.faceRec.predict(self.face_recker,newFrame)
                else:
                    predicted_image = self.faceRec.justDetect(newFrame)
                #get the dimensions of the image
                height, width, _ = predicted_image.shape
                #convert the detection cv2 image into a QImage
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
                        
        #set the pause image and transmit it
        self.emitted_signal = self.video_signal.emit(self.pause_image)
        
    def prepare_pics(self, detMethod):
        try:
            self.faceRec.faceDetector = detMethod #Set the detector
            self.faceRec.prepare_training_images(self.training_data_folder)#create all training images
        except Exception as e:
            print "Training exception check settings.\nException:" + str(e)
            errorBox("Writing exception check settings.\nException:" + str(e))
        
    def train_algorithm(self, recMethod):
        try:
            self.faceRec.faceRecognizer = recMethod #Set the recogizer
            self.face_recker = self.faceRec.train(self.training_data_folder)#train and return recognizer
        except Exception as e:
            print "Training exception check settings.\nException:" + str(e)
            errorBox("Writing exception check settings.\nException:" + str(e))
        
    def unpause_video(self):
        #this is called if the signal is disconnected
        self.video_signal.emit(self.qt_image)
        
    def getImage(self):        
        #collect a list of all windows matching the ID and their window text
        def enum_cb(hwnd, results):
            self.winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
        win32gui.EnumWindows(enum_cb, self.toplist)
        #create the list
        self.windowList = [(self.hwnd, title) for self.hwnd, title in self.winlist if self.capWindowName in title.lower()]
        #take the hwnd for first window matching the ID
        self.hwndList = self.windowList[0]
        self.hwnd = self.hwndList[0]
        # get the values for the client area of the window (window without the titlebar)
        left, top, right, bot = win32gui.GetClientRect(self.hwnd)
        w = right - left
        h = bot - top
        
        hwndDC = win32gui.GetWindowDC(self.hwnd)
        mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        #create bitmap of the window
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        saveDC.SelectObject(saveBitMap)
    
        # Print the client area or the window 
        self.result = windll.user32.PrintWindow(self.hwnd, saveDC.GetSafeHdc(), 1)
        
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        try:            
            pilImage = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1)
        except:
            print "Image get exeption handled"
            return 0, 0
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwndDC)
        
        if self.result != 0:
            #PrintWindow Succeeded
            self.imageArray = numpy.array(pilImage)
        return self.result, self.imageArray