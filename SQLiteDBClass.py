import sqlite3
import os

class database_manager():
    """This class is to access and modify the database"""
    
    def __init__(self,parent = None):    
        #get the local directory
        self.localDir = os.path.dirname(os.path.realpath(__file__))    
        # Connecting to the database file
        sqlite_file = self.localDir + '/database/my_db.sqlite'
        self.tbl_name = 'Employees';
        self.conn = sqlite3.connect(sqlite_file)
        self.c = self.conn.cursor()

    #function to create a new database table
    def create_table(self,table_name1, new_field, field_type, prim_key = 0):   
        prim_key_txt = ""    
        if prim_key == 1:
            prim_key_txt = "PRIMARY KEY"
        self.c.execute('CREATE TABLE {tn} ("{nf}" {ft} {pk})'\
            .format(tn=table_name1, nf=new_field, ft=field_type, pk = prim_key_txt)) 

    #function to add a new column to an existing data
    def add_column(self,table_name, new_column, column_type):    
        self.c.execute('ALTER TABLE {tn} ADD COLUMN "{cn}" {ct}'\
            .format(tn = table_name, cn = new_column, ct = column_type))
    
    #function to build the employee table
    def create_employee_table(self):
        try:
            self.create_table(self.tbl_name,'ID','INTEGER',1)
            self.add_column(self.tbl_name,'First Name','TEXT')
            self.add_column(self.tbl_name,'Last Name','TEXT')
            self.add_column(self.tbl_name,'Position','TEXT')
            self.add_column(self.tbl_name,'File Name','TEXT')
        #exception handling in case table exists
        except sqlite3.OperationalError:
            print 'Table ' + self.tbl_name + ' already exists!'

    #function to insert a specific value into a specific column of a row with a specific index and update
    def add_value(self, table_name, id_column, column_name, id_num, value):
        self.c.execute("INSERT OR IGNORE INTO {tn} ({idf}, '{cn}') VALUES ({im}, '{va}')".\
            format(tn=table_name, idf=id_column, cn=column_name, im=id_num, va=value))   
        print('Added {va} value to {cn} column in {idf} number {im}'.\
            format(va=value, cn=column_name, idf=id_column, im=id_num))    
        self.c.execute("UPDATE {tn} SET '{cn}'=('{va}') WHERE {idf}=({im})".\
            format(tn=table_name, cn=column_name, va=value, idf=id_column, im=id_num))
        self.get_value('*',table_name,'ID','3')

    #function to query the database for a specific value
    def get_value(self, column_name,table_name,column_where,column_value):
        self.c.execute('SELECT {cn} FROM {tn} WHERE {cw}="{cv}"'.\
            format(cn=column_name, tn=table_name, cw=column_where, cv=column_value))
        values = self.c.fetchall()
        return values
        
    #commit changes and close the database
    def commit_close(self):
        self.conn.commit()
        self.conn.close()