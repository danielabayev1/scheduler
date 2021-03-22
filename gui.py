from PyQt5 import QtCore, QtGui, QtWidgets

TIME_SLOTS = 19
DAY_SLOTS = 7
DAY_LIST = ['Sunday', 'Monday', 'Tuesday', "Wednesday", 'Thursday', 'Friday', 'Saturday']


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
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
        self.menuSave = QtWidgets.QMenu(self.menubar)
        self.menuSave.setObjectName("menuSave")
        self.menuview = QtWidgets.QMenu(self.menubar)
        self.menuview.setObjectName("menuview")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actiontoday_s_schedule = QtWidgets.QAction(MainWindow)
        self.actiontoday_s_schedule.setObjectName("actiontoday_s_schedule")
        self.action7_days_schedule = QtWidgets.QAction(MainWindow)
        self.action7_days_schedule.setObjectName("action7_days_schedule")
        self.menuview.addAction(self.actiontoday_s_schedule)
        self.menuview.addAction(self.action7_days_schedule)
        self.menubar.addAction(self.menuSave.menuAction())
        self.menubar.addAction(self.menuview.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        first_hour = 6
        for i in range(TIME_SLOTS):
            item = self.tableWidget.verticalHeaderItem(i)
            current_hour = first_hour + i
            if current_hour == 24:
                item.setText(_translate("MainWindow", "00:00"))
            elif current_hour > 9:
                item.setText(_translate("MainWindow", f"{current_hour}:00"))
            else:
                item.setText(_translate("MainWindow", f"0{current_hour}:00"))
        for i in range(DAY_SLOTS):
            item = self.tableWidget.horizontalHeaderItem(i)
            item.setText(_translate("MainWindow", DAY_LIST[i]))

        self.label.setText(_translate("MainWindow", "My Schedule"))

        self.menuSave.setTitle(_translate("MainWindow", "Save"))
        self.menuview.setTitle(_translate("MainWindow", "view"))
        self.actiontoday_s_schedule.setText(_translate("MainWindow", "today\'s schedule"))
        self.action7_days_schedule.setText(_translate("MainWindow", "weekly schedule"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
