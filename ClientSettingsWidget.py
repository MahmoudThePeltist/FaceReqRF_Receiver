from PyQt4.QtGui import *

class ReceptionSettings(QDialog):
    """This class provides a settings window for the server"""
    
    def __init__(self):
        super(ReceptionSettings, self).__init__()
        
        #Add Radio Buttons
        self.radio_group_box = QGroupBox("Please select a reception method:") 
        self.radio_button_group = QButtonGroup()
        
        self.radio_button_0 = QRadioButton("Local Area Network")
        self.radio_button_1 = QRadioButton("Local Webcam")
        self.radio_button_2 = QRadioButton("RTL-SDR Receiver")
        
        self.radio_button_layout = QVBoxLayout()
        self.radio_button_layout.addWidget(self.radio_button_0)
        self.radio_button_layout.addWidget(self.radio_button_1)
        self.radio_button_layout.addWidget(self.radio_button_2)
        
        self.radio_button_group.addButton(self.radio_button_0)
        self.radio_button_group.addButton(self.radio_button_1) 
        self.radio_button_group.addButton(self.radio_button_2)       
        self.radio_button_group.setId(self.radio_button_0, 0)
        self.radio_button_group.setId(self.radio_button_1, 1)
        self.radio_button_group.setId(self.radio_button_2, 2)
        
        self.radio_group_box.setLayout(self.radio_button_layout)
        #Add Texboxes and their labels
        self.label1 = QLabel("Adress: ")
        self.label2 = QLabel("Port: ")
        self.label3 = QLabel("Buffer: ")
        self.label4 = QLabel("timeout: ")
        self.textBox1 = QLineEdit()
        self.textBox2 = QLineEdit()
        self.textBox3 = QLineEdit()
        self.textBox4 = QLineEdit()
        self.SettingsSubmitButton = QPushButton("Submit")
        
        #create layouts
        self.setting_form_grid = QGridLayout()
        self.setting_total_layout = QVBoxLayout()
        #add lable widgets to the grid layout
        self.setting_form_grid.addWidget(self.label1,0,0)
        self.setting_form_grid.addWidget(self.label2,1,0)
        self.setting_form_grid.addWidget(self.label3,2,0)
        self.setting_form_grid.addWidget(self.label4,3,0)
        #add line edit widgets to the grid layout
        self.setting_form_grid.addWidget(self.textBox1,0,1)
        self.setting_form_grid.addWidget(self.textBox2,1,1)
        self.setting_form_grid.addWidget(self.textBox3,2,1)
        self.setting_form_grid.addWidget(self.textBox4,3,1)
        
        self.setting_total_layout.addWidget(self.radio_group_box)
        self.setting_total_layout.addLayout(self.setting_form_grid)
        self.setting_total_layout.addWidget(self.SettingsSubmitButton)
        
        self.setLayout(self.setting_total_layout)

        self.SettingsSubmitButton.clicked.connect(self.close)
        
    #function to set the textbox default values
    def setValues(self, transMethod, gottenAddress, gottenPort, gottenBuffer, gottenTimeout):
        print "Current Values are: ", transMethod, gottenAddress, gottenPort, gottenBuffer, gottenTimeout
        if transMethod == 0:
            self.radio_button_0.setChecked(True)
        elif transMethod == 1:
            self.radio_button_1.setChecked(True)
        elif transMethod == 2:
            self.radio_button_2.setChecked(True)
        self.textBox1.setText(str(gottenAddress))
        self.textBox2.setText(str(gottenPort))
        self.textBox3.setText(str(gottenBuffer))
        self.textBox4.setText(str(gottenTimeout))
        
    #function to return the new entered values
    def getValues(self):
        print "New values are: ", self.radio_button_group.checkedId() , self.textBox1.text(), int(self.textBox2.text()), int (self.textBox3.text()), self.textBox4.text()
        return self.radio_button_group.checkedId() , self.textBox1.text(), int(self.textBox2.text()), int (self.textBox3.text()), self.textBox4.text()