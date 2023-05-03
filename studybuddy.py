import sys
import sqlite3
import time
from time import mktime
from PyQt5.QtWidgets import *
from datetime import datetime, timedelta, date

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
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
        
        self.buttonDay.clicked.connect(self.view_day)
        self.buttonMonth.clicked.connect(self.view_month)
        self.buttonWeek.clicked.connect(self.view_week)
        
        self.pushButton_2.clicked.connect(self.create_event)
        self.pushButton_3.clicked.connect(self.edit_event)
        self.pushButton.clicked.connect(self.delete_event)
        
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.calendarWidget.activated.connect(self.view_day)
        
    # Application Functions
    def calendarDateChanged(self):
        print("date changed")
        
        dateSelected = self.calendarWidget.selectedDate()
        print(dateSelected)
        self.labelDate_2.setText(dateSelected.toString("MMM dd"))
        self.labelDate.setText(dateSelected.toString("MMM dd"))
      
        self.dateEdit.setMinimumDate(dateSelected)
        self.dateEdit_2.setMinimumDate(dateSelected)
        self.dateEdit.setDate(dateSelected)
        self.dateEdit_2.setDate(dateSelected)
        print(dateSelected.dayOfWeek())
        

        if dateSelected.dayOfWeek()== 7:
            
            thisWeeksSunday = time.strptime(str(dateSelected.year()) + ' ' + str(dateSelected.weekNumber()[0]) + ' 0','%Y %W %w')
        else:
            thisWeeksSunday = time.strptime(str(dateSelected.year()) + ' ' + str(dateSelected.weekNumber()[0]-1) + ' 0','%Y %W %w')
        
        thisWeeksSunday = datetime.fromtimestamp(mktime(thisWeeksSunday))
        thisWeeksSunday = thisWeeksSunday.strftime('%B %d')
        
        self.labelSunday.setText(thisWeeksSunday)
        date_1 = datetime.strptime(thisWeeksSunday, "%B %d")

        mon = (date_1 + timedelta(days=1)).strftime("%B %d")
        tue = (date_1 + timedelta(days=2)).strftime("%B %d")
        wed = (date_1 + timedelta(days=3)).strftime("%B %d")
        thu = (date_1 + timedelta(days=4)).strftime("%B %d")
        fri = (date_1 + timedelta(days=5)).strftime("%B %d")
        sat = (date_1 + timedelta(days=6)).strftime("%B %d")

        self.labelMonday.setText(mon)
        self.labelTuesday.setText(tue)
        self.labelWednesday.setText(wed)
        self.labelThursday.setText(thu)
        self.labelFriday.setText(fri)
        self.labelSaturday.setText(sat)  

    def calendar_edit(self):
        pass

    def edit_note(self):
        pass

    # Database Functions

 
   

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

    def view_month(self):
        self.stackedWidget.setCurrentIndex(0)

    def view_week(self):
        self.stackedWidget.setCurrentIndex(3)

    def view_day(self):
        self.stackedWidget.setCurrentIndex(2)

    def create_event(self):
        self.stackedWidget.setCurrentIndex(1)
        
    def edit_event(self):
        # when selecting an item on the QTableWidget it'll edit the note that you clicked
        self.stackedWidget.setCurrentIndex(1)
        # Grab data from database and populate qLineEdit boxes

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