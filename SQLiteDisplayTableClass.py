from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sqlite3
import os

class DisplayClass(QDialog):
    """This class displays a table of entered people"""
    
    def __init__(self):
        super(DisplayClass, self).__init__()
        #get local directory
        self.localDir = os.path.dirname(os.path.realpath(__file__))
        #set the window title, icon and geometry  
        self.setWindowTitle("Table Display")
        self.setWindowIcon(QIcon(self.localDir + "/images/FaceReqRFIcon.png"))
        self.setGeometry(25,50,535,400)
        #adding table and buttons
        self.displayTable = QTableWidget()
        self.refreshButton = QPushButton("Refresh")
        self.quitButton = QPushButton("Quit")
        #get the values from the database
        self.sqlite_file = self.localDir + '/database/my_db.sqlite'
        self.tbl_name = 'Employees';
        self.conn = sqlite3.connect(self.sqlite_file)
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM {tn}'.\
            format(tn=self.tbl_name))
        self.tableValues = self.c.fetchall()
        
        #set up the table's number of rows and columns
        self.displayTable.setRowCount(len(self.tableValues))
        self.displayTable.setColumnCount(len(self.tableValues[0]))
        self.row = 0        
        
        #populate the table with values from the database
        for rowValues in self.tableValues:
            for self.col in range(0, len(self.tableValues[0])):
                #get a value, turn it into a string, then into a table item
                item = QTableWidgetItem(str(rowValues[self.col]))
                item.setFlags(Qt.ItemIsEnabled)#make the item non editable
                self.displayTable.setItem(self.row, self.col, item) #display item in table           
            self.row += 1        
        
        #button layout setup
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.refreshButton)
        self.buttonLayout.addWidget(self.quitButton)
        #main layout setup
        self.totalLayout = QVBoxLayout()
        self.totalLayout.addWidget(self.displayTable)
        self.totalLayout.addLayout(self.buttonLayout)
        #set the dialog box's layout
        self.setLayout(self.totalLayout)
        #connect the buttons
        self.quitButton.clicked.connect(self.close)        
        self.refreshButton.clicked.connect(self.refresh)
        
    def refresh(self):
        self.c.execute('SELECT * FROM {tn}'.\
            format(tn=self.tbl_name))
        self.tableValues = self.c.fetchall()
        #set up the table's number of rows and columns
        self.displayTable.setRowCount(len(self.tableValues))
        self.displayTable.setColumnCount(len(self.tableValues[0]))
        self.row = 0            
        #populate the table with values from the database
        for rowValues in self.tableValues:
            for self.col in range(0, len(self.tableValues[0])):
                #get a value, turn it into a string, then into a table item
                item = QTableWidgetItem(str(rowValues[self.col]))
                item.setFlags(Qt.ItemIsEnabled)#make the item non editable
                self.displayTable.setItem(self.row, self.col, item) #display item in table
            self.row += 1