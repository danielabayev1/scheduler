import sys
from db_handler import *
from PyQt5 import QtCore, QtGui, QtWidgets

TIME_SLOTS = 19
DAY_SLOTS = 7
HOUR_MAPPING = {}


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, db_manager):
        self.db_manager = db_manager
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1122, 798)

        # creating table
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(80, 150, 961, 471))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(DAY_SLOTS)
        self.tableWidget.setRowCount(TIME_SLOTS)
        for i in range(TIME_SLOTS):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(i, item)
        for i in range(DAY_SLOTS):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)

        # creating Title
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(450, 30, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")

        # creating menu bar
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1122, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName('actionSave')
        self.actiontoday_s_schedule = QtWidgets.QAction(MainWindow)
        self.actiontoday_s_schedule.setObjectName("actiontoday_s_schedule")
        self.action7_days_schedule = QtWidgets.QAction(MainWindow)
        self.action7_days_schedule.setObjectName("action7_days_schedule")
        self.menuView.addAction(self.actiontoday_s_schedule)
        self.menuView.addAction(self.action7_days_schedule)
        self.menuFile.addAction(self.actionSave)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.actionSave.triggered.connect(self.save)

    def save(self):
        for i in range(TIME_SLOTS):
            for j in range(DAY_SLOTS):
                activity = self.tableWidget.item(i, j)
                if activity is not None:

                    day_number = int((date.today() - DBManager.INITIAL_DATE).days) + j
                    hour = HOUR_MAPPING[i]
                    print(day_number, hour)
                    if (i, j) in self.in_db:
                        # update
                        if activity.text().strip() != '':
                            self.db_manager.update_activity((day_number, hour, activity.text()))
                        else:
                            self.db_manager.delete_activity((day_number, hour))
                    else:
                        # insert
                        self.db_manager.insert_activity((day_number, hour, activity.text()))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        # formatting 'time' rows
        first_hour = 6
        for i in range(TIME_SLOTS):
            item = self.tableWidget.verticalHeaderItem(i)
            item.setText(_translate("MainWindow", HOUR_MAPPING[i]))

        # formatting 'day' columns
        for i in range(DAY_SLOTS):
            cur_day = (date.today() + timedelta(i))
            item = self.tableWidget.horizontalHeaderItem(i)
            item.setText(_translate("MainWindow", f'{cur_day.strftime("%d.%m.%y")}\n{cur_day.strftime("%A")}'))

        self.load_curr_week_schedule()

        self.label.setText(_translate("MainWindow", "My Schedule"))

        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.actionSave.setText(_translate("MainWindow", "save"))
        self.actiontoday_s_schedule.setText(_translate("MainWindow", "today\'s schedule"))
        self.action7_days_schedule.setText(_translate("MainWindow", "weekly schedule"))

    def load_curr_week_schedule(self):
        today = (date.today() - DBManager.INITIAL_DATE).days
        curr_week_activites = self.db_manager.get_this_week_data()
        self.in_db = []
        for activity in curr_week_activites:
            day_col = activity[DBManager.DATE] - today
            hour_row = list(HOUR_MAPPING.keys())[list(HOUR_MAPPING.values()).index(activity[DBManager.HOUR])]
            self.in_db.append((hour_row, day_col))
            self.tableWidget.setItem(hour_row, day_col, QtWidgets.QTableWidgetItem(activity[DBManager.ACTIVITY]))


def load_hour_mapping():
    for i in range(TIME_SLOTS):
        if i == TIME_SLOTS - 1:
            HOUR_MAPPING[i] = f'00:00'
        elif i < 4:
            HOUR_MAPPING[i] = f'0{i + 6}:00'
        else:
            HOUR_MAPPING[i] = f'{i + 6}:00'


def shell_daily_schedule(db_manager):
    curr_week_activites = db_manager.get_this_day_data()
    for activity in curr_week_activites:
        print(activity[DBManager.HOUR], activity[DBManager.ACTIVITY])


# todo work on edge cases
if __name__ == "__main__":
    load_hour_mapping()
    db_manager = DBManager()
    if sys.argv[1] == "gui":
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow, db_manager)
        MainWindow.show()
        sys.exit(app.exec_())
    elif sys.argv[1] == "shell":
        shell_daily_schedule(db_manager)
