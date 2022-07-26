"""
Created on Tue May 11 08:54:30 2021

@author: Baskaryll
Functionality - Create an instance of the budget app
"""
import sys
import inspect
import os

# Set the current working directory to that containing the callBudgetingApp.py (this) file
# Done Prior to importing further modules
module_path = inspect.getfile(inspect.currentframe())
module_dir = os.path.realpath(os.path.dirname(module_path))
os.chdir(module_dir)

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from MainAppFunctionality import *
from AppErrorWindow import *
from AppReportConfirmation import *

# Create the form class for a specific GUI instance
class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_BudgetOverview()
        self.ui.setupUi(self)
        self.show()
  
# Initialize an instance of the budget GUI
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    budget_overview = QtWidgets.QMainWindow()
    ui = Ui_BudgetOverview()
    ui.setupUi(budget_overview)
    budget_overview.show()
    sys.exit(app.exec_())

