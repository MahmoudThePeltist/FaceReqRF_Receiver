from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import sys

class RecordingSettings(QDialog):
    """This class provides a settings window for recording and exporting"""
    
    def __init__(self):
        super(RecordingSettings, self).__init__()
        #get local directory
        if getattr(sys, 'frozen', False):
            # The application is frozen
            self.localDir = os.path.dirname(sys.executable)
        else:
            # The application is not frozen
            self.localDir = os.path.dirname(os.path.realpath(__file__))    
        #set the window title and icon
        self.setWindowTitle("Export Settings")
        self.setWindowIcon(QIcon(self.localDir + "/images/FaceReqRFIcon.png"))
        #Add Radio Buttons
        self.radio_group_box = QGroupBox("Select export method:")
        self.radio_button_group = QButtonGroup()
        
        self.radio_button_0 = QRadioButton("Video")
        self.radio_button_1 = QRadioButton("GIF")
        
        self.radio_button_layout = QVBoxLayout()
        self.radio_button_layout.addWidget(self.radio_button_0)
        self.radio_button_layout.addWidget(self.radio_button_1)
        
        self.radio_button_group.addButton(self.radio_button_0)
        self.radio_button_group.addButton(self.radio_button_1)      
        self.radio_button_group.setId(self.radio_button_0, 0)
        self.radio_button_group.setId(self.radio_button_1, 1)
        
        self.radio_group_box.setLayout(self.radio_button_layout)
                
        #Add Texboxes and their labels
        self.label1 = QLabel("Skip frames: ")
        self.label2 = QLabel("File name: ")
        self.label3 = QLabel("Frames per second: ")
        self.label4 = QLabel("Video Codec: ")
        self.label5 = QLabel("GIF program: ")
        self.textBox1 = QLineEdit()
        self.textBox2 = QLineEdit()
        self.textBox3 = QLineEdit()
        #add combo boxes
        self.comboBox1 = QComboBox()
        self.comboBox2 = QComboBox()
        self.comboBox1.addItem("libx264")
        self.comboBox1.addItem("mpeg4")
        self.comboBox1.addItem("rawvideo")
        self.comboBox1.addItem("png")
        self.comboBox1.addItem("libvorbis")
        self.comboBox1.addItem("libvpx")
        self.comboBox2.addItem("imageio")
        self.comboBox2.addItem("ImageMagick")
        self.comboBox2.addItem("ffmpeg")
        self.comboBox1.activated[str].connect(self.setCodec)
        self.comboBox2.activated[str].connect(self.setProgram)
        self.useCodec = 'libx264'
        self.useProgram = 'imageio'       
        self.SettingsSubmitButton = QPushButton("Submit")
        
        #create layouts
        self.setting_form_grid = QGridLayout()
        self.setting_total_layout = QVBoxLayout()
        #add lable widgets to the grid layout
        self.setting_form_grid.addWidget(self.label1,0,0)
        self.setting_form_grid.addWidget(self.label2,1,0)
        self.setting_form_grid.addWidget(self.label3,2,0)
        self.setting_form_grid.addWidget(self.label4,3,0)
        self.setting_form_grid.addWidget(self.label5,4,0)
        #add line edit widgets to the grid layout
        self.setting_form_grid.addWidget(self.textBox1,0,1)
        self.setting_form_grid.addWidget(self.textBox2,1,1)
        self.setting_form_grid.addWidget(self.textBox3,2,1)
        self.setting_form_grid.addWidget(self.comboBox1,3,1)
        self.setting_form_grid.addWidget(self.comboBox2,4,1)
        
        self.setting_total_layout.addWidget(self.radio_group_box)
        self.setting_total_layout.addLayout(self.setting_form_grid)
        self.setting_total_layout.addWidget(self.SettingsSubmitButton)
        
        self.setLayout(self.setting_total_layout)

        self.SettingsSubmitButton.clicked.connect(self.close)
    
    #functions to set the codec and program's values using the dropdown's string value
    def setCodec(self, text):
        self.useCodec = text
        
    def setProgram(self, text):
        self.useProgram = text
    
    #function to set the textbox default values
    def setValues(self, exportMethod, gottenSkip, gottenName, gottenFPS):
        print("Current Values are: ", exportMethod, gottenSkip, gottenName, gottenFPS)
        if exportMethod == 0:
            self.radio_button_0.setChecked(True)
        elif exportMethod == 1:
            self.radio_button_1.setChecked(True)
        self.textBox1.setText(str(gottenSkip))
        self.textBox2.setText(str(gottenName))
        self.textBox3.setText(str(gottenFPS))
        
    #function to return the new entered values
    def getValues(self):
        print("New values are: ", self.radio_button_group.checkedId() , int(self.textBox1.text()), self.textBox2.text(), int (self.textBox3.text()), self.useCodec,self.useProgram)
        return self.radio_button_group.checkedId() , int(self.textBox1.text()), self.textBox2.text(), int (self.textBox3.text()), self.useCodec, self.useProgram