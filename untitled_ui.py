# Form implementation generated from reading ui file 'c:\Users\Jyle\Desktop\ACIT-2911-Group-22\untitled.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_StudyBuddy(object):
    def setupUi(self, StudyBuddy):
        StudyBuddy.setObjectName("StudyBuddy")
        StudyBuddy.resize(1575, 859)
        self.centralwidget = QtWidgets.QWidget(parent=StudyBuddy)
        self.centralwidget.setStyleSheet("QWidget{\n"
"  font-family: -apple-system,system-ui,\"Segoe UI\",\"Liberation Sans\",sans-serif;\n"
"\n"
"\n"
"}\n"
".QPushButton {\n"
"  background-color: #e1ecf4;\n"
"  border-radius: 3px;\n"
"  border: 1px solid #7aa7c7;\n"
"  color: #39739d;\n"
"  font-size: 15px;\n"
"  font-weight: 400;\n"
"  margin: 0;\n"
"  outline: none;\n"
"  padding: 8px .8em;\n"
"}\n"
"\n"
".QLabel{\n"
"    font-size: 17px;\n"
"    font-weight: bold;\n"
"    color: #2b5777\n"
"}\n"
"\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.navigationFrame = QtWidgets.QFrame(parent=self.centralwidget)
        self.navigationFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.navigationFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.navigationFrame.setObjectName("navigationFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.navigationFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.navigationFrame1 = QtWidgets.QFrame(parent=self.navigationFrame)
        self.navigationFrame1.setMinimumSize(QtCore.QSize(0, 250))
        self.navigationFrame1.setStyleSheet("QPushButton:disabled {\n"
"\n"
"    font-weight:bold;\n"
"    color:white;\n"
"    background-color: #2b5777;\n"
"}")
        self.navigationFrame1.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.navigationFrame1.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.navigationFrame1.setObjectName("navigationFrame1")
        self.labelCalendar = QtWidgets.QLabel(parent=self.navigationFrame1)
        self.labelCalendar.setGeometry(QtCore.QRect(0, 0, 71, 31))
        self.labelCalendar.setObjectName("labelCalendar")
        self.buttonDay = QtWidgets.QPushButton(parent=self.navigationFrame1)
        self.buttonDay.setGeometry(QtCore.QRect(0, 40, 101, 51))
        self.buttonDay.setStyleSheet("")
        self.buttonDay.setObjectName("buttonDay")
        self.buttonWeek = QtWidgets.QPushButton(parent=self.navigationFrame1)
        self.buttonWeek.setGeometry(QtCore.QRect(0, 100, 101, 51))
        self.buttonWeek.setObjectName("buttonWeek")
        self.buttonMonth = QtWidgets.QPushButton(parent=self.navigationFrame1)
        self.buttonMonth.setGeometry(QtCore.QRect(0, 160, 101, 51))
        self.buttonMonth.setObjectName("buttonMonth")
        self.verticalLayout.addWidget(self.navigationFrame1)
        self.navigationFrame3 = QtWidgets.QFrame(parent=self.navigationFrame)
        self.navigationFrame3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.navigationFrame3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.navigationFrame3.setObjectName("navigationFrame3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.navigationFrame3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_2 = QtWidgets.QLabel(parent=self.navigationFrame3)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom|QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_5.addWidget(self.label_2)
        self.pushButton_8 = QtWidgets.QPushButton(parent=self.navigationFrame3)
        self.pushButton_8.setObjectName("pushButton_8")
        self.verticalLayout_5.addWidget(self.pushButton_8)
        self.verticalLayout.addWidget(self.navigationFrame3)
        self.horizontalLayout_2.addWidget(self.navigationFrame)
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.centralwidget)
        self.stackedWidget.setMinimumSize(QtCore.QSize(0, 575))
        self.stackedWidget.setStyleSheet("")
        self.stackedWidget.setObjectName("stackedWidget")
        self.monthPage = QtWidgets.QWidget()
        self.monthPage.setStyleSheet("")
        self.monthPage.setObjectName("monthPage")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.monthPage)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.calendarWidget = QtWidgets.QCalendarWidget(parent=self.monthPage)
        self.calendarWidget.setMinimumSize(QtCore.QSize(391, 0))
        font = QtGui.QFont()
        font.setFamily("-apple-system")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.calendarWidget.setFont(font)
        self.calendarWidget.setStyleSheet("QCalendarWidget QAbstractItemView\n"
"{ \n"
"selection-background-color: #042944; \n"
"selection-color: white;\n"
"selection-border:10px solid red;\n"
"font-size: 16px;\n"
"\n"
"}\n"
"QCalendarWidget QTableView{\n"
"background-color:lightblue;\n"
"}\n"
"")
        self.calendarWidget.setGridVisible(True)
        self.calendarWidget.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendarWidget.setObjectName("calendarWidget")
        self.horizontalLayout.addWidget(self.calendarWidget)
        self.frame = QtWidgets.QFrame(parent=self.monthPage)
        self.frame.setMinimumSize(QtCore.QSize(0, 0))
        self.frame.setMaximumSize(QtCore.QSize(400, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(parent=self.frame)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.listView = QtWidgets.QListView(parent=self.frame)
        self.listView.setMinimumSize(QtCore.QSize(0, 0))
        self.listView.setObjectName("listView")
        self.verticalLayout_2.addWidget(self.listView)
        self.horizontalLayout.addWidget(self.frame)
        self.stackedWidget.addWidget(self.monthPage)
        self.editPage = QtWidgets.QWidget()
        self.editPage.setObjectName("editPage")
        self.labelTitle = QtWidgets.QLabel(parent=self.editPage)
        self.labelTitle.setGeometry(QtCore.QRect(0, 30, 55, 16))
        self.labelTitle.setObjectName("labelTitle")
        self.lineEditTitle = QtWidgets.QLineEdit(parent=self.editPage)
        self.lineEditTitle.setGeometry(QtCore.QRect(0, 50, 690, 22))
        self.lineEditTitle.setObjectName("lineEditTitle")
        self.lineEditTags = QtWidgets.QLineEdit(parent=self.editPage)
        self.lineEditTags.setGeometry(QtCore.QRect(0, 100, 690, 22))
        self.lineEditTags.setObjectName("lineEditTags")
        self.labelTags = QtWidgets.QLabel(parent=self.editPage)
        self.labelTags.setGeometry(QtCore.QRect(0, 80, 55, 16))
        self.labelTags.setObjectName("labelTags")
        self.labelStartDate = QtWidgets.QLabel(parent=self.editPage)
        self.labelStartDate.setGeometry(QtCore.QRect(0, 130, 91, 16))
        self.labelStartDate.setObjectName("labelStartDate")
        self.dateEdit = QtWidgets.QDateEdit(parent=self.editPage)
        self.dateEdit.setGeometry(QtCore.QRect(0, 150, 110, 22))
        self.dateEdit.setObjectName("dateEdit")
        self.labelEndDate = QtWidgets.QLabel(parent=self.editPage)
        self.labelEndDate.setGeometry(QtCore.QRect(130, 130, 101, 16))
        self.labelEndDate.setObjectName("labelEndDate")
        self.dateEdit_2 = QtWidgets.QDateEdit(parent=self.editPage)
        self.dateEdit_2.setGeometry(QtCore.QRect(130, 150, 110, 22))
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.horizontalSlider = QtWidgets.QSlider(parent=self.editPage)
        self.horizontalSlider.setGeometry(QtCore.QRect(630, 150, 51, 22))
        self.horizontalSlider.setMaximum(1)
        self.horizontalSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.labelStatus = QtWidgets.QLabel(parent=self.editPage)
        self.labelStatus.setGeometry(QtCore.QRect(630, 130, 55, 16))
        self.labelStatus.setObjectName("labelStatus")
        self.labelDescription = QtWidgets.QLabel(parent=self.editPage)
        self.labelDescription.setGeometry(QtCore.QRect(0, 190, 131, 16))
        self.labelDescription.setObjectName("labelDescription")
        self.buttonCancel = QtWidgets.QPushButton(parent=self.editPage)
        self.buttonCancel.setGeometry(QtCore.QRect(0, 500, 90, 30))
        self.buttonCancel.setObjectName("buttonCancel")
        self.buttonSubmit = QtWidgets.QPushButton(parent=self.editPage)
        self.buttonSubmit.setGeometry(QtCore.QRect(600, 500, 90, 30))
        self.buttonSubmit.setObjectName("buttonSubmit")
        self.labelDate = QtWidgets.QLabel(parent=self.editPage)
        self.labelDate.setGeometry(QtCore.QRect(320, 10, 101, 21))
        self.labelDate.setObjectName("labelDate")
        self.textEdit = QtWidgets.QTextEdit(parent=self.editPage)
        self.textEdit.setGeometry(QtCore.QRect(0, 230, 691, 251))
        self.textEdit.setObjectName("textEdit")
        self.stackedWidget.addWidget(self.editPage)
        self.dayPage = QtWidgets.QWidget()
        self.dayPage.setObjectName("dayPage")
        self.tableWidget = QtWidgets.QTableWidget(parent=self.dayPage)
        self.tableWidget.setGeometry(QtCore.QRect(0, 70, 690, 451))
        self.tableWidget.setStyleSheet("")
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.buttonCancel_2 = QtWidgets.QPushButton(parent=self.dayPage)
        self.buttonCancel_2.setGeometry(QtCore.QRect(600, 530, 90, 30))
        self.buttonCancel_2.setObjectName("buttonCancel_2")
        self.labelDate_2 = QtWidgets.QLabel(parent=self.dayPage)
        self.labelDate_2.setGeometry(QtCore.QRect(320, 10, 141, 16))
        self.labelDate_2.setObjectName("labelDate_2")
        self.pushButton = QtWidgets.QPushButton(parent=self.dayPage)
        self.pushButton.setGeometry(QtCore.QRect(600, 30, 90, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.dayPage)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 30, 90, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.dayPage)
        self.pushButton_3.setGeometry(QtCore.QRect(100, 30, 90, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.stackedWidget.addWidget(self.dayPage)
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.page)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.labelMonth = QtWidgets.QLabel(parent=self.page)
        self.labelMonth.setObjectName("labelMonth")
        self.gridLayout_2.addWidget(self.labelMonth, 0, 3, 1, 3)
        self.labelSunday = QtWidgets.QLabel(parent=self.page)
        self.labelSunday.setObjectName("labelSunday")
        self.gridLayout_2.addWidget(self.labelSunday, 1, 0, 1, 1)
        self.labelMonday = QtWidgets.QLabel(parent=self.page)
        self.labelMonday.setObjectName("labelMonday")
        self.gridLayout_2.addWidget(self.labelMonday, 1, 1, 1, 1)
        self.labelTuesday = QtWidgets.QLabel(parent=self.page)
        self.labelTuesday.setObjectName("labelTuesday")
        self.gridLayout_2.addWidget(self.labelTuesday, 1, 2, 1, 1)
        self.labelWednesday = QtWidgets.QLabel(parent=self.page)
        self.labelWednesday.setObjectName("labelWednesday")
        self.gridLayout_2.addWidget(self.labelWednesday, 1, 3, 1, 1)
        self.labelThursday = QtWidgets.QLabel(parent=self.page)
        self.labelThursday.setObjectName("labelThursday")
        self.gridLayout_2.addWidget(self.labelThursday, 1, 4, 1, 1)
        self.labelFriday = QtWidgets.QLabel(parent=self.page)
        self.labelFriday.setObjectName("labelFriday")
        self.gridLayout_2.addWidget(self.labelFriday, 1, 5, 1, 1)
        self.labelSaturday = QtWidgets.QLabel(parent=self.page)
        self.labelSaturday.setObjectName("labelSaturday")
        self.gridLayout_2.addWidget(self.labelSaturday, 1, 6, 1, 1)
        self.buttonCancel_3 = QtWidgets.QPushButton(parent=self.page)
        self.buttonCancel_3.setObjectName("buttonCancel_3")
        self.gridLayout_2.addWidget(self.buttonCancel_3, 3, 6, 1, 1)
        self.tableviewSunday = QtWidgets.QTableWidget(parent=self.page)
        self.tableviewSunday.setObjectName("tableviewSunday")
        self.tableviewSunday.setColumnCount(2)
        self.tableviewSunday.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableviewSunday.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableviewSunday.setHorizontalHeaderItem(1, item)
        self.gridLayout_2.addWidget(self.tableviewSunday, 2, 0, 1, 1)
        self.tableviewMonday = QtWidgets.QTableWidget(parent=self.page)
        self.tableviewMonday.setObjectName("tableviewMonday")
        self.tableviewMonday.setColumnCount(2)
        self.tableviewMonday.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableviewMonday.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableviewMonday.setHorizontalHeaderItem(1, item)
        self.gridLayout_2.addWidget(self.tableviewMonday, 2, 1, 1, 1)
        self.tableviewTuesday = QtWidgets.QTableWidget(parent=self.page)
        self.tableviewTuesday.setObjectName("tableviewTuesday")
        self.tableviewTuesday.setColumnCount(2)
        self.tableviewTuesday.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableviewTuesday.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableviewTuesday.setHorizontalHeaderItem(1, item)
        self.gridLayout_2.addWidget(self.tableviewTuesday, 2, 2, 1, 1)
        self.tableviewWednesday = QtWidgets.QTableWidget(parent=self.page)
        self.tableviewWednesday.setObjectName("tableviewWednesday")
        self.tableviewWednesday.setColumnCount(2)
        self.tableviewWednesday.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableviewWednesday.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableviewWednesday.setHorizontalHeaderItem(1, item)
        self.gridLayout_2.addWidget(self.tableviewWednesday, 2, 3, 1, 1)
        self.tableviewThursday = QtWidgets.QTableWidget(parent=self.page)
        self.tableviewThursday.setObjectName("tableviewThursday")
        self.tableviewThursday.setColumnCount(2)
        self.tableviewThursday.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableviewThursday.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableviewThursday.setHorizontalHeaderItem(1, item)
        self.gridLayout_2.addWidget(self.tableviewThursday, 2, 4, 1, 1)
        self.tableviewFriday = QtWidgets.QTableWidget(parent=self.page)
        self.tableviewFriday.setObjectName("tableviewFriday")
        self.tableviewFriday.setColumnCount(2)
        self.tableviewFriday.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableviewFriday.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableviewFriday.setHorizontalHeaderItem(1, item)
        self.gridLayout_2.addWidget(self.tableviewFriday, 2, 5, 1, 1)
        self.tableviewSaturday = QtWidgets.QTableWidget(parent=self.page)
        self.tableviewSaturday.setObjectName("tableviewSaturday")
        self.tableviewSaturday.setColumnCount(2)
        self.tableviewSaturday.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableviewSaturday.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableviewSaturday.setHorizontalHeaderItem(1, item)
        self.gridLayout_2.addWidget(self.tableviewSaturday, 2, 6, 1, 1)
        self.stackedWidget.addWidget(self.page)
        self.horizontalLayout_2.addWidget(self.stackedWidget)
        StudyBuddy.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=StudyBuddy)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1575, 26))
        self.menubar.setObjectName("menubar")
        StudyBuddy.setMenuBar(self.menubar)
        self.actionExit = QtGui.QAction(parent=StudyBuddy)
        self.actionExit.setObjectName("actionExit")

        self.retranslateUi(StudyBuddy)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(StudyBuddy)

    def retranslateUi(self, StudyBuddy):
        _translate = QtCore.QCoreApplication.translate
        StudyBuddy.setWindowTitle(_translate("StudyBuddy", "StudyBuddy"))
        self.labelCalendar.setText(_translate("StudyBuddy", "Calendar"))
        self.buttonDay.setText(_translate("StudyBuddy", "Day"))
        self.buttonWeek.setText(_translate("StudyBuddy", "Week"))
        self.buttonMonth.setText(_translate("StudyBuddy", "Month"))
        self.label_2.setText(_translate("StudyBuddy", "Help"))
        self.pushButton_8.setText(_translate("StudyBuddy", "Settings"))
        self.label_3.setText(_translate("StudyBuddy", "Weekly View"))
        self.labelTitle.setText(_translate("StudyBuddy", "Title"))
        self.labelTags.setText(_translate("StudyBuddy", "Tags"))
        self.labelStartDate.setText(_translate("StudyBuddy", "Start Date"))
        self.labelEndDate.setText(_translate("StudyBuddy", "End Date"))
        self.labelStatus.setText(_translate("StudyBuddy", "Status"))
        self.labelDescription.setText(_translate("StudyBuddy", "Description"))
        self.buttonCancel.setText(_translate("StudyBuddy", "Cancel"))
        self.buttonSubmit.setText(_translate("StudyBuddy", "Submit"))
        self.labelDate.setText(_translate("StudyBuddy", "Date"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("StudyBuddy", "Title"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("StudyBuddy", "Tags"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("StudyBuddy", "End Date"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("StudyBuddy", "Status"))
        self.buttonCancel_2.setText(_translate("StudyBuddy", "Cancel"))
        self.labelDate_2.setText(_translate("StudyBuddy", "Date"))
        self.pushButton.setText(_translate("StudyBuddy", "Delete"))
        self.pushButton_2.setText(_translate("StudyBuddy", "Add"))
        self.pushButton_3.setText(_translate("StudyBuddy", "Edit"))
        self.labelMonth.setText(_translate("StudyBuddy", "Month # ~ Month #"))
        self.labelSunday.setText(_translate("StudyBuddy", "Sunday #"))
        self.labelMonday.setText(_translate("StudyBuddy", "Monday #"))
        self.labelTuesday.setText(_translate("StudyBuddy", "Tuesday #"))
        self.labelWednesday.setText(_translate("StudyBuddy", "Wednesday #"))
        self.labelThursday.setText(_translate("StudyBuddy", "Thursday #"))
        self.labelFriday.setText(_translate("StudyBuddy", "Friday #"))
        self.labelSaturday.setText(_translate("StudyBuddy", "Saturday #"))
        self.buttonCancel_3.setText(_translate("StudyBuddy", "Cancel"))
        item = self.tableviewSunday.horizontalHeaderItem(0)
        item.setText(_translate("StudyBuddy", "Title"))
        item = self.tableviewSunday.horizontalHeaderItem(1)
        item.setText(_translate("StudyBuddy", "Status"))
        item = self.tableviewMonday.horizontalHeaderItem(0)
        item.setText(_translate("StudyBuddy", "Title"))
        item = self.tableviewMonday.horizontalHeaderItem(1)
        item.setText(_translate("StudyBuddy", "Status"))
        item = self.tableviewTuesday.horizontalHeaderItem(0)
        item.setText(_translate("StudyBuddy", "Title"))
        item = self.tableviewTuesday.horizontalHeaderItem(1)
        item.setText(_translate("StudyBuddy", "Status"))
        item = self.tableviewWednesday.horizontalHeaderItem(0)
        item.setText(_translate("StudyBuddy", "Title"))
        item = self.tableviewWednesday.horizontalHeaderItem(1)
        item.setText(_translate("StudyBuddy", "Status"))
        item = self.tableviewThursday.horizontalHeaderItem(0)
        item.setText(_translate("StudyBuddy", "Title"))
        item = self.tableviewThursday.horizontalHeaderItem(1)
        item.setText(_translate("StudyBuddy", "Status"))
        item = self.tableviewFriday.horizontalHeaderItem(0)
        item.setText(_translate("StudyBuddy", "Title"))
        item = self.tableviewFriday.horizontalHeaderItem(1)
        item.setText(_translate("StudyBuddy", "Status"))
        item = self.tableviewSaturday.horizontalHeaderItem(0)
        item.setText(_translate("StudyBuddy", "Title"))
        item = self.tableviewSaturday.horizontalHeaderItem(1)
        item.setText(_translate("StudyBuddy", "Status"))
        self.actionExit.setText(_translate("StudyBuddy", "Exit"))
