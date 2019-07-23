from PyQt4.QtGui import *
import os
import sys

class helpMenu(QDialog):
    """This class will display a dialog that contains help info"""
    
    def __init__(self):
        super(helpMenu,self).__init__()
        #get local directory
        if getattr(sys, 'frozen', False):
            # The application is frozen
            self.localDir = os.path.dirname(sys.executable)
        else:
            # The application is not frozen
            self.localDir = os.path.dirname(os.path.realpath(__file__))    
        #set the window title and icon
        self.setWindowTitle("Help")
        self.setWindowIcon(QIcon(self.localDir + "/images/FaceReqRFIcon.png"))
        self.setGeometry(25,50,500,500)
        #add labels and buttons
        self.title1 = QLabel("What is this app?")
        self.title2 = QLabel("\nWhat can it do?")
        self.title3 = QLabel("\nHow do I use it?")
        self.text1 = QTextEdit()
        self.text2 = QTextEdit()
        self.text3 = QTextEdit()
        self.doneButton = QPushButton("done")
        #set the font options.
        font_A = QFont('Helvetica',15)
        font_B = QFont('Helvetica',12)
        self.title1.setFont(font_A)
        self.title2.setFont(font_A)
        self.title3.setFont(font_A)
        self.text1.setFont(font_B)
        self.text2.setFont(font_B)
        self.text3.setFont(font_B)
        #set the textboxes to be read only
        self.text1.setReadOnly(True)
        self.text2.setReadOnly(True)
        self.text3.setReadOnly(True)
        #add content to textboxes
        self.text1.setHtml("This is the receiver portion of FaceReqRF, which is a security application "\
                            "that utilizes facial recognition, created by Mahmoud Aburas and Soliman Shaloof.")
        self.text2.setHtml("It allows you to add people and their images to a database, which are then "\
                            "used for facial recognition to see if they enter the view of a camera, the "\
                            "camera can be recording and transmitting from a distance.")
        self.text3.setHtml("1 - Enter people of interest into the database using the 'Add New Face' screen, "\
                            "when you enter the data, you will be asked to add facial images, make sure the "\
                            "images you use show the face clearly. "\
                            "<br><br>2 - Make sure that either the ""'Transmitter Application' is capturing and "\
                            "transmitting image data, or that the IP Camera/Local Camera you are using is "\
                            "operational, use 'Reception Settings' to choose the correct reception method."\
                            "<br><br>3 - Choose a suitable facial detection algorithm and facial recognition alogrithm "\
                            "from 'Det/Rec Settings' then click 'Start Receiving' to enter the reception screen."\
                            "<br><br>4 - Click 'Prepare Training Images' to scan the images you used for faces that "\
                            "can be used to train for facial recognition, after this operation is complete, click "\
                            "'Train Recognizer' to train the facial recognition algorithm with the found faces."\
                            "<br><br>5 - After the recognizer has been trained, click '<< Start Reception >>' to start "\
                            "receiving and displaying the image data, while receiving, you may click "\
                            "'<< Start Recording >>' to begin saving the images being displayed."\
                            "<br><br>6 - Optionally, if you would like to export the saved images as a video o a .gif "\
                            "file, you may do that by clicking '|| Export Recording ||', this may take some "\
                            "time depending on the settings chosen in 'Recording Settings' and the amount "\
                            "of recorded data.")
        #create and setup layouts
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.title1)
        self.mainLayout.addWidget(self.text1)
        self.mainLayout.addWidget(self.title2)
        self.mainLayout.addWidget(self.text2)
        self.mainLayout.addWidget(self.title3)
        self.mainLayout.addWidget(self.text3)
        #set the layout for the dialog box
        self.setLayout(self.mainLayout)