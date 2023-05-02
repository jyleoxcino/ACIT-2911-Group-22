import sys
import sqlite3
import datetime

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
from sqlite3 import Error

"""""
SQLite database

Event Properties
- Title         STRING
- Description   STRING
- Tags          STRING?
- Start Date    DATE/TIME
- Due Date      DATE/TIME
- Complete      BOOLEAN

"""""

class Database_Controller():
    def __init__(self):
        self.path = "./database.db"
        
        self.conn = self.create_connection()
        self.create_note_table()
    
    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect("./sqliteDB/database.db")
            return conn
        except Error as e:
            print(e)

        return conn
        
    def create_note_table(self):
        sql_create_note_table = """ CREATE TABLE IF NOT EXISTS note(
                                        id integer PRIMARY KEY,
                                        description text,
                                        begin_date text,
                                        end_date text,
                                        completion_status integer,
                                        title text
                                    ); """
        
        
        if self.conn is not None:
            c = self.conn.cursor()
            c.execute(sql_create_note_table)

class Main(QMainWindow):
    def __init__(self):
        # Inherit all methods and properties from QMainWindow
        super(Main, self).__init__()
        # Load UI file created in Qt Designer
        loadUi("untitled.ui", self)
        self.connectDB = Database_Controller()
        
    # Application Functions

    def calendar_edit(self):
        pass

    def edit_note(self):
        pass

    # Database Functions

 
    def create_event(self):
        """
        add event to database
        SQL QUERY INSERT
        """
        pass

    def update_event(self):
        """
        modify existing event in database
        SQL QUERY UPDATE 
        """
        pass

    def delete_event(self):
        """
        SQL QUERY DELETE
        """
        pass


if __name__ == "__main__":
    """
    Loads UI and initializes studybuddy window
    """
    
    

    # Create QApplication Instance
    app = QApplication(sys.argv)
    # Create Main Instance
    ui = Main()
    # Load Main (GUI)
    ui.show()
    # Start QApplication
    app.exec_()