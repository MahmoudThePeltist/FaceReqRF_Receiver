from PyQt4.QtGui import *
import os
import sys

class ReceptionSettings(QDialog):
    """This class provides a settings window for the server"""
    
    def __init__(self):
        super(ReceptionSettings, self).__init__()
        #get local directory
        if getattr(sys, 'frozen', False):
            # The application is frozen
            self.localDir = os.path.dirname(sys.executable)
        else:
            # The application is not frozen
            self.localDir = os.path.dirname(os.path.realpath(__file__))    
        #set the window title and icon
        self.setWindowTitle("Reception Settings")
        self.setWindowIcon(QIcon(self.localDir + "/images/FaceReqRFIcon.png"))
        #create Radio Button group and radio buttons
        self.radio_button_group = QButtonGroup()
        self.radio_button_0 = QRadioButton("Local Area Network")
        self.radio_button_1 = QRadioButton("Local Webcam")
        self.radio_button_2 = QRadioButton("RTL-SDR Receiver")
        self.radio_button_3 = QRadioButton("IP Camera / HTTP MJPEG feed")
        #connect each radio button to a fuction
        self.radio_button_0.clicked.connect(self.clicked_LAN)
        self.radio_button_1.clicked.connect(self.clicked_LW)
        self.radio_button_2.clicked.connect(self.clicked_RTL)
        self.radio_button_3.clicked.connect(self.clicked_HTTP)
        #create layout and add the buttons
        self.radio_button_layout = QVBoxLayout()
        self.radio_button_layout.addWidget(self.radio_button_0)
        self.radio_button_layout.addWidget(self.radio_button_1)
        self.radio_button_layout.addWidget(self.radio_button_2)
        self.radio_button_layout.addWidget(self.radio_button_3)
        #add buttons to button group
        self.radio_button_group.addButton(self.radio_button_0)
        self.radio_button_group.addButton(self.radio_button_1) 
        self.radio_button_group.addButton(self.radio_button_2)  
        self.radio_button_group.addButton(self.radio_button_3)   
        #set button IDs
        self.radio_button_group.setId(self.radio_button_0, 0)
        self.radio_button_group.setId(self.radio_button_1, 1)
        self.radio_button_group.setId(self.radio_button_2, 2)
        self.radio_button_group.setId(self.radio_button_3, 3)
        #create group box for radio buttons and add the layout to it
        self.radio_group_box = QGroupBox("Please select a reception method:")
        self.radio_group_box.setLayout(self.radio_button_layout)              
        #create the labels, textboxes and submit button
        self.label1 = QLabel("Adress: ")
        self.label2 = QLabel("Port: ")
        self.label3 = QLabel("Buffer: ")
        self.label4 = QLabel("Receiver Title: ")
        self.label5 = QLabel("Image Resize: ")
        self.label6 = QLabel("Image Crop: ")
        self.label7 = QLabel("HTTP feed address: ")
        self.label8 = QLabel("Camera Port: ")
        self.textBox1 = QLineEdit()
        self.textBox2 = QLineEdit()
        self.textBox3 = QLineEdit()
        self.textBox4 = QLineEdit()
        self.textBox5 = QLineEdit()
        self.textBox6a = QLineEdit()
        self.textBox6b = QLineEdit()
        self.textBox6c = QLineEdit()
        self.textBox6d = QLineEdit()
        self.textBox7 = QLineEdit()
        self.textBox8 = QLineEdit()
        self.SettingsSubmitButton = QPushButton("Submit")
        #create layouts
        self.LAN_setting_form_grid = QGridLayout()
        self.LWC_setting_form_grid = QGridLayout()
        self.RTL_setting_form_grid = QGridLayout()
        self.HTTP_setting_form_grid = QGridLayout()
        self.setting_total_layout = QVBoxLayout()
        #add textboxes of crop to their own layout
        self.crop_textboxes = QHBoxLayout()
        self.crop_textboxes.addWidget(self.textBox6a)
        self.crop_textboxes.addWidget(self.textBox6b)
        self.crop_textboxes.addWidget(self.textBox6c)
        self.crop_textboxes.addWidget(self.textBox6d)
        #add lable widgets to the grid layout
        self.LAN_setting_form_grid.addWidget(self.label1,0,0)
        self.LAN_setting_form_grid.addWidget(self.label2,1,0)
        self.LAN_setting_form_grid.addWidget(self.label3,2,0)
        self.LWC_setting_form_grid.addWidget(self.label8,0,0)
        self.RTL_setting_form_grid.addWidget(self.label4,0,0)
        self.RTL_setting_form_grid.addWidget(self.label5,1,0)
        self.RTL_setting_form_grid.addWidget(self.label6,2,0)
        self.HTTP_setting_form_grid.addWidget(self.label7,0,0)
        #add line edit widgets to the grid layout
        self.LAN_setting_form_grid.addWidget(self.textBox1,0,1)
        self.LAN_setting_form_grid.addWidget(self.textBox2,1,1)
        self.LAN_setting_form_grid.addWidget(self.textBox3,2,1)
        self.LWC_setting_form_grid.addWidget(self.textBox8,0,1)
        self.RTL_setting_form_grid.addWidget(self.textBox4,0,1)
        self.RTL_setting_form_grid.addWidget(self.textBox5,1,1)
        self.RTL_setting_form_grid.addLayout(self.crop_textboxes,2,1)
        self.HTTP_setting_form_grid.addWidget(self.textBox7,0,1)
        #Create group boxes             
        self.LAN_group_box = QGroupBox("LAN Settings:") 
        self.LWC_group_box = QGroupBox("Local WebCam Settings:") 
        self.RTL_group_box = QGroupBox("RTL Settings:") 
        self.HTTP_group_box = QGroupBox("IP Cam Settings:") 
        #set the group boxes to have the layouts
        self.LAN_group_box.setLayout(self.LAN_setting_form_grid)
        self.LWC_group_box.setLayout(self.LWC_setting_form_grid)
        self.RTL_group_box.setLayout(self.RTL_setting_form_grid)
        self.HTTP_group_box.setLayout(self.HTTP_setting_form_grid)
        #add the group boxes to the total layout
        self.setting_total_layout.addWidget(self.radio_group_box)
        self.setting_total_layout.addWidget(self.LAN_group_box)
        self.setting_total_layout.addWidget(self.LWC_group_box)
        self.setting_total_layout.addWidget(self.RTL_group_box)
        self.setting_total_layout.addWidget(self.HTTP_group_box)
        self.setting_total_layout.addWidget(self.SettingsSubmitButton)
        #set the layot of the widget as the total layout
        self.setLayout(self.setting_total_layout)
        #connect the button to a function
        self.SettingsSubmitButton.clicked.connect(self.close)
        
    #function to set the textbox default values
    def setValues(self, transMethod, gottenAddress, gottenPort, gottenBuffer, gottenFrequency, gottenSampRate, gottenX1, gottenY1, gottenX2, gottenY2, gottenHTTPAdress, gottenCamPort):
        print "Current reception method: ", transMethod
        print "Current LAN settings: ", gottenAddress, gottenPort, gottenBuffer
        print "Current RTL settings: ", gottenFrequency, gottenSampRate
        print "HTTP address: ",gottenHTTPAdress, " __ Webcam port: ", gottenCamPort
        if transMethod == 0:
            self.radio_button_0.setChecked(True)
            self.RTL_group_box.setEnabled(False)    
            self.LWC_group_box.setEnabled(False)
            self.LAN_group_box.setEnabled(True)
            self.HTTP_group_box.setEnabled(False)
        elif transMethod == 1:
            self.radio_button_1.setChecked(True)
            self.RTL_group_box.setEnabled(False)
            self.LWC_group_box.setEnabled(True)
            self.LAN_group_box.setEnabled(False)
            self.HTTP_group_box.setEnabled(False)
        elif transMethod == 2:
            self.radio_button_2.setChecked(True)
            self.RTL_group_box.setEnabled(True)
            self.LWC_group_box.setEnabled(False)
            self.LAN_group_box.setEnabled(False)
            self.HTTP_group_box.setEnabled(False)
        elif transMethod == 3:
            self.radio_button_3.setChecked(True)
            self.RTL_group_box.setEnabled(False)
            self.LWC_group_box.setEnabled(False)
            self.LAN_group_box.setEnabled(False)
            self.HTTP_group_box.setEnabled(True)
        self.textBox1.setText(str(gottenAddress))
        self.textBox2.setText(str(gottenPort))
        self.textBox3.setText(str(gottenBuffer))
        self.textBox4.setText(str(gottenFrequency))
        self.textBox5.setText(str(gottenSampRate))
        self.textBox6a.setText(str(gottenX1))
        self.textBox6b.setText(str(gottenY1))
        self.textBox6c.setText(str(gottenX2))
        self.textBox6d.setText(str(gottenY2))
        self.textBox7.setText(str(gottenHTTPAdress))
        self.textBox8.setText(str(gottenCamPort))
        
    #function to return the new entered values
    def getValues(self):
        print "New reception method: ", self.radio_button_group.checkedId()
        print "New LAN settings: ", self.textBox1.text(), int(self.textBox2.text()), int (self.textBox3.text())
        print "New RTL settings: ", self.textBox4.text(), self.textBox5.text()
        print "New HTTP address: ", self.textBox7.text(), " __ New webcam port: ", self.textBox8.text()
        return self.radio_button_group.checkedId() , self.textBox1.text(), int(self.textBox2.text()), int (self.textBox3.text()), self.textBox4.text(), self.textBox5.text(), int(self.textBox6a.text()), int(self.textBox6b.text()), int(self.textBox6c.text()), int(self.textBox6d.text()), self.textBox7.text(), int(self.textBox8.text())
        
    #functions to control which settings are enabled or disabled
    def clicked_LAN(self):
        self.RTL_group_box.setEnabled(False)
        self.LWC_group_box.setEnabled(False)
        self.LAN_group_box.setEnabled(True)
        self.HTTP_group_box.setEnabled(False)
    def clicked_LW(self):
        self.RTL_group_box.setEnabled(False)
        self.LWC_group_box.setEnabled(True)
        self.LAN_group_box.setEnabled(False)
        self.HTTP_group_box.setEnabled(False)
    def clicked_RTL(self):
        self.RTL_group_box.setEnabled(True)
        self.LWC_group_box.setEnabled(False)
        self.LAN_group_box.setEnabled(False)
        self.HTTP_group_box.setEnabled(False)
    def clicked_HTTP(self):
        self.RTL_group_box.setEnabled(False)
        self.LWC_group_box.setEnabled(False)
        self.LAN_group_box.setEnabled(False)
        self.HTTP_group_box.setEnabled(True)