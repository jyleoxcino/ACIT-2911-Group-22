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
            self.connectDB.dataInsert(data)
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

    
sql = """insert into note(description,begin_date,end_date,completion_status,title) values(?,?,?)""", (description,title,start_date,end_date,status)