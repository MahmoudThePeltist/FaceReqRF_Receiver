from PyQt4.QtGui import *

class ReceptionSettings(QDialog):
    """This class provides a settings window for the server"""
    
    def __init__(self):
        super(ReceptionSettings, self).__init__()
        
        self.setWindowTitle("Reception Settings")
        self.setWindowIcon(QIcon("images/FaceReqRFIcon.png"))
        #Add Radio Buttons
        self.radio_group_box = QGroupBox("Please select a reception method:")
        self.radio_button_group = QButtonGroup()
        
        self.radio_button_0 = QRadioButton("Local Area Network")
        self.radio_button_1 = QRadioButton("Local Webcam")
        self.radio_button_2 = QRadioButton("RTL-SDR Receiver")
        self.radio_button_3 = QRadioButton("IP Camera / HTTP MJPEG feed")
        
        self.radio_button_0.clicked.connect(self.clicked_LAN)
        self.radio_button_1.clicked.connect(self.clicked_LW)
        self.radio_button_2.clicked.connect(self.clicked_RTL)
        self.radio_button_3.clicked.connect(self.clicked_HTTP)
        
        self.radio_button_layout = QVBoxLayout()
        self.radio_button_layout.addWidget(self.radio_button_0)
        self.radio_button_layout.addWidget(self.radio_button_1)
        self.radio_button_layout.addWidget(self.radio_button_2)
        self.radio_button_layout.addWidget(self.radio_button_3)
        
        self.radio_button_group.addButton(self.radio_button_0)
        self.radio_button_group.addButton(self.radio_button_1) 
        self.radio_button_group.addButton(self.radio_button_2)  
        self.radio_button_group.addButton(self.radio_button_3)       
        self.radio_button_group.setId(self.radio_button_0, 0)
        self.radio_button_group.setId(self.radio_button_1, 1)
        self.radio_button_group.setId(self.radio_button_2, 2)
        self.radio_button_group.setId(self.radio_button_3, 3)
        
        self.radio_group_box.setLayout(self.radio_button_layout)
                
        #Add Texboxes and their labels                 
        self.LAN_group_box = QGroupBox("LAN Settings:") 
        self.RTL_group_box = QGroupBox("RTL Settings:") 
        self.HTTP_group_box = QGroupBox("IP Cam Settings:") 

        self.label1 = QLabel("Adress: ")
        self.label2 = QLabel("Port: ")
        self.label3 = QLabel("Buffer: ")
        self.label4 = QLabel("Frequency: ")
        self.label5 = QLabel("Sampling Rate: ")
        self.label6 = QLabel("HTTP feed adress: ")
        self.textBox1 = QLineEdit()
        self.textBox2 = QLineEdit()
        self.textBox3 = QLineEdit()
        self.textBox4 = QLineEdit()
        self.textBox5 = QLineEdit()
        self.textBox6 = QLineEdit()
        self.SettingsSubmitButton = QPushButton("Submit")
        
        #create layouts
        self.LAN_setting_form_grid = QGridLayout()
        self.RTL_setting_form_grid = QGridLayout()
        self.HTTP_setting_form_grid = QGridLayout()
        self.setting_total_layout = QVBoxLayout()
        #add lable widgets to the grid layout
        self.LAN_setting_form_grid.addWidget(self.label1,0,0)
        self.LAN_setting_form_grid.addWidget(self.label2,1,0)
        self.LAN_setting_form_grid.addWidget(self.label3,2,0)
        self.RTL_setting_form_grid.addWidget(self.label4,0,0)
        self.RTL_setting_form_grid.addWidget(self.label5,1,0)
        self.HTTP_setting_form_grid.addWidget(self.label6,0,0)
        #add line edit widgets to the grid layout
        self.LAN_setting_form_grid.addWidget(self.textBox1,0,1)
        self.LAN_setting_form_grid.addWidget(self.textBox2,1,1)
        self.LAN_setting_form_grid.addWidget(self.textBox3,2,1)
        self.RTL_setting_form_grid.addWidget(self.textBox4,0,1)
        self.RTL_setting_form_grid.addWidget(self.textBox5,1,1)
        self.HTTP_setting_form_grid.addWidget(self.textBox6,0,1)
        
        self.LAN_group_box.setLayout(self.LAN_setting_form_grid)
        self.RTL_group_box.setLayout(self.RTL_setting_form_grid)
        self.HTTP_group_box.setLayout(self.HTTP_setting_form_grid)
        
        self.setting_total_layout.addWidget(self.radio_group_box)
        self.setting_total_layout.addWidget(self.LAN_group_box)
        self.setting_total_layout.addWidget(self.RTL_group_box)
        self.setting_total_layout.addWidget(self.HTTP_group_box)
        self.setting_total_layout.addWidget(self.SettingsSubmitButton)
        
        self.setLayout(self.setting_total_layout)

        self.SettingsSubmitButton.clicked.connect(self.close)
        
    #function to set the textbox default values
    def setValues(self, transMethod, gottenAddress, gottenPort, gottenBuffer, gottenFrequency, gottenSampRate, gottenHTTPAdress):
        print "Current Values are: ", transMethod, gottenAddress, gottenPort, gottenBuffer, gottenFrequency, gottenSampRate, gottenHTTPAdress
        if transMethod == 0:
            self.radio_button_0.setChecked(True)
            self.RTL_group_box.setEnabled(False)
            self.LAN_group_box.setEnabled(True)
            self.HTTP_group_box.setEnabled(False)
        elif transMethod == 1:
            self.radio_button_1.setChecked(True)
            self.RTL_group_box.setEnabled(False)
            self.LAN_group_box.setEnabled(False)
            self.HTTP_group_box.setEnabled(False)
        elif transMethod == 2:
            self.radio_button_2.setChecked(True)
            self.RTL_group_box.setEnabled(True)
            self.LAN_group_box.setEnabled(False)
            self.HTTP_group_box.setEnabled(False)
        elif transMethod == 3:
            self.radio_button_3.setChecked(True)
            self.RTL_group_box.setEnabled(False)
            self.LAN_group_box.setEnabled(False)
            self.HTTP_group_box.setEnabled(True)
        self.textBox1.setText(str(gottenAddress))
        self.textBox2.setText(str(gottenPort))
        self.textBox3.setText(str(gottenBuffer))
        self.textBox4.setText(str(gottenFrequency))
        self.textBox5.setText(str(gottenSampRate))
        self.textBox6.setText(str(gottenHTTPAdress))
        
    #function to return the new entered values
    def getValues(self):
        print "New values are: ", self.radio_button_group.checkedId() , self.textBox1.text(), int(self.textBox2.text()), int (self.textBox3.text()), self.textBox4.text(), self.textBox5.text(), self.textBox6.text()
        return self.radio_button_group.checkedId() , self.textBox1.text(), int(self.textBox2.text()), int (self.textBox3.text()), self.textBox4.text(), self.textBox5.text(), self.textBox6.text()
        
    #functions to control which settings are enabled or disabled
    def clicked_LAN(self):
        self.RTL_group_box.setEnabled(False)
        self.LAN_group_box.setEnabled(True)
        self.HTTP_group_box.setEnabled(False)
    def clicked_LW(self):
        self.RTL_group_box.setEnabled(False)
        self.LAN_group_box.setEnabled(False)
        self.HTTP_group_box.setEnabled(False)
    def clicked_RTL(self):
        self.RTL_group_box.setEnabled(True)
        self.LAN_group_box.setEnabled(False)
        self.HTTP_group_box.setEnabled(False)
    def clicked_HTTP(self):
        self.RTL_group_box.setEnabled(False)
        self.LAN_group_box.setEnabled(False)
        self.HTTP_group_box.setEnabled(True)