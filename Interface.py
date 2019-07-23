print("---- ### Welcome to FaceReqRF ### ----\n")
print("Importing Sys, OS and datetime libraries... ")
import sys
import os
import datetime
# these imports are for cx_freeze
print("Importing numpy... ")
import numpy.core._methods
import numpy.lib.format
# pyqt import
print("Importing PyQt5, sqlite3, Socket... ")
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from sqlite3 import *
from socket import gethostbyname, gethostname
#  Try to import moviepy
print("Trying to import MoviePy...")
try:
    from moviepy.editor import ImageSequenceClip
except Exception as e:
   print("MoviePy import error.\nException:" + str(e))
# reception and display classes
print("Importing local modules... ")
from PyQtCamClass import *
from PyQtSocketClass import *
from PyQtHTTPClass import *
from PyQtWindowClass import *
from PyQtImageViewer import *
# settings widgets
from SettingsClientWidget import *
from SettingsFaceWidget import *
from SettingsExportWidget import *
# sql classes
from SQLiteDisplayTableClass import *
from SQLiteDBClass import *
from ManuallyAddFace import *
# facial recognition class
from CV2FacRecClass import *
# help and error dialogs
from DialogHelp import *
from DialogError import *

class mainWindow(QMainWindow):
    def __init__(self):
        # call super user constructor
        super(mainWindow,self).__init__()  
        # set window title and icon
        if getattr(sys, 'frozen', False):
            #  The application is frozen
            self.localDir = os.path.dirname(sys.executable)
        else:
            # The application is not frozen
            self.localDir = os.path.dirname(os.path.realpath(__file__))    
        # set window title and icon
        self.setWindowTitle("FaceReqRF - Main Menu")
        self.setWindowIcon(QIcon(self.localDir + "/images/FaceReqRFIcon.png"))
        # call the function to create the window
        self.create_main_menu_layout()
        # stylesheet
        self.setStyleSheet("QPushButton {background-color: #7a92ba; height:30%; border: none; color:white; font-size:16px;} QPushButton:hover{background-color: #5370a0}")
        # create stacked layout
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.select_main_menu_widget)
        # select the central widget to display the layout
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)
        # Make sure recording directory exists
        if not os.path.exists(self.localDir + "/recording"):
            print("Directory: ", (self.localDir + "/recording"), " does not exist, creating...")
            os.makedirs(self.localDir + "/recording")
        # Make sure database directory exists
        if not os.path.exists(self.localDir + "/database"):
            print("Directory: ", (self.localDir + "/database"), " does not exist, creating...")
            os.makedirs(self.localDir + "/database")
        # Make sure exported directory exists
        if not os.path.exists(self.localDir + "/exported"):
            print("Directory: ", (self.localDir + "/exported"), " does not exist, creating...")
            os.makedirs(self.localDir + "/exported")
        # Make sure frames directory exists
        if not os.path.exists(self.localDir + "/frames"):
            print("Directory: ", (self.localDir + "/frames"), " does not exist, creating...")
            os.makedirs(self.localDir + "/frames")
        # reception variables
        self.transMeth = 1
        self.host = gethostbyname(gethostname())
        self.port = 4096
        self.buf = 1024
        self.windowTitle = '9868'
        self.windowResize = 1
        self.cropX1 = 350
        self.cropY1 = 120
        self.cropX2 = 350
        self.cropY2 = 0
        # button flags
        self.recording = False
        self.receiving = False
        self.firstRun = True
        # Detection and Recognition flags
        self.detMethod = 2
        self.recMethod = 2
        self.useXML = 1
        # recording variables
        self.recordSkip = 0
        self.writeFPS = 10
        self.writeMethod = 0
        self.writeName = 'recording'
        self.writeCodec = "libx264" # libx264 or mpeg4 or rawvideo or png or libvorbis or libvpx
        self.writeProgram = "imageio" # imageio or ImageMagick or ffmpeg
        self.httpAddress = 'http://192.168.23.2:4747/mjpegfeed'# IP Cam variable
        self.camPort = 0 # local webcam port
        
    def create_main_menu_layout(self):
        # image in main window:
        self.back_image = QLabel()
        self.back_image.setPixmap(QPixmap(self.localDir + '\images\FaceRecRFBackground.png'))
        self.back_image.setScaledContents(1)
        # several buttons:
        self.b1 = QPushButton("Start Receiving")
        self.b2 = QPushButton("Add New Face")
        self.b3 = QPushButton("Reception Settings")
        self.b4 = QPushButton("Det/Rec Settings")
        self.b5 = QPushButton("Recording Settings")
        self.b6 = QPushButton("Help")
        self.b7 = QPushButton("Quit")
        # Connections:
        self.b1.clicked.connect(self.recognize_window)
        self.b2.clicked.connect(self.face_window)
        self.b3.clicked.connect(self.modifyReceptionSettings)
        self.b4.clicked.connect(self.modifyDetRecSettings)
        self.b5.clicked.connect(self.modifyRecordingSettings)
        self.b6.clicked.connect(self.help_window)
        self.b7.clicked.connect(self.quit_window)
        # Create the main layout
        self.vBox = QVBoxLayout()
        # add widgets to layput
        self.vBox.addWidget(self.back_image)
        self.vBox.addWidget(self.b1)
        self.vBox.addWidget(self.b2)
        # create layout for horizontal buttons and add them to it
        self.hBox1 = QHBoxLayout()     
        self.hBox2 = QHBoxLayout()
        self.hBox1.addWidget(self.b3)
        self.hBox1.addWidget(self.b4)
        self.hBox1.addWidget(self.b5)  
        self.hBox2.addWidget(self.b6)
        self.hBox2.addWidget(self.b7)
        # add horizontal layout to vertical layout
        self.vBox.addLayout(self.hBox1)
        self.vBox.addLayout(self.hBox2)
        # create main widget and set it's layout
        self.select_main_menu_widget = QWidget()
        self.select_main_menu_widget.setLayout(self.vBox)
    
    def recognize_window(self):
        print("Showing reciving window...")
        # Create the recognize window
        self.create_recognize_window() 
        # add this to the stack
        self.stacked_layout.addWidget(self.view_recognize_menu_widget) 
        # change the visible layout in the stack
        self.stacked_layout.setCurrentWidget(self.view_recognize_menu_widget)
        
    def face_window(self):
        print("Showing face window...")
        self.create_face_window() # Create the add face layout
        self.stacked_layout.addWidget(self.view_face_menu_widget)# add this to the stack
        # change the visible layout in the stack
        self.stacked_layout.setCurrentWidget(self.view_face_menu_widget)
        
    def help_window(self):
        print("showing help window...")
        self.msg = helpMenu()
        self.msg.exec_()
        
    def modifyReceptionSettings(self):
        self.reception_dialog = ReceptionSettings()# instantiate the dialog box
        # set values
        self.reception_dialog.setValues(self.transMeth,self.host,self.port,self.buf,self.windowTitle, self.windowResize,self.cropX1,self.cropY1,self.cropX2,self.cropY2, self.httpAddress, self.camPort)
        print("Running dialog box.")
        self.reception_dialog.exec_()
        print("Getting setting values.")
        self.transMeth,self.host,self.port,self.buf,self.windowTitle, self.windowResize,self.cropX1,self.cropY1,self.cropX2,self.cropY2, self.httpAddress, self.camPort  = self.reception_dialog.getValues()
        
    def modifyDetRecSettings(self):
        self.reception_dialog = DetRecSettings()# instantiate the dialog box
        # set values
        self.reception_dialog.setValues(self.detMethod,self.recMethod, self.useXML)
        print("Running dialog box.")
        self.reception_dialog.exec_()
        print("Getting setting values.")
        self.detMethod, self.recMethod, self.useXML = self.reception_dialog.getValues()
        
    def modifyRecordingSettings(self):
        self.recording_dialog = RecordingSettings()# instantiate the dialog box
        # set values
        self.recording_dialog.setValues(self.writeMethod,self.recordSkip,self.writeName,self.writeFPS)
        print("Running dialog box.")
        self.recording_dialog.exec_()
        print("Getting setting values.")
        self.writeMethod,self.recordSkip,self.writeName,self.writeFPS,self.writeCodec,self.writeProgram = self.recording_dialog.getValues()
        
    def main_window(self):
        print("showing main window...")
        self.stacked_layout.setCurrentIndex(0) # change the visible layout in the stack
        
    def quit_window(self):
        print("Quiting...")
        self.close()
        
    def receive_action(self):
        # if we are receiving pause and if we are paused start receiving
        if self.receiving == False:
            # set the recognizer variables
            self.video.recMethod = self.recMethod 
            self.video.detMethod = self.detMethod 
            self.video.useXML = self.useXML
            # call self.video.startVideo() func with this click() see func where btn is defined for more info
            self.invisible_start_btn.click()
            self.receiving = True # set local flag
            print("Starting reception...")
            self.receive_btn.setText(">> Pause Reception <<") # change the text written on the btn
        elif self.receiving == True:
            print("Pausing reception...")
            self.video.run_video = False # set the startVideo function flag off, so we pause rec
            self.receiving = False # set local flag
            self.receive_btn.setText("<< Start Reception >>")  # change the text written on the btn
            
    def record_action(self):       
        # we need to setup a folder to hold the recorded frames
        now = datetime.datetime.now()# get current date info
        folder_name = now.strftime("%Y%m%d") + "_" + str(self.transMeth)# folder name 'year+month+day_transmissionMethod'
        #if folder does not exist create it
        if not os.path.exists(self.localDir + "/recording/" + folder_name):
            print("Directory: ", (self.localDir + "/recording/" + folder_name), " does not exist, creating...")
            os.makedirs(self.localDir + "/recording/" + folder_name)
        #Start or stop recording the frames being displayed
        if self.recording == False:
            print("Recording all images!")
            self.video.recordingFolder = self.localDir + "/recording/" + folder_name + "/"
            self.video.skip_value = self.recordSkip
            self.video.record = True #Start recording all images by setting the record flag = true
            self.record_btn.setText(">> Stop Recording <<")
            self.recording = True #set local flag
        elif self.recording == True:
            print("Stopping recording of images!")
            self.video.record = False #Stop recording images by setting the record flag = false
            self.record_btn.setText("<< Start Recording >>")
            self.recording = False
        
    def export_action(self):
        #get the folder containing the images using a file dialog
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        folderLocs = QStringList() #create a QstringList to hold the location data
        if dlg.exec_():
            folderLocs = dlg.selectedFiles()
            for folderLoc in folderLocs:
                #Export the recorder images as video using ffmpeg
                print("Grabbing images from: ", str(folderLoc))
                folderName = str(folderLoc)[-8:]#get the folder name (the last 8 characters) from the directory name
                try:
                    clip = ImageSequenceClip(str(folderLoc), fps = int(self.writeFPS))
                    print("Writing file...")
                    if self.writeMethod == 0:
                        clip.write_videofile(self.localDir + "/exported/" + folderName + "_" + str(self.writeName) + ".avi",codec = str(self.writeCodec))
                    elif self.writeMethod == 1:            
                        clip.write_gif(self.localDir + "/exported/" + folderName + "_" + str(self.writeName) + ".gif", program = str(self.writeProgram))
                except Exception as e:
                    print("Writing exception check settings.\nException:" + str(e))
                    errorBox("Writing exception check settings.\nException:" + str(e))
        
    def prepare_action(self):
        if self.receiving == True:
            print("Pausing reception...")
            self.video.run_video = False #set the startVideo function flag off, so we pause rec
            self.receiving = False #set local flag
            self.receive_btn.setText("<< Start Reception >>")  #change the text written on the btn
        try:
            print("Preparing images for training...")
            self.video.prepare_pics(self.detMethod)
        except Exception as e:
            print("Preperation error.\nException:" + str(e))
            errorBox("Preperation error.\nException:" + str(e))
            
    def train_action(self):
        if self.receiving == True:
            print("Pausing reception...")
            self.video.run_video = False #set the startVideo function flag off, so we pause rec
            self.receiving = False #set local flag
            self.receive_btn.setText("<< Start Reception >>")  #change the text written on the btn
        try:
            print("Training using prepared images...")
            self.video.train_algorithm(self.recMethod)
        except Exception as e:
            print("Training error.\nException:" + str(e))
            errorBox("Training error.\nException:" + str(e))
            
    def add_action(self):
        print("Adding: ")
        dbms = database_manager()
        print("DBMS ready...")
        dbms.create_employee_table()
        print("Table ready...")
        #get values from the interface
        first_name = self.lef1.text()
        last_name = self.lef2.text()
        position = self.lef3.text()
        id_number = self.lef4.text()
        #add all the values to the database
        print("trying to add: " + first_name + " " + last_name + " " + position + " " + id_number)
        #check if the image folder exists, if it does not create dialog box
        folderName = "j" + str(id_number)
        if os.path.exists(self.localDir + "/training-data/" + folderName):  
            print("folder " + folderName + " found!")
        else:
            faceFolderAdd = faceChoice()
            faceFolderAdd.camPort = self.camPort
            faceFolderAdd.setFolderName(folderName)
            faceFolderAdd.exec_()
        #add the gotten values
        dbms.add_value('Employees','ID','First Name',id_number,first_name)
        dbms.add_value('Employees','ID','Last Name',id_number,last_name) 
        dbms.add_value('Employees','ID','Position',id_number,position)     
        dbms.add_value('Employees','ID','File Name',id_number,folderName) 
        dbms.commit_close()#commit and close the database   
        print('Data added')    
        self.lef1.setText("")
        self.lef2.setText("")
        self.lef3.setText("")
        self.lef4.setText("")
    
    def display_table(self):
        self.database_dialog = DisplayClass()#instantiate the dialog box
        print("Running dialog box.")
        self.database_dialog.exec_()                
        
    def rec_form_set(self, my_label):
        #function to set the lables in the reception page
        self.db = database_manager()
        #get the values from the database
        first_name = self.db.get_value('"First Name"','Employees','ID', my_label[0])
        last_name = self.db.get_value('"Last Name"','Employees','ID', my_label[0])
        position = self.db.get_value('Position','Employees','ID', my_label[0])
        #set the labels in the menu
        try:
            self.le1.setText(first_name[0][0])
            self.le2.setText(last_name[0][0])
            self.le3.setText(position[0][0])
            self.le4.setText(str(my_label[0]))
            self.le5.setText(str(int(my_label[1])))
        except:
            self.le1.setText("Value not in DB")
            self.le2.setText("Value not in DB")
            self.le3.setText("Value not in DB")
            self.le4.setText(str(my_label[0]))
            self.le5.setText(str(int(my_label[1])))
            
        
    #create the layout for adding new faces
    def create_face_window(self):
        #Background image in main window:
        self.form_image = QLabel()
        self.form_image.setPixmap(QPixmap('images\FaceRecRFForm.png'))
        self.form_image.setScaledContents(1)
        #add labels
        self.lf1 = QLabel("First Name: ")
        self.lf2 = QLabel("Last Name: ")
        self.lf3 = QLabel("Wanted For: ")
        self.lf4 = QLabel("ID Number: ")
        #add textboxes
        self.lef1 = QLineEdit()
        self.lef2 = QLineEdit()
        self.lef3 = QLineEdit()
        self.lef4 = QLineEdit()
        #font settings
        font_A = QFont('Helvetica',15)
        self.lf1.setFont(font_A)
        self.lf2.setFont(font_A)
        self.lf3.setFont(font_A)
        self.lf4.setFont(font_A)
        self.lef1.setFont(font_A)
        self.lef2.setFont(font_A)
        self.lef3.setFont(font_A)
        self.lef4.setFont(font_A)
        #add buttons
        self.add_btn = QPushButton("Add")
        self.table_btn = QPushButton("Display Table")
        self.bck_btn = QPushButton("Back")
        #Connections:
        self.add_btn.clicked.connect(self.add_action)
        self.table_btn.clicked.connect(self.display_table)
        self.bck_btn.clicked.connect(self.main_window)
        #create layouts
        self.form_grid = QGridLayout()
        self.button_grid = QGridLayout()
        self.total_layout = QVBoxLayout()
        #add lable widgets to the grid layout
        self.form_grid.addWidget(self.lf1,0,0)
        self.form_grid.addWidget(self.lf2,1,0)
        self.form_grid.addWidget(self.lf3,2,0)
        self.form_grid.addWidget(self.lf4,3,0)
        #add line edit widgets to the grid layout
        self.form_grid.addWidget(self.lef1,0,1)
        self.form_grid.addWidget(self.lef2,1,1)
        self.form_grid.addWidget(self.lef3,2,1)
        self.form_grid.addWidget(self.lef4,3,1)
        #add buttons to layout
        self.button_grid.addWidget(self.add_btn,0,0)
        self.button_grid.addWidget(self.table_btn,0,1)
        self.button_grid.addWidget(self.bck_btn,0,2)
        #add everything to the total grid layout
        self.total_layout.addWidget(self.form_image)
        self.total_layout.addLayout(self.form_grid)
        self.total_layout.addLayout(self.button_grid)
        #create widget to display this layout
        self.view_face_menu_widget = QWidget()
        self.view_face_menu_widget.setLayout(self.total_layout)
        
    def create_recognize_window(self):
        #add labels
        self.l1 = QLabel("First Name: ")
        self.l2 = QLabel("Last Name: ")
        self.l3 = QLabel("Wanted For: ")
        self.l4 = QLabel("ID Number: ")
        self.l5 = QLabel("Confidence: ")
        #add textboxes
        self.le1 = QLabel()
        self.le2 = QLabel()
        self.le3 = QLabel()
        self.le4 = QLabel()
        self.le5 = QLabel()
        #font settings
        font_A = QFont('Helvetica',20)
        self.l1.setFont(font_A)
        self.l2.setFont(font_A)
        self.l3.setFont(font_A)
        self.l4.setFont(font_A)
        self.l5.setFont(font_A)
        self.le1.setFont(font_A)
        self.le2.setFont(font_A)
        self.le3.setFont(font_A)
        self.le4.setFont(font_A)
        self.le5.setFont(font_A)
        #video capture and display classes
        self.thread = QtCore.QThread()
        self.thread.start()
        #if we are using LAN reception use LAN classes
        if (self.transMeth == 0):
            try:
                self.video = ShowReceivedVideo()
                self.video.set_values(self.transMeth, self.host, self.port, self.buf, self.useXML)
                self.video.moveToThread(self.thread)
                self.image_viewer = ImageViewer()
            except Exception as e:
                print("Reception initialization error, check settings.\nException:" + str(e))
                errorBox("Writing exception check settings.\nException:" + str(e))
        #if we are using local webcam use webcam classes
        elif (self.transMeth == 1):
            self.video = ShowVideo()
            #set the webcam port
            if self.video.webcamPort != self.camPort:
                self.video.webcamPort = self.camPort
                self.video.camera = cv2.VideoCapture(self.camPort)
            self.video.moveToThread(self.thread)
            self.image_viewer = ImageViewer()
        #if we are using RTL-SDR use gnu classes
        elif (self.transMeth == 2):
            try:
                self.video = windowCapture()
                self.video.cropX1 = self.cropX1
                self.video.cropY1 = self.cropY1
                self.video.cropX2 = self.cropX2
                self.video.cropY2 = self.cropY2
                self.video.capWindowName = str(self.windowTitle)
                self.video.capWindowResize = float(self.windowResize)
                self.video.moveToThread(self.thread)
                self.image_viewer = ImageViewer()
            except Exception as e:
                print("Reception initialization error, check settings.\nException:" + str(e))
                errorBox("Writing exception check settings.\nException:" + str(e))
        #if we are using an IP camera
        elif (self.transMeth == 3):
            try:
                self.video = ShowIPVideo()
                self.video.httpAddress = self.httpAddress
                self.video.moveToThread(self.thread)
                self.image_viewer = ImageViewer()                
            except Exception as e:
                print("Reception initialization error, check settings.\nException:" + str(e))
                errorBox("Writing exception check settings.\nException:" + str(e))
        #connect to the streams
        self.video.video_signal.connect(self.image_viewer.setImage)
        self.video.label_signal.connect(self.rec_form_set)
        #add buttons
        self.receive_btn = QPushButton("<< Start Reception >>")
        self.record_btn = QPushButton("<< Start Recording >>")
        self.export_btn = QPushButton("|| Export Recording ||")
        self.prep_btn = QPushButton("Prepare Training Images")
        self.train_btn = QPushButton("Train Recognizer")
        self.back_btn = QPushButton("Back")
        #next is a button designed to do nothing but start receiving, this is to "fix" the crash
        #that happens when self.video.startVideo() is called anywhere ouside of a button click
        self.invisible_start_btn = QPushButton("you should not be seeing this")
        self.invisible_start_btn.clicked.connect(self.video.startVideo)
        #Connections:
        self.receive_btn.clicked.connect(self.receive_action)
        self.record_btn.clicked.connect(self.record_action)
        self.export_btn.clicked.connect(self.export_action)
        self.prep_btn.clicked.connect(self.prepare_action)
        self.train_btn.clicked.connect(self.train_action)
        self.back_btn.clicked.connect(self.main_window)
        #create layouts
        self.form_grid = QGridLayout()
        self.first_button_grid = QGridLayout()
        self.second_button_grid = QGridLayout()
        self.total_grid = QGridLayout()
        #add lable widgets to the grid layout
        self.form_grid.addWidget(self.l1,0,0)
        self.form_grid.addWidget(self.l2,1,0)
        self.form_grid.addWidget(self.l3,2,0)
        self.form_grid.addWidget(self.l4,3,0)
        self.form_grid.addWidget(self.l5,4,0)
        #add line edit widgets to the grid layout
        self.form_grid.addWidget(self.le1,0,1)
        self.form_grid.addWidget(self.le2,1,1)
        self.form_grid.addWidget(self.le3,2,1)
        self.form_grid.addWidget(self.le4,3,1)
        self.form_grid.addWidget(self.le5,4,1)
        #add buttons to button grid
        self.first_button_grid.addWidget(self.receive_btn,0,0)
        self.first_button_grid.addWidget(self.record_btn,1,0)
        self.first_button_grid.addWidget(self.export_btn,2,0)
        #add buttons to button grid
        self.second_button_grid.addWidget(self.prep_btn,0,0)
        self.second_button_grid.addWidget(self.train_btn,1,0)
        self.second_button_grid.addWidget(self.back_btn,2,0)
        #add everything to the total grid layout
        self.total_grid.addWidget(self.image_viewer,0,0)
        self.total_grid.addLayout(self.form_grid,0,1)
        self.total_grid.addLayout(self.first_button_grid,1,0)
        self.total_grid.addLayout(self.second_button_grid,1,1)
        #create widget to display this layout
        self.view_recognize_menu_widget = QWidget()
        self.view_recognize_menu_widget.setLayout(self.total_grid)
        self.video.run_video = False

def main():
    application = QApplication(sys.argv) #create new application
    main_window = mainWindow() #Create new instance of main window
    main_window.setGeometry(25,50,1200,600)
    main_window.show() #make instance visible
    main_window.raise_() #raise window to the top of window stack
    application.exec_() #monitor application for events
    sys.exit(application.exec_())
    
if __name__ == "__main__":
    main()