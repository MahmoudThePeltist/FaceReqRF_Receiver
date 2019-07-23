#pyqt import
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class errorBox(QDialog):
    """This class will display a dialog that contains help info"""  
    def __init__(self,errorText = "Error box Error"):
        self.popUp.setWindowTitle("Error")
        self.popUp.setWindowIcon(QIcon(self.localDir + "/images/FaceReqRFIcon.png"))
        #add buttons label and textbox
        self.errorLabel = QLabel(errorText)
        self.okBtn = QPushButton("Ok")
        #add connection
        self.okBtn.clicked.connect(self.popUp.close)
        #setup layouts
        self.popupLayout = QVBoxLayout()        
        self.popupLayout.addWidget(self.errorLabel)        
        self.popupLayout.addWidget(self.okBtn)        
        self.popUp.setLayout(self.popupLayout)
        self.popUp.exec_()