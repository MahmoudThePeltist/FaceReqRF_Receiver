from PyQt4.QtGui import *
import sqlite3

class DisplayClass(QDialog):
    """This class displays a table of entered people"""
    
    def __init__(self):
        super(DisplayClass, self).__init__()
                
        self.setWindowTitle("Table Display")
        self.setWindowIcon(QIcon("images/FaceReqRFIcon.png"))
        self.setGeometry(25,50,535,400)
        #adding table and buttons
        self.displayTable = QTableWidget()
        self.refreshButton = QPushButton("Refresh")
        self.quitButton = QPushButton("Quit")
                
        #get the values from the database
        self.sqlite_file = 'database/my_db.sqlite'
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
                self.displayTable.setItem(self.row, self.col, QTableWidgetItem(rowValues[self.col]))
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
                self.displayTable.setItem(self.row, self.col, QTableWidgetItem(rowValues[self.col]))
            self.row += 1