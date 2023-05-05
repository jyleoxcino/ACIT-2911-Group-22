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
    
    def dataInsert(self, data):
        if data is None:
            return
        else:
            self.data = data
        print(self.data)
        title = self.data['title']
        tags = self.data['tags']
        description = self.data['description']
        start_date = self.data['start_date']
        end_date = self.data['end_date']
        status = self.data['status']
        print(title,tags,description,start_date,end_date,status)
        sql = """INSERT INTO note(description,begin_date,end_date,completion_status,title) VALUES(?,?,?,?,?);""" 
        params = (description,start_date,end_date,status,title)
        c = self.conn.cursor()
        c.execute(sql,params)
        self.conn.commit()


    def DeleteTask(self,title):
        c = self.conn.cursor()
        
        deleteQuery = """DELETE FROM note WHERE title = ?"""
        values = (title, )
        c.execute(deleteQuery,values)
        self.conn.commit()

    def dataUpdate(self,data):
        if data is None:
            return
        else:
            self.data = data
        print(self.data)
        title = self.data['title']
        tags = self.data['tags']
        description = self.data['description']
        start_date = self.data['start_date']
        end_date = self.data['end_date']
        status = self.data['status']
        print(title,tags,description,start_date,end_date,status)
        sql = """UPDATE note SET description = ?, begin_date= ?,end_date = ?,completion_status = ?,title = ? WHERE title = ? """ 
        params = (description,start_date,end_date,status,title,title)
        c = self.conn.cursor()
        c.execute(sql,params)
        self.conn.commit()



