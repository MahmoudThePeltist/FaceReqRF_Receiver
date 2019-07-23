from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os
import sys
from shutil import copyfile
import time
from DialogError import *

#reception and display classes
from PyQtCamClass import *
from PyQtImageViewer import *

class faceChoice(QDialog):
    """This class will create a face folder and allow the user to add a face to it"""
    
    def __init__(self):
        super(faceChoice,self).__init__()
        #set local directory, title and icon        
        if getattr(sys, 'frozen', False):
            # The application is frozen
            self.localDir = os.path.dirname(sys.executable)
        else:
            # The application is not frozen
            self.localDir = os.path.dirname(os.path.realpath(__file__))                        
        self.setWindowTitle("Adding face folder")
        self.setWindowIcon(QIcon(self.localDir + "/images/FaceReqRFIcon.png"))
        #variables        
        self.folderName = "j_ERROR"
        self.camPort = 1
        self.fileCount = 0
        #create text and buttons
        self.text1 = QLabel("Warning, folder not found!")
        self.text2 = QLabel("What would you like to do after folder creation?")
        self.button1 = QPushButton("Just Create Folder")
        self.button2 = QPushButton("Capture images with webcam")
        self.button3 = QPushButton("Browse for images")
        #font settings
        font_A = QFont('Helvetica',15)
        self.text1.setFont(font_A)
        self.text2.setFont(font_A)
        self.text1.setAlignment(Qt.AlignCenter)
        self.text2.setAlignment(Qt.AlignCenter)
        #connect buttons to functions        
        self.button1.clicked.connect(self.justMake)
        self.button2.clicked.connect(self.capImages)
        self.button3.clicked.connect(self.getFiles)
        #create layouts and add widgets
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.button1)
        self.buttonLayout.addWidget(self.button2)
        self.buttonLayout.addWidget(self.button3)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.text1)
        self.mainLayout.addWidget(self.text2)
        self.mainLayout.addLayout(self.buttonLayout)
        self.setLayout(self.mainLayout)
        
    def setFolderName(self, newName):
        self.folderName = newName
        self.text1.setText("Warning, folder " + self.folderName + " not found!")
    
    def justMake(self):
        try:
            print "Directory: ", (self.localDir + "/training-data/" + self.folderName), " does not exist, creating..."
            os.makedirs(self.localDir + "/training-data/" + self.folderName)
            self.close()
        except Exception as e:
            print "File get issue.\nException: " + str(e)
            errorBox("File get issue.\nException: " + str(e))
    
    def capImages(self):
        try:
            print "Directory: ", (self.localDir + "/training-data/" + self.folderName), " does not exist, creating..."
            os.makedirs(self.localDir + "/training-data/" + self.folderName)
            capWindow = imageCapture()
            capWindow.camPort = self.camPort
            capWindow.folderName = self.folderName
            capWindow.exec_()        
            self.close()
        except Exception as e:
            print "Capture window issue.\nException: " + str(e)
            errorBox("Capture window issue.\nException: " + str(e))

    def getFiles(self):
        try:
            print "Directory: ", (self.localDir + "/training-data/" + self.folderName), " does not exist, creating..."
            os.makedirs(self.localDir + "/training-data/" + self.folderName)
            dlg = QFileDialog()#instantiate QFileDialog object
            #set the selection mode to "ExistingFiles" so we can select muliple images
            dlg.setFileMode(QFileDialog.ExistingFiles)
            #set the filter so that we can only select image files
            dlg.setFilter("Image files (*.jpg)")
            fileNames = QStringList() #create a QstringList to hold the list of files
            if dlg.exec_(): #if the dialog box is executed
                 fileNames = dlg.selectedFiles()#get the list of files from the dialog box
                 for fileLoc in fileNames:
                     print fileLoc
                     newFile = self.localDir + "/training-data/" + self.folderName + "/" + str(self.fileCount) + ".jpg"
                     copyfile(fileLoc,newFile)
                     self.fileCount +=1
        except Exception as e:
            print "File get issue.\nException: " + str(e)
            errorBox("File get issue.\nException: " + str(e))
             
        
class imageCapture(QDialog):
    """This class allows us to capture images using a webcam"""
    
    def __init__(self):
        super(imageCapture,self).__init__()
        #set local directory, title and icon        
        if getattr(sys, 'frozen', False):
            # The application is frozen
            self.localDir = os.path.dirname(sys.executable)
        else:
            # The application is not frozen
            self.localDir = os.path.dirname(os.path.realpath(__file__))                        
        self.setWindowTitle("Adding face folder")
        self.setWindowIcon(QIcon(self.localDir + "/images/FaceReqRFIcon.png"))
        self.setStyleSheet("QPushButton {background-color: #7a92ba; height:30%; border: none; color:white; font-size:16px;} QPushButton:hover{background-color: #5370a0}")
        self.setGeometry(25,50,600,600)
        self.defaultImage = self.localDir + '/images/FaceRecRFSnap.png'
        #variables        
        self.camPort = 1
        self.receiving = False
        self.folderName = "j_ERROR"
        #add buttons
        self.buttonStr = QPushButton("Start Stream")
        self.buttonInv = QPushButton("INVISIBLE")
        self.buttonCap = QPushButton("Take picture")
        self.backButton = QPushButton("Back")
        #video capture and display classes
        self.thread = QtCore.QThread()
        self.thread.start()
        self.video = ShowVideo()
        self.video.moveToThread(self.thread)
        self.imageViewer = ImageViewer()
        #set the default screen image
        self.video.video_signal.connect(self.imageViewer.setImage)
        self.imageViewer.image = QtGui.QImage(self.defaultImage,"PNG")
        #connect buttons
        self.buttonStr.clicked.connect(self.startCamera)
        self.buttonInv.clicked.connect(self.video.startVideo)
        self.buttonCap.clicked.connect(self.capture)
        self.backButton.clicked.connect(self.close)        
        #create layouts and add widgets
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.imageViewer)
        self.mainLayout.addWidget(self.buttonStr)
        self.mainLayout.addWidget(self.buttonCap)
        self.mainLayout.addWidget(self.backButton)
        self.setLayout(self.mainLayout)
    
    def capture(self):
        try:
            self.video.folderName = self.folderName
            self.video.captureImage = True
            time.sleep(0.3)
        except Exception as e:
            print "Image capture issue.\nException: " + str(e)
            errorBox("Image capture issue.\nException: " + str(e))
    
    def startCamera(self):
        #if we are receiving pause and if we are paused start receiving
        if self.receiving == False:            
            #set the webcam port
            if self.video.webcamPort != self.camPort:
                self.video.webcamPort = self.camPort
                self.video.camera = cv2.VideoCapture(self.camPort)
            #call self.video.startVideo() func with this click() see func where btn is defined for more info
            self.buttonInv.click()
            self.receiving = True #set local flag            
            print "Starting reception..."
            self.buttonStr.setText("Pause Stream") #change the text written on the btn
        elif self.receiving == True:
            print "Pausing reception..."
            self.video.run_video = False #set the startVideo function flag off, so we pause rec
            self.receiving = False #set local flag
            self.buttonStr.setText("Start Stream")  #change the text written on the btn