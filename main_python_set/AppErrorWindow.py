# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'budgeting_app_error_confirmation.ui'
#
# Created by: PyQt5 UI code generator 5.9.2


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ErrorWindow(object):
    def setup(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 146)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("error_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 211, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QLabel(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 50, 500, 71))
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

