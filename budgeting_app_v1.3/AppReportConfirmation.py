# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'budgeting_app_report_confirmation.ui'
#


from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess
import sys

class Ui_ConfirmationWindow(object):
    def setup_confirmation_window(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(444, 212)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("success_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 60, 231, 81))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.open_report_push_button = QtWidgets.QPushButton(self.centralwidget)
        self.open_report_push_button.setGeometry(QtCore.QRect(260, 60, 171, 81))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.open_report_push_button.setFont(font)
        self.open_report_push_button.setObjectName("open_report_push_button")
        self.open_report_push_button.clicked.connect(self.open_report)
        font = QtGui.QFont()
        font.setPointSize(14)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Report Successfully Generated!"))
        self.label.setText(_translate("MainWindow", "Report Generated:"))
        self.open_report_push_button.setText(_translate("MainWindow", "Open Report"))

    def open_report(self):
        try:
            subprocess.Popen(['budget_report.pdf'], shell = True)
        except:
            string = 'nothing happens' # Placeholder string, should never be used

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_ConfirmationWindow()
    ui.setup_confirmation_window(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

