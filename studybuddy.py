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

# events
1 - event_id                INTEGER
2 - title                   TEXT
3 - description             TEXT
4 - start_date              DATE
5 - end_date                DATE
6 - completion_status       BOOLEAN

# tags
1 - tag_id                  INTEGER
2 - tag_name                TEXT

# schedules
1 - schedule_id             INTEGER
2 - title                   TEXT
3 - description             TEXT
4 - start_date              DATE
5 - end_date                DATE
6 - day_of_week             TEXT

# event_tags
1 - event_id                INTEGER
2 - tag_id                  INTEGER

# schedule_tags
1 - schedule_id             INTEGER
2 - tag_id                  INTEGER

"""""


class Database_Controller():
    def __init__(self):
        self.path = "./database.db"

        self.conn = self.create_connection()
        self.create_tables()

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect("./sqliteDB/database.db")
            return conn
        except Error as e:
            print(e)

    def create_tables(self):
        sql_queries = """
            CREATE TABLE IF NOT EXISTS events (
                event_id INTEGER PRIMARY KEY,
                title TEXT,
                description TEXT,
                start_date DATE,
                end_date DATE,
                completion_status BOOLEAN
            );
            CREATE TABLE IF NOT EXISTS tags (
                tag_id INTEGER PRIMARY KEY,
                tag_name TEXT
            );
            CREATE TABLE IF NOT EXISTS event_tags (
                event_id INTEGER,
                tag_id INTEGER,
                FOREIGN KEY (event_id) REFERENCES events(event_id),
                FOREIGN KEY (tag_id) REFERENCES tags(tag_id),
                PRIMARY KEY (event_id, tag_id)
            );
            CREATE TABLE IF NOT EXISTS schedules (
                schedule_id INTEGER PRIMARY KEY,
                title TEXT,
                description TEXT,
                start_date DATE,
                end_date DATE,
                days_of_week TEXT
            );
            CREATE TABLE IF NOT EXISTS schedule_tags (
                schedule_id INTEGER,
                tag_id INTEGER,
                FOREIGN KEY (schedule_id) REFERENCES schedules(schedule_id),
                FOREIGN KEY (tag_id) REFERENCES tags(tag_id),
                PRIMARY KEY (schedule_id, tag_id)
            );
        """

        with self.conn:
            c = self.conn.cursor()
            c.executescript(sql_queries)

    def query_week(self, week_start):
        query = """SELECT * FROM events WHERE date(end_date) between ? and ?"""

        if self.conn is not None:
            c = self.conn.cursor()
            params = (week_start.strftime(
            "%Y-%m-%d"), (week_start + timedelta(days=6)).strftime("%Y-%m-%d"))
            print(
                params)
            print(query)
            data = c.execute(query, params)

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

        sql = """INSERT INTO events(description,start_date,end_date,completion_status, title) VALUES(?,?,?,?,?);"""
        params = (description, start_date, end_date, status, title)

        c = self.conn.cursor()
        c.execute(sql, params)
        self.conn.commit()

    def delete_event(self, data):
        c = self.conn.cursor()
        deleteQuery = """DELETE FROM events WHERE title = ?"""
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

        sql = """UPDATE events SET description = ?, start_date= ?,end_date = ?,completion_status = ?,title = ? WHERE title = ? """

        params = (description, start_date, end_date, status, title, title)

        c = self.conn.cursor()
        c.execute(sql, params)
        self.conn.commit()


class Main(QMainWindow):
    def __init__(self):
        # Inherit all methods and properties from QMainWindow
        super(Main, self).__init__()
        # Load UI file created in Qt Designer
        loadUi("studybuddy.ui", self)
        self.connectDB = Database_Controller()

        """
        Indexes

        0 - Month View
        1 - Modify Event View
        2 - Daily View
        3 - Weekly View
        4 - Search View
        5 - Schedule View
        6 - Modify Schedule View
        7 - Settings View

        """

        # Navigation Menu

        # Calendar
        self.buttonNavigationCalendarDay.clicked.connect(self.view_day)
        self.buttonNavigationCalendarMonth.clicked.connect(self.view_month)
        self.buttonNavigationCalendarWeek.clicked.connect(self.view_week)

        # Search
        self.buttonNavigationSearch.clicked.connect(self.view_search)

        # Schedule
        self.buttonNavigationScheduleView.clicked.connect(self.view_schedule)
        self.buttonNavigationScheduleAdd.clicked.connect(self.create_schedule)

        # Settings
        self.buttonNavigationSettings.clicked.connect(self.view_settings)

        # Weekly View
        self.buttonViewWeeklyCancel.clicked.connect(self.view_month)

        # Daily View
        self.buttonViewDailyAdd.clicked.connect(self.create_event)
        self.buttonViewDailyEdit.clicked.connect(self.edit_event)
        self.buttonViewDailyDelete.clicked.connect(self.delete_event)

        # Create / Edit Event View
        self.buttonModifyEventSubmit.clicked.connect(self.event_manager)
        self.buttonModifyEventCancel.clicked.connect(self.view_month)
        self.buttonViewDailyBack.clicked.connect(self.view_day)

        # Calendar Interaction
        self.calendarWidget.clicked.connect(self.select_date)
        self.calendarWidget.activated.connect(self.view_day)

        # Defaults
        self.__set_defaults()

    # Application Functions
    def __set_defaults(self):
        self.stackedWidgetViews.setCurrentIndex(0)
        self.buttonNavigationCalendarMonth.setDisabled(True)
        self.selected_date = self.calendarWidget.selectedDate()
        self.min_date = self.get_sunday()
        self.data = self.connectDB.query_week(self.min_date)
        self.weekly_data = []
        for item in self.data:
            dic = {
                'event_id': item[0],
                'title': item[1],
                'description': item[2],
                'start_date': item[3],
                'end_date': item[4],
                'completion_status': item[5]
            }
            self.weekly_data.append(dic)

    # VIEWS


    def view_day(self):
        self.populate_daily()
        self.buttonNavigationCalendarDay.setDisabled(True)
        self.buttonNavigationCalendarMonth.setDisabled(False)
        self.buttonNavigationCalendarWeek.setDisabled(False)
        self.buttonNavigationSearch.setDisabled(False)
        self.buttonNavigationScheduleView.setDisabled(False)
        self.buttonNavigationScheduleAdd.setDisabled(False)
        self.buttonNavigationSettings.setDisabled(False)
        dateSelected = self.calendarWidget.selectedDate()
        self.labelViewDailyDate.setText(dateSelected.toString("MMM dd"))
        self.stackedWidgetViews.setCurrentIndex(2)

    def view_month(self):
        self.buttonNavigationCalendarDay.setDisabled(False)
        self.buttonNavigationCalendarMonth.setDisabled(True)
        self.buttonNavigationCalendarWeek.setDisabled(False)
        self.buttonNavigationSearch.setDisabled(False)
        self.buttonNavigationScheduleView.setDisabled(False)
        self.buttonNavigationScheduleAdd.setDisabled(False)
        self.buttonNavigationSettings.setDisabled(False)
        self.stackedWidgetViews.setCurrentIndex(0)

    def view_week(self):
        self.buttonNavigationCalendarDay.setDisabled(False)
        self.buttonNavigationCalendarMonth.setDisabled(False)
        self.buttonNavigationCalendarWeek.setDisabled(True)
        self.buttonNavigationSearch.setDisabled(False)
        self.buttonNavigationScheduleView.setDisabled(False)
        self.buttonNavigationScheduleAdd.setDisabled(False)
        self.buttonNavigationSettings.setDisabled(False)

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
        thisWeeksSunday = thisWeeksSunday.strftime('%Y-%m-%d')

        self.labelSunday.setText(thisWeeksSunday)

        date_1 = datetime.strptime(thisWeeksSunday, '%Y-%m-%d')

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
        self.stackedWidgetViews.setCurrentIndex(3)

    def view_search(self):
        self.stackedWidgetViews.setCurrentIndex(4)
        self.buttonNavigationCalendarDay.setDisabled(False)
        self.buttonNavigationCalendarMonth.setDisabled(False)
        self.buttonNavigationCalendarWeek.setDisabled(False)
        self.buttonNavigationSearch.setDisabled(True)
        self.buttonNavigationScheduleView.setDisabled(False)
        self.buttonNavigationScheduleAdd.setDisabled(False)
        self.buttonNavigationSettings.setDisabled(False)

    def view_schedule(self):
        self.stackedWidgetViews.setCurrentIndex(5)
        self.buttonNavigationCalendarDay.setDisabled(False)
        self.buttonNavigationCalendarMonth.setDisabled(False)
        self.buttonNavigationCalendarWeek.setDisabled(False)
        self.buttonNavigationSearch.setDisabled(False)
        self.buttonNavigationScheduleView.setDisabled(True)
        self.buttonNavigationScheduleAdd.setDisabled(False)
        self.buttonNavigationSettings.setDisabled(False)

    def view_settings(self):
        self.stackedWidgetViews.setCurrentIndex(7)
        self.buttonNavigationCalendarDay.setDisabled(False)
        self.buttonNavigationCalendarMonth.setDisabled(False)
        self.buttonNavigationCalendarWeek.setDisabled(False)
        self.buttonNavigationSearch.setDisabled(False)
        self.buttonNavigationScheduleView.setDisabled(False)
        self.buttonNavigationScheduleAdd.setDisabled(False)
        self.buttonNavigationSettings.setDisabled(True)

    # EVENTS

    def create_event(self):
        self.set_event_defaults()
        self.edit_flag = 0
        dateSelected = self.calendarWidget.selectedDate()
        self.labelModifyEventDate.setText(dateSelected.toString("MMM dd"))

        self.dataModifyEventStartDate.setMinimumDate(dateSelected)
        self.dataModifyEventEndDate.setMinimumDate(dateSelected)
        self.dataModifyEventStartDate.setDate(dateSelected)
        self.dataModifyEventEndDate.setDate(dateSelected)
        self.stackedWidgetViews.setCurrentIndex(1)

        cur = self.connectDB.conn.cursor()
        query = 'SELECT * FROM events'

        row_count = 1
        tablerow = 0
        for row in cur.execute(query):
            self.tableViewDaily.setRowCount(row_count)

            self.tableViewDaily.setItem(tablerow, 0, QTableWidgetItem(row[5]))
            self.tableViewDaily.setItem(tablerow, 1, QTableWidgetItem(row[1]))
            self.tableViewDaily.setItem(tablerow, 2, QTableWidgetItem(row[3]))
            self.tableViewDaily.setItem(tablerow, 3, QTableWidgetItem(row[4]))

            tablerow += 1
            row_count += 1

    def edit_event(self):
        if len(self.tableViewDaily.selectedItems()) == 0:
            return

        self.edit_flag = 1
        self.stackedWidgetViews.setCurrentIndex(1)
        # when selecting an item on the QTableWidget it'll edit the events that you clicked
        cur = self.connectDB.conn.cursor()
        title = self.tableViewDaily.selectedItems()[0].text()
        sql = """SELECT * FROM events WHERE title = ?"""
        values = (title, )
        row_count = 1
        tablerow = 0
        for row in cur.execute(sql, values):
            self.dataModifyEventTags.setText("placeholder")
            self.dataModifyEventTitle.setText(row[5])
            self.dataModifyEventDescription.setText(row[1])
            self.dataModifyEventStatus.setValue(row[4])
            tablerow += 1
            row_count += 1

    def delete_event(self):
        title = self.tableViewDaily.selectedItems()[0].text()
        self.connectDB.delete_event(title)
        self.populate_daily()

    def event_manager(self):
        if self.edit_flag == 0:
            self.connectDB.create_event(self.get_event_data())
        elif self.edit_flag == 1:
            self.connectDB.update_event(self.get_event_data())
        self.set_event_defaults()
        self.populate_daily()

    # SCHEDULE

    def create_schedule(self):
        self.stackedWidgetViews.setCurrentIndex(6)
        self.buttonNavigationCalendarDay.setDisabled(False)
        self.buttonNavigationCalendarMonth.setDisabled(False)
        self.buttonNavigationCalendarWeek.setDisabled(False)
        self.buttonNavigationSearch.setDisabled(False)
        self.buttonNavigationScheduleView.setDisabled(False)
        self.buttonNavigationScheduleAdd.setDisabled(True)
        self.buttonNavigationSettings.setDisabled(False)

    def edit_schedule(self):
        pass

    def delete_schedule(self):
        pass

    # OTHER

    def format_completion_status(self, data):
        if data == 0:
            return "Incomplete"
        else:
            return "Completed"

    def get_sunday(self):

        if self.selected_date.dayOfWeek() == 7:

            thisWeeksSunday = time.strptime(str(self.selected_date.year(
            )) + ' ' + str(self.selected_date.weekNumber()[0]) + ' 0', '%Y %W %w')

        else:
            thisWeeksSunday = time.strptime(str(self.selected_date.year(
            )) + ' ' + str(self.selected_date.weekNumber()[0]-1) + ' 0', '%Y %W %w')

        thisWeeksSunday = datetime.fromtimestamp(mktime(thisWeeksSunday))
        thisWeeksSunday = thisWeeksSunday.strftime('%Y-%m-%d')

        return datetime.strptime(thisWeeksSunday, "%Y-%m-%d")

    def select_date(self):
        self.selected_date = self.calendarWidget.selectedDate()
        self.selected_date = str(self.selected_date.year(
        )) + '-'+str(self.selected_date.month())+'-'+str(self.selected_date.day())

    def set_event_defaults(self):
        self.dataModifyEventTags.clear()
        self.dataModifyEventTitle.clear()
        self.dataModifyEventDescription.clear()
        self.dataModifyEventStartDate.clear()
        self.dataModifyEventEndDate.clear()
        self.dataModifyEventStatus.setValue(0)

    def get_event_data(self):
        data = {
            "title": self.dataModifyEventTitle.text(),
            "tags": self.dataModifyEventTags.text(),
            "description": self.dataModifyEventDescription.toPlainText(),
            "start_date": self.dataModifyEventStartDate.text(),
            "end_date": self.dataModifyEventEndDate.text(),
            "status": self.dataModifyEventStatus.value()
        }
        return data

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
                task['end_date'], "%Y-%m-%d").strftime("%B %d")

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
                tablerow, 1, QTableWidgetItem(self.format_completion_status(row['completion_status'])))

            tablerow += 1
            row_count += 1

        row_count = 1
        tablerow = 0
        for row in self.sun_list:
            self.tableviewSunday.setRowCount(row_count)

            self.tableviewSunday.setItem(
                tablerow, 0, QTableWidgetItem(row['title']))
            self.tableviewSunday.setItem(
                tablerow, 1, QTableWidgetItem(self.format_completion_status(row['completion_status'])))

            tablerow += 1
            row_count += 1

        row_count = 1
        tablerow = 0
        for row in self.tue_list:
            self.tableviewTuesday.setRowCount(row_count)

            self.tableviewTuesday.setItem(
                tablerow, 0, QTableWidgetItem(row['title']))
            self.tableviewTuesday.setItem(
                tablerow, 1, QTableWidgetItem(self.format_completion_status(row['completion_status'])))

            tablerow += 1
            row_count += 1

        row_count = 1
        tablerow = 0
        for row in self.wed_list:
            self.tableviewWednesday.setRowCount(row_count)

            self.tableviewWednesday.setItem(
                tablerow, 0, QTableWidgetItem(row['title']))
            self.tableviewWednesday.setItem(
                tablerow, 1, QTableWidgetItem(self.format_completion_status(row['completion_status'])))

            tablerow += 1
            row_count += 1

        row_count = 1
        tablerow = 0
        for row in self.thu_list:
            self.tableviewThursday.setRowCount(row_count)

            self.tableviewThursday.setItem(
                tablerow, 0, QTableWidgetItem(row['title']))
            self.tableviewThursday.setItem(
                tablerow, 1, QTableWidgetItem(self.format_completion_status(row['completion_status'])))

            tablerow += 1
            row_count += 1

        row_count = 1
        tablerow = 0
        for row in self.fri_list:
            self.tableviewFriday.setRowCount(row_count)

            self.tableviewFriday.setItem(
                tablerow, 0, QTableWidgetItem(row['title']))
            self.tableviewFriday.setItem(
                tablerow, 1, QTableWidgetItem(self.format_completion_status(row['completion_status'])))

            tablerow += 1
            row_count += 1

        row_count = 1
        tablerow = 0
        for row in self.sat_list:
            self.tableviewSaturday.setRowCount(row_count)

            self.tableviewSaturday.setItem(
                tablerow, 0, QTableWidgetItem(row['title']))
            self.tableviewSaturday.setItem(
                tablerow, 1, QTableWidgetItem(self.format_completion_status(row['completion_status'])))

            tablerow += 1
            row_count += 1

    def populate_daily(self):
        """
        SQL QUERY DELETE
        """
        dateSelected = self.calendarWidget.selectedDate()
        self.labelModifyEventDate.setText(dateSelected.toString("MMM dd"))
        self.dataModifyEventStartDate.setMinimumDate(dateSelected)
        self.dataModifyEventEndDate.setMinimumDate(dateSelected)
        self.dataModifyEventStartDate.setDate(dateSelected)
        self.dataModifyEventEndDate.setDate(dateSelected)

        # Grab data from database and populate qLineEdit boxes
        cur = self.connectDB.conn.cursor()
        query = """SELECT * FROM events where date(end_date) = ?"""
        params = (dateSelected.toString("yyyy-MM-dd"), )
        row_count = 1
        tablerow = 0
        for row in cur.execute(query, params):
            if row is not None:
                self.tableViewDaily.setRowCount(row_count)
                self.tableViewDaily.setItem(
                    tablerow, 0, QTableWidgetItem(row[1]))
                self.tableViewDaily.setItem(
                    tablerow, 1, QTableWidgetItem(row[3]))
                self.tableViewDaily.setItem(
                    tablerow, 2, QTableWidgetItem(row[4]))
                self.tableViewDaily.setItem(
                    tablerow, 3, QTableWidgetItem(self.format_completion_status(row[5])))
                tablerow += 1
                row_count += 1


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
