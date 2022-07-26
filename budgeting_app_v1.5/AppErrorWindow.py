# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'budgeting_app_error_confirmation.ui'
#
# Created by: PyQt5 UI code generator 5.9.2

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import ctypes

class Ui_ErrorWindow(object):
    def setup(self, MainWindow):
         # Get maximum sizing of window
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [screen_width, screen_height] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        self.useable_rect = [screen_width, screen_height]
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.useable_rect[0] * 0.3, self.useable_rect[1] * 0.2)
        self.sub_size = MainWindow.size()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("error_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, self.sub_size.width() * 0.8, self.sub_size.height() / 3))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QLabel(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, (self.sub_size.height() / 3) + 30, self.sub_size.width() * 0.8, self.sub_size.height() / 3))
        font.setPointSize(12)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "News of your failure is....disturbing"))
        self.label.setText(_translate("MainWindow", "An error has occurred:"))
       

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_ErrorWindow()
    ui.setup(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

