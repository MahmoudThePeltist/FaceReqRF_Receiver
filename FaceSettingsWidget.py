from PyQt4.QtGui import *
import os

class DetRecSettings(QDialog):
    """This class provides a settings window for detection and recognition"""
    
    def __init__(self):
        super(DetRecSettings, self).__init__()
        
        self.localDir = os.path.dirname(os.path.realpath(__file__))                        
        self.setWindowTitle("Detection/Recognition Settings")
        self.setWindowIcon(QIcon(self.localDir + "/images/FaceReqRFIcon.png"))
        #Add Radio Buttons
        self.radio_group_box_1 = QGroupBox("Select detection method:")
        self.radio_button_group_1 = QButtonGroup()
        
        self.radio_button_0 = QRadioButton("HAAR Cascade")
        self.radio_button_1 = QRadioButton("LBP Cascade")
        self.radio_button_2 = QRadioButton("Improved LBP Cascade")
        
        self.radio_button_layout_1 = QVBoxLayout()
        self.radio_button_layout_1.addWidget(self.radio_button_0)
        self.radio_button_layout_1.addWidget(self.radio_button_1)
        self.radio_button_layout_1.addWidget(self.radio_button_2)
        
        self.radio_button_group_1.addButton(self.radio_button_0)
        self.radio_button_group_1.addButton(self.radio_button_1)      
        self.radio_button_group_1.addButton(self.radio_button_2)      
        self.radio_button_group_1.setId(self.radio_button_0, 0)
        self.radio_button_group_1.setId(self.radio_button_1, 1)
        self.radio_button_group_1.setId(self.radio_button_2, 2)
        
        self.radio_group_box_1.setLayout(self.radio_button_layout_1)
                
        self.radio_group_box_2 = QGroupBox("Select recognission method:")
        self.radio_button_group_2 = QButtonGroup()
        
        self.radio_button_3 = QRadioButton("EigenFaces Method")
        self.radio_button_4 = QRadioButton("FisherFaces Method")
        self.radio_button_5 = QRadioButton("LBPH Method")
        
        self.radio_button_layout_2 = QVBoxLayout()
        self.radio_button_layout_2.addWidget(self.radio_button_3)
        self.radio_button_layout_2.addWidget(self.radio_button_4)
        self.radio_button_layout_2.addWidget(self.radio_button_5)
        
        self.radio_button_group_2.addButton(self.radio_button_3)
        self.radio_button_group_2.addButton(self.radio_button_4)      
        self.radio_button_group_2.addButton(self.radio_button_5)      
        self.radio_button_group_2.setId(self.radio_button_3, 0)
        self.radio_button_group_2.setId(self.radio_button_4, 1)
        self.radio_button_group_2.setId(self.radio_button_5, 2)
        
        self.radio_group_box_2.setLayout(self.radio_button_layout_2)
                
        self.SettingsSubmitButton = QPushButton("Submit")
        
        #create and set layouts
        self.setting_total_layout = QVBoxLayout()
        self.setting_total_layout.addWidget(self.radio_group_box_1)
        self.setting_total_layout.addWidget(self.radio_group_box_2)
        self.setting_total_layout.addWidget(self.SettingsSubmitButton)
        self.setLayout(self.setting_total_layout)

        self.SettingsSubmitButton.clicked.connect(self.close)
    
    #function to set the textbox default values
    def setValues(self, detMethod, recMethod):
        print "Current Values are: ", detMethod, recMethod
        if detMethod == 0:
            self.radio_button_0.setChecked(True)
        elif detMethod == 1:
            self.radio_button_1.setChecked(True)
        elif detMethod == 2:
            self.radio_button_2.setChecked(True)
        if recMethod == 0:
            self.radio_button_3.setChecked(True)
        elif recMethod == 1:
            self.radio_button_4.setChecked(True)
        elif recMethod == 2:
            self.radio_button_5.setChecked(True)

    #function to return the new entered values
    def getValues(self):
        print "New values are: ", self.radio_button_group_1.checkedId(),  self.radio_button_group_2.checkedId()
        return self.radio_button_group_1.checkedId(),  self.radio_button_group_2.checkedId()