class Main(QMainWindow):
    def __init__(self):
        # Inherit all methods and properties from QMainWindow
        super(Main, self).__init__()
        # Load UI file created in Qt Designer
        loadUi("untitled.ui", self)
        self.connectDB = Database_Controller()

        self.calendarWidget.clicked.connect(self.create_note)
        self.buttonCancel.clicked.connect(self.set_default)
        self.buttonSubmit.clicked.connect(self.submit_button)
        self.buttonDay.clicked.connect(self.view_day)
        self.buttonMonth.clicked.connect(self.view_month)
        self.buttonWeek.clicked.connect(self.view_week)
        
        self.pushButton_2.clicked.connect(self.create_event)
        self.pushButton_3.clicked.connect(self.edit_event)
        self.pushButton.clicked.connect(self.delete_event)
        self.buttonCancel_2.clicked.connect(self.set_default)
        self.pushButton_4.clicked.connect(self.edit_note2)
      
        self.calendarWidget.activated.connect(self.view_day)
        self.edit_event
        self.pushButton.clicked.connect(self.delete_event)
        self.buttonSubmit.clicked.connect(self.updateData)
    # Application Functions

    def submit_button(self):
        while True:
            self.stackedWidget.setCurrentIndex(0)
            tags = self.lineEditTags.text()
            title = self.lineEditTitle.text()
            description = self.lineEditDescription.text()
            start_date = self.dateEdit.text()
            end_date = self.dateEdit_2.text()
            status = self.horizontalSlider.value()
            self.lineEditTags.clear()
            self.lineEditTitle.clear()
            self.lineEditDescription.clear()
            self.dateEdit.clear()
            self.dateEdit_2.clear()
            self.horizontalSlider.setValue(0)
            data = {
                "title": title,
                "tags" : tags,
                "description": description,
                "start_date" : start_date,
                "end_date" : end_date,
                "status" : status
            }
            if self.edit_flag == 0:
                self.connectDB.dataInsert(data)
            elif self.edit_flag == 1:
                self.connectDB.dataUpdate(data)

            # print(f'{tags}, {title}, {description}, {start_date}, {end_date}, {status}')
            break

    

    def set_default(self):
        self.stackedWidget.setCurrentIndex(0)

    def calendar_edit(self):
        pass

    def edit_note(self):
        pass

    def create_note(self):
        self.stackedWidget.setCurrentIndex(1)
        self.edit_flag = 0
        

    
    # Database Functions

    # def create_connection(self):
    #     conn = None
    #     try:
    #         conn = sqlite3.connect("./database.db")
    #         print(sqlite3.version)
    #     except Error as e:
    #         print(e)
    #     finally:
    #         if conn:
    #             conn.close()
            
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
        title = self.lineEditDelete.text()
        self.connectDB.DeleteTask(title)
        cur = self.connectDB.conn.cursor()
        query = 'SELECT * FROM note'

        row_count = 1
        tablerow = 0
        for row in cur.execute(query):
            self.tableWidget.setRowCount(row_count)
            print(row)
            self.tableWidget.setItem(tablerow, 0, QTableWidgetItem(row[5]))
            self.tableWidget.setItem(tablerow, 1, QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tablerow, 2, QTableWidgetItem(row[3]))
            self.tableWidget.setItem(tablerow, 3, QTableWidgetItem(row[4]))

            tablerow += 1
            row_count += 1
       
        

    def view_month(self):
        self.buttonDay.setDisabled(False)
        self.buttonMonth.setDisabled(True)
        self.buttonWeek.setDisabled(False)
        self.stackedWidget.setCurrentIndex(0)
    
    def view_week(self):
        self.buttonDay.setDisabled(False)
        self.buttonMonth.setDisabled(False)
        self.buttonWeek.setDisabled(True)

        dateSelected = self.calendarWidget.selectedDate()
        
        if dateSelected.dayOfWeek()== 7:
            
            thisWeeksSunday = time.strptime(str(dateSelected.year()) + ' ' + str(dateSelected.weekNumber()[0]) + ' 0','%Y %W %w')
            self.labelMonth.setText("Week"+' '+str(dateSelected.weekNumber()[0]+1)+" of "+str(self.calendarWidget.yearShown()))
        else:
            thisWeeksSunday = time.strptime(str(dateSelected.year()) + ' ' + str(dateSelected.weekNumber()[0]-1) + ' 0','%Y %W %w')
            self.labelMonth.setText("Week"+' '+str(dateSelected.weekNumber()[0])+" of "+str(self.calendarWidget.yearShown()))

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

        self.stackedWidget.setCurrentIndex(3)

    def view_day(self):
        self.buttonDay.setDisabled(True)
        self.buttonMonth.setDisabled(False)
        self.buttonWeek.setDisabled(False)

        dateSelected = self.calendarWidget.selectedDate()
  
        self.labelDate_2.setText(dateSelected.toString("MMM dd"))
        
        self.stackedWidget.setCurrentIndex(2)

    def edit_event(self):
        dateSelected = self.calendarWidget.selectedDate()
        self.labelDate.setText(dateSelected.toString("MMM dd"))
      
        self.dateEdit.setMinimumDate(dateSelected)
        self.dateEdit_2.setMinimumDate(dateSelected)
        self.dateEdit.setDate(dateSelected)
        self.dateEdit_2.setDate(dateSelected)
       
        # when selecting an item on the QTableWidget it'll edit the note that you clicked
        self.stackedWidget.setCurrentIndex(1)
        # Grab data from database and populate qLineEdit boxes
        cur = self.connectDB.conn.cursor()
        query = 'SELECT * FROM note'

        row_count = 1
        tablerow = 0
        for row in cur.execute(query):
            self.tableWidget.setRowCount(row_count)
            print(row)
            self.tableWidget.setItem(tablerow, 0, QTableWidgetItem(row[5]))
            self.tableWidget.setItem(tablerow, 1, QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tablerow, 2, QTableWidgetItem(row[3]))
            self.tableWidget.setItem(tablerow, 3, QTableWidgetItem(row[4]))

            tablerow += 1
            row_count += 1

    def edit_note2(self):
        self.edit_flag = 1
        self.stackedWidget.setCurrentIndex(1)
        cur = self.connectDB.conn.cursor()
        title = self.lineEditDelete.text()
        # sql = """SELECT 'title','tags', 'description', 'begin_date', 'end_date', 'completion_status' FROM note WHERE title = ?"""
        sql = """SELECT * FROM note WHERE title = ?"""
        values = (title, )
        row_count = 1
        tablerow = 0
        for row in cur.execute(sql, values):
            print(row)
            # self.stackedWidget.setRowCount(row_count)
            # print(row)
            self.lineEditTags.setText("placeholder")
            self.lineEditTitle.setText(row[5])
            self.lineEditDescription.setText(row[1])
            # self.dateEdit.setDate(datetime.strptime(row[2]))
            # self.dateEdit_2.setDate(datetime.strptime(row[3]))
            self.horizontalSlider.setValue(row[4])
            

            tablerow += 1
            row_count += 1

           
        # self.lineEditTags.clear()
        # self.lineEditTitle.clear()
        # self.lineEditDescription.clear()
        # self.dateEdit.clear()
        # self.dateEdit_2.clear()
           
    def updateData(self):
            tags = self.lineEditTags.text()
            title = self.lineEditTitle.text()
            description = self.lineEditDescription.text()
            start_date = self.dateEdit.text()
            end_date = self.dateEdit_2.text()
            status = self.horizontalSlider.value()
            self.lineEditTags.clear()
            self.lineEditTitle.clear()
            self.lineEditDescription.clear()
            self.dateEdit.clear()
            self.dateEdit_2.clear()
            self.horizontalSlider.setValue(0)
            data = {
                "title": title,
                "tags" : tags,
                "description": description,
                "start_date" : start_date,
                "end_date" : end_date,
                "status" : status
            }
            self.connectDB.dataUpdate(data)
        


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

    
# sql = """insert into note(description,begin_date,end_date,completion_status,title) values(?,?,?)""", (description,title,start_date,end_date,status)