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

    def query_week(self, week_start):
        query = "SELECT * FROM NOTE WHERE end_date between " + week_start.strftime(
            "%Y/%m/%d")+" and " + (week_start + timedelta(days=6)).strftime("%Y/%m/%d")

        if self.conn is not None:
            c = self.conn.cursor()
            data = c.execute(query)

        return data

    def create_event(self, data):
        if data is None:
            return
        else:
            self.data = data

        title = self.data['title']
        tags = self.data['tags']
        description = self.data['description']
        start_date = self.data['start_date']
        end_date = self.data['end_date']
        status = self.data['status']

        sql = """INSERT INTO note(description,begin_date,end_date,completion_status,title) VALUES(?,?,?,?,?);"""
        params = (description, start_date, end_date, status, title)

        c = self.conn.cursor()
        c.execute(sql, params)
        self.conn.commit()

    def delete_event(self, data):
        c = self.conn.cursor()
        deleteQuery = """DELETE FROM note WHERE title = ?"""
        values = (data, )
        c.execute(deleteQuery, values)
        self.conn.commit()
        print(values, "has been deleted")

    def update_event(self, data):
        if data is None:
            return
        else:
            self.data = data

        title = self.data['title']
        tags = self.data['tags']
        description = self.data['description']
        start_date = self.data['start_date']
        end_date = self.data['end_date']
        status = self.data['status']

        sql = """UPDATE note SET description = ?, begin_date= ?,end_date = ?,completion_status = ?,title = ? WHERE title = ? """

        params = (description, start_date, end_date, status, title, title)

        c = self.conn.cursor()
        c.execute(sql, params)
        self.conn.commit()


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

        self.buttonSubmit.clicked.connect(self.event_manager)
        self.buttonCancel.clicked.connect(self.view_day)

        self.calendarWidget.clicked.connect(self.select_date)
        self.calendarWidget.activated.connect(self.view_day)
        self.__set_defaults()

    # Application Functions
    def __set_defaults(self):
        self.stackedWidget.setCurrentIndex(0)

        self.selected_date = self.calendarWidget.selectedDate()
        self.min_date = self.get_sunday()
        self.data = self.connectDB.query_week(self.min_date)
        self.weekly_data = []
        for item in self.data:
            dic = {
                'id': item[0],
                'discription': item[1],
                'start_date': item[2],
                'end_date': item[3],
                'status': item[4],
                'title': item[5]
            }
            self.weekly_data.append(dic)

    def get_sunday(self):

        if self.selected_date.dayOfWeek() == 7:

            thisWeeksSunday = time.strptime(str(self.selected_date.year(
            )) + ' ' + str(self.selected_date.weekNumber()[0]) + ' 0', '%Y %W %w')

        else:
            thisWeeksSunday = time.strptime(str(self.selected_date.year(
            )) + ' ' + str(self.selected_date.weekNumber()[0]-1) + ' 0', '%Y %W %w')

        thisWeeksSunday = datetime.fromtimestamp(mktime(thisWeeksSunday))
        thisWeeksSunday = thisWeeksSunday.strftime('%B %d')

        return datetime.strptime(thisWeeksSunday, "%B %d")

    def select_date(self):
        self.selected_date = self.calendarWidget.selectedDate()
        self.selected_date = str(self.selected_date.year(
        )) + '/'+str(self.selected_date.month())+'/'+str(self.selected_date.day())

    def set_event_defaults(self):
        self.lineEditTags.clear()
        self.lineEditTitle.clear()
        self.textEdit.clear()
        self.dateEdit.clear()
        self.dateEdit_2.clear()
        self.horizontalSlider.setValue(0)

    def event_manager(self):
        if self.edit_flag == 0:
            self.connectDB.create_event(self.get_event_data())
        elif self.edit_flag == 1:
            self.connectDB.update_event(self.get_event_data())
        self.set_event_defaults()
        self.populate_daily()

    def get_event_data(self):

        data = {
            "title": self.lineEditTitle.text(),
            "tags": self.lineEditTags.text(),
            "description": self.textEdit.toPlainText(),
            "start_date": self.dateEdit.text(),
            "end_date": self.dateEdit_2.text(),
            "status": self.horizontalSlider.value()
        }

        return data

    def view_day(self):
        self.populate_daily()
        self.buttonDay.setDisabled(True)
        self.buttonMonth.setDisabled(False)
        self.buttonWeek.setDisabled(False)

        dateSelected = self.calendarWidget.selectedDate()

        self.labelDate_2.setText(dateSelected.toString("MMM dd"))

        self.stackedWidget.setCurrentIndex(2)

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

        if dateSelected.dayOfWeek() == 7:

            thisWeeksSunday = time.strptime(str(dateSelected.year(
            )) + ' ' + str(dateSelected.weekNumber()[0]) + ' 0', '%Y %W %w')
            self.labelMonth.setText(
                "Week"+' '+str(dateSelected.weekNumber()[0]+1)+" of "+str(self.calendarWidget.yearShown()))
        else:
            thisWeeksSunday = time.strptime(str(dateSelected.year(
            )) + ' ' + str(dateSelected.weekNumber()[0]-1) + ' 0', '%Y %W %w')
            self.labelMonth.setText(
                "Week"+' '+str(dateSelected.weekNumber()[0])+" of "+str(self.calendarWidget.yearShown()))

        thisWeeksSunday = datetime.fromtimestamp(mktime(thisWeeksSunday))
        thisWeeksSunday = thisWeeksSunday.strftime('%B %d')

        self.labelSunday.setText(thisWeeksSunday)

        date_1 = datetime.strptime(thisWeeksSunday, "%B %d")

        self.sun = (date_1 + timedelta(days=0)).strftime("%B %d")
        self.mon = (date_1 + timedelta(days=1)).strftime("%B %d")
        self.tue = (date_1 + timedelta(days=2)).strftime("%B %d")
        self.wed = (date_1 + timedelta(days=3)).strftime("%B %d")
        self.thu = (date_1 + timedelta(days=4)).strftime("%B %d")
        self.fri = (date_1 + timedelta(days=5)).strftime("%B %d")
        self.sat = (date_1 + timedelta(days=6)).strftime("%B %d")

        self.labelMonday.setText(self.mon)
        self.labelTuesday.setText(self.tue)
        self.labelWednesday.setText(self.wed)
        self.labelThursday.setText(self.thu)
        self.labelFriday.setText(self.fri)
        self.labelSaturday.setText(self.sat)

        self.display_weekly_view()
        self.stackedWidget.setCurrentIndex(3)

    def display_weekly_view(self):

        self.sun_list = []
        self.mon_list = []
        self.tue_list = []
        self.wed_list = []
        self.thu_list = []
        self.fri_list = []
        self.sat_list = []
        self.tableviewSunday.setRowCount(0)
        self.tableviewMonday.setRowCount(0)
        self.tableviewTuesday.setRowCount(0)
        self.tableviewWednesday.setRowCount(0)
        self.tableviewThursday.setRowCount(0)
        self.tableviewFriday.setRowCount(0)
        self.tableviewSaturday.setRowCount(0)
        for task in self.weekly_data:

            end_date_formatted = datetime.strptime(
                task['end_date'], "%m/%d/%Y").strftime("%B %d")

            if end_date_formatted == self.sun:
                self.sun_list.append(task)
            elif end_date_formatted == self.mon:
                self.mon_list.append(task)
            elif end_date_formatted == self.tue:
                self.tue_list.append(task)
            elif end_date_formatted == self.wed:
                self.wed_list.append(task)
            elif end_date_formatted == self.thu:
                self.thu_list.append(task)
            elif end_date_formatted == self.fri:
                self.fri_list.append(task)
            elif end_date_formatted == self.sat:
                self.sat_list.append(task)
            else:
                continue

        row_count = 1
        tablerow = 0
        for row in self.mon_list:
            self.tableviewMonday.setRowCount(row_count)

            self.tableviewMonday.setItem(
                tablerow, 0, QTableWidgetItem(row['title']))
            self.tableviewMonday.setItem(
                tablerow, 1, QTableWidgetItem(str(row['status'])))

            tablerow += 1
            row_count += 1

        row_count = 1
        tablerow = 0
        for row in self.sun_list:
            self.tableviewSunday.setRowCount(row_count)

            self.tableviewSunday.setItem(
                tablerow, 0, QTableWidgetItem(row['title']))
            self.tableviewSunday.setItem(
                tablerow, 1, QTableWidgetItem(str(row['status'])))

            tablerow += 1
            row_count += 1

        row_count = 1
        tablerow = 0
        for row in self.tue_list:
            self.tableviewTuesday.setRowCount(row_count)

            self.tableviewTuesday.setItem(
                tablerow, 0, QTableWidgetItem(row['title']))
            self.tableviewTuesday.setItem(
                tablerow, 1, QTableWidgetItem(str(row['status'])))

            tablerow += 1
            row_count += 1

        row_count = 1
        tablerow = 0
        for row in self.wed_list:
            self.tableviewWednesday.setRowCount(row_count)

            self.tableviewWednesday.setItem(
                tablerow, 0, QTableWidgetItem(row['title']))
            self.tableviewWednesday.setItem(
                tablerow, 1, QTableWidgetItem(str(row['status'])))

            tablerow += 1
            row_count += 1

        row_count = 1
        tablerow = 0
        for row in self.thu_list:
            self.tableviewThursday.setRowCount(row_count)

            self.tableviewThursday.setItem(
                tablerow, 0, QTableWidgetItem(row['title']))
            self.tableviewThursday.setItem(
                tablerow, 1, QTableWidgetItem(str(row['status'])))

            tablerow += 1
            row_count += 1

        row_count = 1
        tablerow = 0
        for row in self.fri_list:
            self.tableviewFriday.setRowCount(row_count)

            self.tableviewFriday.setItem(
                tablerow, 0, QTableWidgetItem(row['title']))
            self.tableviewFriday.setItem(
                tablerow, 1, QTableWidgetItem(str(row['status'])))

            tablerow += 1
            row_count += 1

        row_count = 1
        tablerow = 0
        for row in self.sat_list:
            self.tableviewSaturday.setRowCount(row_count)

            self.tableviewSaturday.setItem(
                tablerow, 0, QTableWidgetItem(row['title']))
            self.tableviewSaturday.setItem(
                tablerow, 1, QTableWidgetItem(str(row['status'])))

            tablerow += 1
            row_count += 1

    def create_event(self):
        self.set_event_defaults()
        self.edit_flag = 0
        dateSelected = self.calendarWidget.selectedDate()
        self.labelDate.setText(dateSelected.toString("MMM dd"))

        self.dateEdit.setMinimumDate(dateSelected)
        self.dateEdit_2.setMinimumDate(dateSelected)
        self.dateEdit.setDate(dateSelected)
        self.dateEdit_2.setDate(dateSelected)
        self.stackedWidget.setCurrentIndex(1)

        cur = self.connectDB.conn.cursor()
        query = 'SELECT * FROM note'

        row_count = 1
        tablerow = 0
        for row in cur.execute(query):
            self.tableWidget.setRowCount(row_count)

            self.tableWidget.setItem(tablerow, 0, QTableWidgetItem(row[5]))
            self.tableWidget.setItem(tablerow, 1, QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tablerow, 2, QTableWidgetItem(row[3]))
            self.tableWidget.setItem(tablerow, 3, QTableWidgetItem(row[4]))

            tablerow += 1
            row_count += 1

    def populate_daily(self):
        """
        SQL QUERY DELETE
        """
        dateSelected = self.calendarWidget.selectedDate()
        self.labelDate.setText(dateSelected.toString("MMM dd"))
      
        self.dateEdit.setMinimumDate(dateSelected)
        self.dateEdit_2.setMinimumDate(dateSelected)
        self.dateEdit.setDate(dateSelected)
        self.dateEdit_2.setDate(dateSelected)
       
        # Grab data from database and populate qLineEdit boxes
        cur = self.connectDB.conn.cursor()
        query = """SELECT * FROM note where end_date = ?"""
        params = (dateSelected.toString("M/d/yyyy"), )
        row_count = 1
        tablerow = 0
        for row in cur.execute(query, params):
            self.tableWidget.setRowCount(row_count)
            self.tableWidget.setItem(tablerow, 0, QTableWidgetItem(row[5]))
            self.tableWidget.setItem(tablerow, 1, QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tablerow, 2, QTableWidgetItem(row[3]))
            self.tableWidget.setItem(tablerow, 3, QTableWidgetItem(str(row[4])))

            tablerow += 1
            row_count += 1

    def edit_event(self):
        self.edit_flag = 1
        self.stackedWidget.setCurrentIndex(1)
        # when selecting an item on the QTableWidget it'll edit the note that you clicked
        cur = self.connectDB.conn.cursor()
        title = self.tableWidget.selectedItems()[0].text()
        sql = """SELECT * FROM note WHERE title = ?"""
        values = (title, )
        row_count = 1
        tablerow = 0
        for row in cur.execute(sql, values):
            self.lineEditTags.setText("placeholder")
            self.lineEditTitle.setText(row[5])
            self.textEdit.setText(row[1])
            self.horizontalSlider.setValue(row[4])
            tablerow += 1
            row_count += 1
        
    def delete_event(self):
        title = self.tableWidget.selectedItems()[0].text()
        self.connectDB.delete_event(title)
        self.populate_daily()

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
