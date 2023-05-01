import sys
import sqlite3
import datetime
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi

"""""
Event Properties
- Title         STRING
- Description   STRING
- Tags          STRING?
- Start Date    DATE/TIME
- Due Date      DATE/TIME
- Complete      BOOLEAN

"""""

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loadUi("untitled.ui", self)
    
    def edit_note(self):
        pass
    
    def create_event(self):
        pass
    
    def update_event(self):
        pass
    
    def delete_event(self):
        pass
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Main()
    ui.show()
    app.exec_()