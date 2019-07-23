import win32gui
import win32ui
from ctypes import windll
from PIL import Image
from PyQt4 import QtCore
from PyQt4 import QtGui
import numpy 
import cv2

from CV2FacRecClass import *

class windowCapture(QtCore.QObject):
    
    def __init__(self, parent = None):
        super(windowCapture, self).__init__(parent)
        #facial recognission variables
        self.faceRec = facial_recognition()
        self.training_data_folder = 'training-data'
        self.face_recker = None
        #image recording variables
        self.record = False
        self.skip_value = 1
        self.skip_count = 0
        self.record_count = 0
        #screen capture values
        self.windowName = '440'
        self.toplist, self.winlist = [], []
        self.hwnd = 0
        
    video_signal = QtCore.pyqtSignal(QtGui.QImage, name = 'vidSig')
    label_signal = QtCore.pyqtSignal(int)
    
    @QtCore.pyqtSlot()
    def startVideo(self):
        #set the flag used to run the camera
        self.run_video = True
        while self.run_video:
            ret, frame = self.getImage()
            if ret:               
                frame = cv2.resize(frame,(0,0),fx=0.8,fy=0.8)
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
        
    def getImage(self):        
        #collect a list of all windows matching the ID and their window text
        def enum_cb(hwnd, results):
            self.winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
        win32gui.EnumWindows(enum_cb, self.toplist)
        #create the list
        self.windowList = [(self.hwnd, title) for self.hwnd, title in self.winlist if self.windowName in title.lower()]
        #take the hwnd for first window matching the ID
        self.hwndList = self.windowList[0]
        self.hwnd = self.hwndList[0]
        print self.hwnd
        # get the values for the client area.
        left, top, right, bot = win32gui.GetClientRect(self.hwnd)
        w = right - left
        h = bot - top
        
        hwndDC = win32gui.GetWindowDC(self.hwnd)
        mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        saveDC.SelectObject(saveBitMap)
    
        # Change the line below depending on whether you want the whole window
        # or just the client area. 
        self.result = windll.user32.PrintWindow(self.hwnd, saveDC.GetSafeHdc(), 1)
        #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
        print self.result
        
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        
        pilImage = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)
            
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwndDC)
        
        if self.result != 0:
            #PrintWindow Succeeded
            self.imageArray = numpy.array(pilImage)
        return self.result, self.imageArray