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
            data = c.execute(query, params)
        return data

    def create_event(self, data):
        if data is None:
            return
        else:
            self.data = data

        title = self.data['title']
        description = self.data['description']
        start_date = self.data['start_date']
        end_date = self.data['end_date']
        status = self.data['completion_status']

        sql = """INSERT INTO events(description,start_date,end_date,completion_status, title) VALUES(?,?,?,?,?);"""
        params = (description, start_date, end_date, status, title)
        print("event has been created")
        c = self.conn.cursor()
        c.execute(sql, params)
        self.conn.commit()

    def delete_event(self, data):
        c = self.conn.cursor()
        deleteQuery = """DELETE FROM events WHERE title = ?"""
        values = (data, )
        c.execute(deleteQuery, values)
        self.conn.commit()
        print(data, "has been deleted from the database.")

    def update_event(self, data):
        if data is None:
            return
        else:
            self.data = data

        event_id = self.data['event_id']
        title = self.data['title']
        description = self.data['description']
        start_date = self.data['start_date']
        end_date = self.data['end_date']
        completion_status = self.data['completion_status']

        sql = """UPDATE events SET title = ?, description = ?, start_date= ?, end_date = ?, completion_status = ? WHERE event_id = ? """

        params = (title, description, start_date, end_date, completion_status, event_id)

        c = self.conn.cursor()
        c.execute(sql, params)
        self.conn.commit()

    def get_schedule_tags(self, schedule_id):
        pass

    def get_event_tags(self, event_id):
        query = """SELECT * FROM event_tags WHERE event_id = ?"""
        params = (event_id, )
        c = self.conn.cursor()
        data = c.execute(query, params)
        return data

    def get_tags(self, data):
        tag_names = []
        query = f'SELECT * FROM tags WHERE tag_id = ?'
        c = self.conn
        for tag_id in data:
            params = (tag_id[1], )
            data = c.execute(query, params)
            tag_names.append(data.fetchone()[1])
        return tag_names

    def get_all_tags(self):
        query = """ SELECT * FROM tags"""
        c = self.conn.cursor()
        cursor = c.execute(query)
        data = cursor.fetchall()
        return data

