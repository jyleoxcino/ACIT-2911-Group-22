import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import timedelta

class DayWidget(QWidget):
    def __init__(self, data):
        super().__init__()

        if data is None:
            self.data = None
        else:
            self.data = data

        # completion status == 1, label is green, label is red
        # if "schedule_id" color is blue
        
        # if "event_id" in self.data.keys():
        #     self.id = self.data["event_id"]
        #     self.completion_status = self.data["completion_status"]

        frame = QFrame()
        layout = QGridLayout(frame)
        self.setLayout(layout)
        layout.setSpacing(0)
        
        self.labelDay = QLabel(str(data['date']))
        self.categoryLabel = QLabel("")
        self.categoryLabel.setAlignment(Qt.AlignCenter)
    
        event_data = ["test", "test1", "test2", "test3", "test4"]

        layout.addWidget(self.labelDay, 0, 0, 1, 2)
        layout.addWidget(self.categoryLabel, 0, 1, 1, 2)
        for i in range(5):
            layout.addWidget(QPushButton(event_data[i]), i + 1, 0, 1, 3)

class CustomCalendarWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.current_date = datetime.datetime.now()

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        self.layoutUpper = QHBoxLayout()
        # self.layoutUpper.setStretchFactor(stretch=20)
        self.layoutMiddle = QHBoxLayout()
        # self.layoutMiddle.setStretchFactor(stretch=20)
        
        self.buttonNextMonth = QPushButton("Next")
        self.buttonPreviousMonth = QPushButton("Prev")
        self.labelMonth = QLabel(self.current_date.strftime("%B %Y"))
        
        self.buttonNextMonth.clicked.connect(self.next_month)
        self.buttonPreviousMonth.clicked.connect(self.previous_month)
        self.layoutUpper.addWidget(self.buttonPreviousMonth)
        self.layoutUpper.addWidget(self.labelMonth)
        self.layoutUpper.addWidget(self.buttonNextMonth)
        
        self.main_layout.addLayout(self.layoutUpper)
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        for day in days:
            self.layoutMiddle.addWidget(QLabel(day))
            
        self.main_layout.addLayout(self.layoutMiddle)
        self.labelMonth.setAlignment(Qt.AlignCenter)

        self.days_layout = QGridLayout()
        self.main_layout.addLayout(self.days_layout)

        self.set_defaults()
     
    def set_defaults(self):
        self.get_month()
        self.first = self.calculate_first()
        self.day_of_week = self.calculate_day()
        self.start_date = self.calculate_start()
        self.populate_days()
       
    def next_month(self):
        self.current_date = self.current_date + timedelta(days=30)
        self.clear_days()
        self.set_defaults()
    
    def previous_month(self):
        self.current_date = self.current_date - timedelta(days=30)
        self.clear_days()
        self.set_defaults()
        
    def populate_days(self):
        day = self.start_date
        for row in range(6):
            for column in range(7):
                data = {
                    "date": day.strftime("%B %d"),
                    "data": None
                }
                # dayitem = row * 7 + column + 1
                dayWidget = DayWidget(data)
                self.days_layout.addWidget(dayWidget, row, column)
                day = day + timedelta(days=1)
    
    def clear_days(self):
        for i in reversed(range(self.days_layout.count())):
            item = self.days_layout.itemAt(i)
            item.widget().close()
    
    def get_data(self):
        pass

    def get_month(self):
        self.labelMonth.setText(self.current_date.strftime("%B %Y"))

    def calculate_first(self):
        return self.current_date.replace(day=1)
    
    def calculate_day(self):
        return self.current_date.weekday()
    
    def calculate_start(self):
        return self.first - timedelta(days=self.day_of_week)