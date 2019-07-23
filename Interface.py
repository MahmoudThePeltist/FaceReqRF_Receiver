import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from sqlite3 import *

from Cam2PyQtClass import *
from Socket2PyQtClass import *
from ClientSettingsWidget import *

from CV2FacRecClass import *
from SQLiteDBClass import *


class mainWindow(QMainWindow):
    def __init__(self):
        #call super user constructor
        super(mainWindow,self).__init__()  
        #set window title
        self.setWindowTitle("FaceReqRF - Main Menu")
        #call the function to create the window
        self.create_main_menu_layout()
        #create stacked layout
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.select_main_menu_widget)
        #select the central widget to display the layout
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)
        #variables
        self.transMeth = 0
        self.host = "127.0.0.1"
        self.port = 4096
        self.buf = 1024
        self.timeOut = 0.05
        
    def create_main_menu_layout(self):
        #image in main window:
        self.back_image = QLabel()
        self.back_image.setPixmap(QPixmap('images\FaceRecRFBackground.png'))
        self.back_image.setScaledContents(1)
        #several buttons:
        self.b1 = QPushButton("Start Reciving")
        self.b2 = QPushButton("Add New Face")
        self.b3 = QPushButton("Reception Settings")
        self.b4 = QPushButton("Help")
        self.b5 = QPushButton("Quit")
        #Connections:
        self.b1.clicked.connect(self.recognize_window)
        self.b2.clicked.connect(self.face_window)
        self.b3.clicked.connect(self.modifySettings)
        self.b4.clicked.connect(self.help_window)
        self.b5.clicked.connect(self.quit_window)
        #Create the main layout
        self.vBox = QVBoxLayout()
        #add widgets to layput
        self.vBox.addWidget(self.back_image)
        self.vBox.addWidget(self.b1)
        self.vBox.addWidget(self.b2)
        self.vBox.addWidget(self.b3)
        #create layout for horizontal buttons and add them to it        
        self.hBox = QHBoxLayout()
        self.hBox.addWidget(self.b4)
        self.hBox.addWidget(self.b5)
        #add horizontal layout to vertical layout
        self.vBox.addLayout(self.hBox)
        #create main widget and set it's layout
        self.select_main_menu_widget = QWidget()
        self.select_main_menu_widget.setLayout(self.vBox)
    
    def recognize_window(self):
        print "Showing reciving window..."
        #Create the recognize window
        self.create_recognize_window() 
        #add this to the stack
        self.stacked_layout.addWidget(self.view_recognize_menu_widget) 
        #change the visible layout in the stack
        self.stacked_layout.setCurrentWidget(self.view_recognize_menu_widget)
        
    def face_window(self):
        print "Showing face window..."
        #Create the add face layout
        self.create_face_window() 
        #add this to the stack
        self.stacked_layout.addWidget(self.view_face_menu_widget)
        #change the visible layout in the stack
        self.stacked_layout.setCurrentWidget(self.view_face_menu_widget)
        
    def help_window(self):
        print "showing help window..."
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("FaceReqRF is a facial Recognition project by:")
        self.msg.setInformativeText("Mahmoud Aburas and Soliman Shalloof")
        self.msg.setWindowTitle("Help")
        self.msg.setDetailedText("Details: This is a facial recognition program, start reciving data being transmitted by the HackRF or add a new face to the database. remember to click 'prepare' after adding images and train the algorithm with the images.")
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec_()
        
    def modifySettings(self):
        #instantiate the dialog box
        self.settings_dialog = ReceptionSettings()
        #set values
        self.settings_dialog.setValues(self.transMeth,self.host,self.port,self.buf,self.timeOut)
        print "Running dialog box."
        self.settings_dialog.exec_()
        print "Getting setting values."
        self.transMeth,self.host,self.port,self.buf,self.timeOut = self.settings_dialog.getValues()
        
    def main_window(self):
        print "showing main window..."
        self.stacked_layout.setCurrentIndex(0) #change the visible layout in the stack
        
    def quit_window(self):
        print "Quiting..."
        self.close()
        
    def start_action(self):
        print "Starting video..."
        
    def stop_action(self):
        print "Pausing Video..."
        self.video.run_video = False
        
    def prepare_action(self):
        print "Preparing images for training..."
        self.video.prepare_pics()
        
    def train_action(self):
        print "Training using prepared images..."
        self.video.train_algorithm()
    
    def add_action(self):
        print "Adding: "
        dbms = database_manager()
        print "DBMS ready..."
        dbms.create_employee_table()
        print "Table ready..."
        #get values from the interface
        first_name = self.lef1.text()
        last_name = self.lef2.text()
        position = self.lef3.text()
        id_number = self.lef4.text()
        img_folder = self.lef5.text()
        #add all the values to the database
        print first_name + " " + last_name + " " + position + " " + id_number + " " + img_folder
        dbms.add_value('Employees','ID','First Name',id_number,first_name)
        dbms.add_value('Employees','ID','Last Name',id_number,last_name) 
        dbms.add_value('Employees','ID','Position',id_number,position) 
        dbms.add_value('Employees','ID','File Name',id_number,img_folder) 
        #commit and close the database        
        dbms.commit_close()
        print 'Data added'
        
    def rec_form_set(self, my_label):
        #function to set the lables in the reception page
        self.db = database_manager()
        #get the values from the database
        first_name = self.db.get_value('"First Name"','Employees','ID', my_label)
        last_name = self.db.get_value('"Last Name"','Employees','ID', my_label)
        position = self.db.get_value('Position','Employees','ID', my_label)
        ID = str(my_label)
        #set the labels in the menu
        self.le1.setText(first_name[0][0])
        self.le2.setText(last_name[0][0])
        self.le3.setText(position[0][0])
        self.le4.setText(ID)
        
    #create the layout for adding new faces
    def create_face_window(self):
        #Background image in main window:
        self.form_image = QLabel()
        self.form_image.setPixmap(QPixmap('images\FaceRecRFForm.png'))
        self.form_image.setScaledContents(1)
        #add labels
        self.lf1 = QLabel("First Name: ")
        self.lf2 = QLabel("Last Name: ")
        self.lf3 = QLabel("Position: ")
        self.lf4 = QLabel("ID Number: ")
        self.lf5 = QLabel("Images Folder: ")
        #add textboxes
        self.lef1 = QLineEdit()
        self.lef2 = QLineEdit()
        self.lef3 = QLineEdit()
        self.lef4 = QLineEdit()
        self.lef5 = QLineEdit()
        #font settings
        font_A = QFont('Helvetica',15)
        self.lf1.setFont(font_A)
        self.lf2.setFont(font_A)
        self.lf3.setFont(font_A)
        self.lf4.setFont(font_A)
        self.lf5.setFont(font_A)
        self.lef1.setFont(font_A)
        self.lef2.setFont(font_A)
        self.lef3.setFont(font_A)
        self.lef4.setFont(font_A)
        self.lef5.setFont(font_A)
        #add buttons
        self.add_btn = QPushButton("Add")
        self.bck_btn = QPushButton("Back")
        #Connections:
        self.add_btn.clicked.connect(self.add_action)
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
        self.form_grid.addWidget(self.lf5,4,0)
        #add line edit widgets to the grid layout
        self.form_grid.addWidget(self.lef1,0,1)
        self.form_grid.addWidget(self.lef2,1,1)
        self.form_grid.addWidget(self.lef3,2,1)
        self.form_grid.addWidget(self.lef4,3,1)
        self.form_grid.addWidget(self.lef5,4,1)
        #add buttons to layout
        self.button_grid.addWidget(self.add_btn,0,0)
        self.button_grid.addWidget(self.bck_btn,0,1)
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
        self.l3 = QLabel("Position: ")
        self.l4 = QLabel("ID Number: ")
        #add textboxes
        self.le1 = QLabel()
        self.le2 = QLabel()
        self.le3 = QLabel()
        self.le4 = QLabel()
        #font settings
        font_A = QFont('Helvetica',20)
        self.l1.setFont(font_A)
        self.l2.setFont(font_A)
        self.l3.setFont(font_A)
        self.l4.setFont(font_A)
        self.le1.setFont(font_A)
        self.le2.setFont(font_A)
        self.le3.setFont(font_A)
        self.le4.setFont(font_A)
        #video capture and display classes
        self.thread = QtCore.QThread()
        self.thread.start()
        #if we are using LAN reception use LAN classes
        if (self.transMeth == 0):
            self.video = ShowReceivedVideo()
            self.video.set_values(self.transMeth, self.host, self.port, self.buf, self.timeOut)
            self.video.moveToThread(self.thread)
            self.image_viewer = ReceivedImageViewer()
        #if we are using local webcam use webcam classes
        elif (self.transMeth == 1):
            self.video = ShowVideo()
            self.video.moveToThread(self.thread)
            self.image_viewer = ImageViewer()
        #if we are using RTL-SDR use gnu classes
        elif (self.transMeth == 2):
            print "TO BE DONE!"
        #if we are using hackRF then TO BE DONE!
        self.video.video_signal.connect(self.image_viewer.setImage)
        self.video.label_signal.connect(self.rec_form_set)
        #add values        
        #add buttons
        self.start_btn = QPushButton("<< Start >>")
        self.stop_btn = QPushButton("<< Pause >>")
        self.prep_btn = QPushButton("Prepare Training Images")
        self.train_btn = QPushButton("Train Recognizer")
        self.back_btn = QPushButton("Back")
        #Connections:
        self.start_btn.clicked.connect(self.start_action)
        self.start_btn.clicked.connect(self.video.startVideo)
        self.stop_btn.clicked.connect(self.stop_action)
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
        #add line edit widgets to the grid layout
        self.form_grid.addWidget(self.le1,0,1)
        self.form_grid.addWidget(self.le2,1,1)
        self.form_grid.addWidget(self.le3,2,1)
        self.form_grid.addWidget(self.le4,3,1)
        #add buttons to button grid
        self.first_button_grid.addWidget(self.start_btn,0,0)
        self.first_button_grid.addWidget(self.stop_btn,0,1)
        #add buttons to button grid
        self.second_button_grid.addWidget(self.prep_btn,0,0)
        self.second_button_grid.addWidget(self.train_btn,0,1)
        #add everything to the total grid layout
        self.total_grid.addWidget(self.image_viewer,0,0)
        self.total_grid.addLayout(self.form_grid,0,1)
        self.total_grid.addLayout(self.first_button_grid,1,0)
        self.total_grid.addLayout(self.second_button_grid,1,1)
        self.total_grid.addWidget(self.back_btn,2,1)
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