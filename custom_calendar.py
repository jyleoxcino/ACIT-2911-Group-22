import datetime
from db_controller import Database_Controller
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import timedelta


class DayWidget(QWidget):
    signal = pyqtSignal(object)

    def __init__(self, data, parent=None):
        super().__init__()

        if data is None:
            self.data = None
        else:
            self.data = data

        frame = QFrame()
        layout = QGridLayout(frame)
        self.setLayout(layout)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)

        self.labelDay = QLabel(data['date'].strftime("%B %d"))
        self.categoryLabel = QLabel("")
        self.categoryLabel.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.labelDay, 0, 0, 1, 2)
        layout.addWidget(self.categoryLabel, 0, 1, 1, 2)

        i = 0
        for item in self.data['data']:
            event_id = item[0]
            listing = QPushButton(item[1])
            listing.setFont(QFont('Arial', 8))
            layout.addWidget(listing, i + 1, 0, 1, 3)
            listing.clicked.connect(
                lambda checked, event_id=event_id: self.clicked_event(event_id))
            i += 1

    def clicked_event(self, listing_id):
        self.signal.emit(listing_id)


class CustomCalendarWidget(QWidget):
    signal = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__()

        self.db_connection = Database_Controller()
        self.current_date = datetime.datetime.now()

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        self.layoutUpper = QHBoxLayout()
        self.main_layout.setStretchFactor(self.layoutUpper, 20)
        self.layoutMiddle = QHBoxLayout()
        self.main_layout.setStretchFactor(self.layoutMiddle, 20)

        self.buttonNextMonth = QPushButton("Next")
        self.buttonPreviousMonth = QPushButton("Prev")
        self.labelMonth = QLabel(self.current_date.strftime("%B %Y"))

        self.buttonNextMonth.clicked.connect(self.next_month)
        self.buttonPreviousMonth.clicked.connect(self.previous_month)
        self.layoutUpper.addWidget(self.buttonPreviousMonth)
        self.layoutUpper.addWidget(self.labelMonth)
        self.layoutUpper.addWidget(self.buttonNextMonth)

        self.main_layout.addLayout(self.layoutUpper)
        days = ["Sunday", "Monday", "Tuesday",
                "Wednesday", "Thursday", "Friday", "Saturday"]
        for day in days:
            self.layoutMiddle.addWidget(QLabel(day))

        self.main_layout.addLayout(self.layoutMiddle)
        self.labelMonth.setAlignment(Qt.AlignCenter)

        self.days_layout = QGridLayout()
        self.main_layout.addLayout(self.days_layout)
        self.main_layout.setStretchFactor(self.days_layout, 60)

        self.set_defaults()

    def set_defaults(self):
        self.clear_days()
        self.get_month()
        self.first = self.calculate_first()
        self.day_of_week = self.calculate_day()
        self.start_date = self.calculate_start()
        self.populate_days()

    def next_month(self):
        self.current_date = self.current_date + timedelta(days=30)
        self.set_defaults()

    def previous_month(self):
        self.current_date = self.current_date - timedelta(days=30)
        self.set_defaults()

    def populate_days(self):
        date = self.start_date
        for row in range(5):
            for column in range(7):
                listings = self.db_connection.get_date_listing(date)
                data = {
                    "date": date,
                    "data": listings
                }
                dayWidget = DayWidget(data, parent=self)
                self.days_layout.addWidget(dayWidget, row, column)
                date = date + timedelta(days=1)
                dayWidget.signal.connect(self.test_emit)

    def test_emit(self, listing):
        self.signal.emit(listing)

    def clear_days(self):
        for i in reversed(range(self.days_layout.count())):
            item = self.days_layout.itemAt(i)
            item.widget().close()

    def get_month(self):
        self.labelMonth.setText(self.current_date.strftime("%B %Y"))

    def calculate_first(self):
        return self.current_date.replace(day=1)

    def calculate_day(self):
        return self.current_date.weekday()

    def calculate_start(self):
        return self.first - timedelta(days=self.day_of_week)