class Main(QMainWindow):
    def __init__(self):
        # Inherit all methods and properties from QMainWindow
        super(Main, self).__init__()
        # Load UI file created in Qt Designer
        loadUi("studybuddy.ui", self)
        self.connectDB = Database_Controller()

        self.database_tags = self.connectDB.get_all_tags()

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
        self.tableViewDaily.doubleClicked.connect(self.edit_event)
        self.buttonViewDailyBack.clicked.connect(self.view_day)

        # Create / Edit Event View
        self.buttonModifyEventSubmit.clicked.connect(self.event_manager)
        self.buttonModifyEventCancel.clicked.connect(self.view_day)
        self.buttonModifyEventAddTag.clicked.connect(self.add_event_tag)
        self.buttonModifyEventDeleteTag.clicked.connect(self.delete_event_tag)

        # Calendar Interaction
        self.calendarWidget.clicked.connect(self.select_date)
        self.calendarWidget.activated.connect(self.view_day)

        # Defaults
        self.__set_defaults()

    # Application Functions
    def __set_defaults(self):
        self.stackedWidgetViews.setCurrentIndex(0)
        self.buttonNavigationCalendarMonth.setDisabled(True)
        self.popularize_weekly_list()
        self.tableViewDaily.setColumnHidden(0, True)

    # VIEWS

    def popularize_weekly_list(self):
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

        date_1 = datetime.strptime(thisWeeksSunday, '%Y-%m-%d')

        self.sun = (date_1 + timedelta(days=0)).strftime("%B %d")
        self.mon = (date_1 + timedelta(days=1)).strftime("%B %d")
        self.tue = (date_1 + timedelta(days=2)).strftime("%B %d")
        self.wed = (date_1 + timedelta(days=3)).strftime("%B %d")
        self.thu = (date_1 + timedelta(days=4)).strftime("%B %d")
        self.fri = (date_1 + timedelta(days=5)).strftime("%B %d")
        self.sat = (date_1 + timedelta(days=6)).strftime("%B %d")

        self.labelSunday.setText(self.sun)
        self.labelMonday.setText(self.mon)
        self.labelTuesday.setText(self.tue)
        self.labelWednesday.setText(self.wed)
        self.labelThursday.setText(self.thu)
        self.labelFriday.setText(self.fri)
        self.labelSaturday.setText(self.sat)
        self.popularize_weekly_list()
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
        for item in self.database_tags:
            self.comboModifyEventTagsAdd.addItem(item[1])
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
        current_tags = []
        for column in range(self.tableModifyEventTags.columnCount()):
            item = self.tableModifyEventTags.item(0, column)
            if item is not None:
                current_tags.append(item)
        for item in self.database_tags:
            for tags in current_tags:
                if item == tags:
                    pass
                else:
                    self.comboModifyEventTagsAdd.addItem(item[1])

        self.set_event_defaults()
        selected_row = self.tableViewDaily.selectedItems()
        if len(selected_row) < 1:
            return
        self.stackedWidgetViews.setCurrentIndex(1)
        self.edit_flag = 1
        table = self.tableViewDaily
        row_number = self.tableViewDaily.row(selected_row[0])

        self.event_id = int(table.item(row_number, 0).text())
        tags_ids = self.connectDB.get_event_tags(self.event_id)
        tags = self.connectDB.get_tags(tags_ids)

        column_count = 1
        column_number = 0
        for tag in tags:
            self.tableModifyEventTags.setColumnCount(column_count)
            self.tableModifyEventTags.setItem(
                0, column_number, QTableWidgetItem(tag))
            column_number += 1
            column_count += 1

        # when selecting an item on the QTableWidget it'll edit the events that you clicked
        cur = self.connectDB.conn.cursor()
        sql = """SELECT * FROM events WHERE event_id = ?"""
        values = (self.event_id, )

        for item in cur.execute(sql, values):
            self.dataModifyEventTitle.setText(item[1])
            self.dataModifyEventDescription.setText(item[2])
            self.dataModifyEventStatus.setValue(item[5])

    def delete_event(self):
        if len(self.tableViewDaily.selectedItems()) > 0:
            row = self.tableViewDaily.currentRow()
            event_id = self.tableViewDaily.item(row, 0).text()
            try:
                self.connectDB.delete_event(event_id)
            except Error as e:
                print(e)
                return
            self.tableViewDaily.removeRow(row)

    def event_manager(self):
        if self.edit_flag == 0:
            self.connectDB.create_event(self.get_event_data())
        elif self.edit_flag == 1:
            self.connectDB.update_event(self.get_event_data())
        self.set_event_defaults()
        self.populate_daily()

    def add_event_tag(self):
        current_tags = []
        for column in range(self.tableModifyEventTags.columnCount()):
            item = self.tableModifyEventTags.item(0, column)
            if item is not None:
                current_tags.append(item)
        tag = self.comboModifyEventTagsAdd.currentText()
        if tag == "":
            return
        for tags in current_tags:
            if tag == tags:
                break

        item = QTableWidgetItem(tag)
        self.comboModifyEventTagsAdd.removeItem(self.comboModifyEventTagsAdd.findText(tag))
        self.tableModifyEventTags.setColumnCount(self.tableModifyEventTags.columnCount() + 1)
        self.tableModifyEventTags.setItem(0, self.tableModifyEventTags.columnCount() - 1, item)
        self.comboModifyEventTagsAdd.setCurrentText("")

    def delete_event_tag(self):
        current_tags = []
        for column in range(self.tableModifyEventTags.columnCount()):
            item = self.tableModifyEventTags.item(0, column)
            if item is not None:
                current_tags.append(item)
        if self.tableModifyEventTags.selectedItems():
            selected_item = self.tableModifyEventTags.selectedItems()[0]
            tag = selected_item.text()
            for tags in current_tags:
                if tag == tags:
                    return
            self.tableModifyEventTags.removeColumn(selected_item.column())
            self.comboModifyEventTagsAdd.addItem(tag)

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
        sunday = datetime.strptime(thisWeeksSunday, "%Y-%m-%d")

        return sunday

    def select_date(self):
        self.selected_date = self.calendarWidget.selectedDate()
        self.selected_date = str(self.selected_date.year(
        )) + '-'+str(self.selected_date.month())+'-'+str(self.selected_date.day())

    def set_event_defaults(self):
        self.dataModifyEventTitle.clear()
        self.dataModifyEventDescription.clear()
        self.dataModifyEventStartDate.clear()
        self.dataModifyEventEndDate.clear()
        self.dataModifyEventStatus.setValue(0)
        self.comboModifyEventTagsAdd.clear()
        self.tableModifyEventTags.clear()
        self.tableModifyEventTags.setColumnCount(0)
        self.tableModifyEventTags.setRowCount(1)
        self.comboModifyEventTagsAdd.addItem("")

    def get_event_data(self):
        current_tags = []
        for column in range(self.tableModifyEventTags.columnCount()):
            item = self.tableModifyEventTags.item(0, column)
            if item is not None:
                current_tags.append(item.text())
        data = {
            "event_id": self.event_id,
            "title": self.dataModifyEventTitle.text(),
            # "tags": self.dataModifyEventTags.text(),
            "description": self.dataModifyEventDescription.toPlainText(),
            "start_date": self.dataModifyEventStartDate.text(),
            "end_date": self.dataModifyEventEndDate.text(),
            "completion_status": self.dataModifyEventStatus.value()
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

        date_list = [self.sun_list, self.mon_list, self.tue_list,
                     self.wed_list, self.thu_list, self.fri_list, self.sat_list]
        table_list = [self.tableviewSunday, self.tableviewMonday, self.tableviewTuesday,
                      self.tableviewWednesday, self.tableviewThursday, self.tableviewFriday, self.tableviewSaturday]

        for i in range(0, 7):
            row_count = 1
            tablerow = 0
            for alist in date_list[i]:
                table_list[i].setRowCount(row_count)
                table_list[i].setItem(
                    tablerow, 0, QTableWidgetItem(alist['title']))
                table_list[i].setItem(
                    tablerow, 1, QTableWidgetItem(self.format_completion_status(alist['completion_status'])))
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
        self.tableViewDaily.setRowCount(0)

        # Grab data from database and populate qLineEdit boxes
        cur = self.connectDB.conn.cursor()
        query = """SELECT * FROM events where date(end_date) = ?"""
        params = (dateSelected.toString("yyyy-MM-dd"), )
        row_count = 1
        tablerow = 0
        for row in cur.execute(query, params):
            if row is not None:
                self.tableViewDaily.setRowCount(row_count)
                # event_id - hidden
                self.tableViewDaily.setItem(
                    tablerow, 0, QTableWidgetItem(str(row[0])))
                # title
                self.tableViewDaily.setItem(
                    tablerow, 1, QTableWidgetItem(row[1]))
                # start date
                self.tableViewDaily.setItem(
                    tablerow, 3, QTableWidgetItem(row[4]))
                # completion
                self.tableViewDaily.setItem(
                    tablerow, 4, QTableWidgetItem(self.format_completion_status(row[5])))
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
