from PyQt4.QtGui import *
import os
import sys

class DetRecSettings(QDialog):
    """This class provides a settings window for detection and recognition"""
    
    def __init__(self):
        super(DetRecSettings, self).__init__()
        #get local directory
        if getattr(sys, 'frozen', False):
            # The application is frozen
            self.localDir = os.path.dirname(sys.executable)
        else:
            # The application is not frozen
            self.localDir = os.path.dirname(os.path.realpath(__file__))    
        #set the window title and icon                     
        self.setWindowTitle("Detection/Recognition Settings")
        self.setWindowIcon(QIcon(self.localDir + "/images/FaceReqRFIcon.png"))
        #add first groupbox and radio button group
        self.radio_group_box_1 = QGroupBox("Select detection method:")
        self.radio_button_group_1 = QButtonGroup()
        
        self.radio_button_0 = QRadioButton("HAAR Cascade")
        self.radio_button_1 = QRadioButton("LBP Cascade")
        self.radio_button_2 = QRadioButton("Caffe - Deep Learning")
        
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
        #add second groupbox and radio button group       
        self.radio_group_box_2 = QGroupBox("Select recognition method:")
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
        #add final groupbox and checkbox
        self.checkbox_group_box = QGroupBox("Other:")
        self.checkBox_label = QLabel("Use pretrained recognizer XML: ")
        self.checkBox = QCheckBox()
        self.checkbox_layout = QHBoxLayout()
        self.checkbox_layout.addWidget(self.checkBox_label)
        self.checkbox_layout.addWidget(self.checkBox)
        self.checkbox_group_box.setLayout(self.checkbox_layout)
                
        self.SettingsSubmitButton = QPushButton("Submit")
        
        #create and set layouts
        self.setting_total_layout = QVBoxLayout()
        self.setting_total_layout.addWidget(self.radio_group_box_1)
        self.setting_total_layout.addWidget(self.radio_group_box_2)
        self.setting_total_layout.addWidget(self.checkbox_group_box)
        self.setting_total_layout.addWidget(self.SettingsSubmitButton)
        self.setLayout(self.setting_total_layout)

        self.SettingsSubmitButton.clicked.connect(self.close)
    
    #function to set the textbox default values
    def setValues(self, detMethod, recMethod, useXML):
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
        if useXML == 0:
            self.checkBox.setChecked(0)
        elif useXML == 1:
            self.checkBox.setChecked(1)

    #function to return the new entered values
    def getValues(self):
        print "Detector: ", self.radio_button_group_1.checkedId(),"\nRecognizor: ",  self.radio_button_group_2.checkedId(),"\nUse pretrained recognizer XML: ", int(self.checkBox.isChecked())
        return self.radio_button_group_1.checkedId(),  self.radio_button_group_2.checkedId(), int(self.checkBox.isChecked())