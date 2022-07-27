"""
Author - Matthew Hughes
Date - 11/5/2021
Functionality - Creates a GUI for budget setup and analysis
                Generates a library and report from the info
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from AppErrorWindow import *
from AppReportConfirmation import *
from AppReportProduction import *
import json
import pandas as pd
import numpy as np
from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat, Table, VerticalSpace, HorizontalSpace
import matplotlib.pyplot as plt
from pylatex.utils import italic
import os
from pdflatex import PDFLaTeX
import sys
import ctypes
import openpyxl
from openpyxl.chart import LineChart, Reference

class Ui_BudgetOverview(object):
    
    def setupUi(self, BudgetOverview):
        
        # Get screen size information
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [screen_width, screen_height] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        self.useable_rect = [screen_width, screen_height]
        
        BudgetOverview.setObjectName("BudgetOverview")
        BudgetOverview.resize(self.useable_rect[0] * 0.4, self.useable_rect[1] * 0.55)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("main_app_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        BudgetOverview.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(BudgetOverview)
        self.centralwidget.setObjectName("centralwidget")
        
        # Add button functionality
        self.add_item_push_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_item_push_button.setGeometry(QtCore.QRect(10, 420, self.useable_rect[0] * 0.125, 71))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.add_item_push_button.setFont(font)
        self.add_item_push_button.setObjectName("add_item_push_button")
        self.remove_item_push_button = QtWidgets.QPushButton(self.centralwidget)
        self.remove_item_push_button.setGeometry(QtCore.QRect(self.useable_rect[0] * 0.13, 420, self.useable_rect[0] * 0.125, 71))
        self.add_item_push_button.clicked.connect(self.add_to_table)
        font = QtGui.QFont()
        font.setPointSize(18)
        
        # Add remove button functionality
        self.remove_item_push_button.setFont(font)
        self.remove_item_push_button.setObjectName("remove_item_push_button")
        self.generate_report_push_button = QtWidgets.QPushButton(self.centralwidget)
        self.generate_report_push_button.setGeometry(QtCore.QRect(2 * self.useable_rect[0] * 0.13, 410, self.useable_rect[0] * 0.13, 91))
        self.remove_item_push_button.clicked.connect(self.remove_from_table)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        
        # Add generate report button functionality
        self.generate_report_push_button.setFont(font)
        self.generate_report_push_button.setObjectName("generate_report_push_button")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 30, self.useable_rect[0] * 0.39, 371))
        self.generate_report_push_button.clicked.connect(self.generate_report)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.tableWidget.setFont(font)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        BudgetOverview.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(BudgetOverview)
        self.statusbar.setObjectName("statusbar")
        BudgetOverview.setStatusBar(self.statusbar)
        if os.path.exists('budget_text_doc.txt'):
            with open('budget_text_doc.txt', 'r+') as pre:
                pre_data = json.load(pre)
            
            row_count = (len(pre_data['Amount']))
            column_count = 3
            column_names = ['Category', 'Amount', 'Frequency']
            self.tableWidget.setRowCount(row_count)

            for row in range(row_count):  # add items from array to QTableWidget
                for column_name in column_names:
                    item = ((pre_data[column_name][row]))
                    if column_name == 'Category':
                        self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(item))
                    if column_name == 'Amount':
                        self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(item))
                    if column_name == 'Frequency':
                        self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(item))
        
        self.retranslateUi(BudgetOverview)
        QtCore.QMetaObject.connectSlotsByName(BudgetOverview)
        BudgetOverview.setTabOrder(self.add_item_push_button, self.remove_item_push_button)
        BudgetOverview.setTabOrder(self.remove_item_push_button, self.generate_report_push_button)
        BudgetOverview.setTabOrder(self.generate_report_push_button, self.tableWidget)

    def retranslateUi(self, BudgetOverview):
        _translate = QtCore.QCoreApplication.translate
        BudgetOverview.setWindowTitle(_translate("BudgetOverview", "Budget Report Generation"))
        self.add_item_push_button.setText(_translate("BudgetOverview", "Add Category"))
        self.remove_item_push_button.setText(_translate("BudgetOverview", "Remove Category"))
        self.generate_report_push_button.setText(_translate("BudgetOverview", "Generate Report"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("BudgetOverview", "Category"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("BudgetOverview", "Amount"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("BudgetOverview", "Frequency"))

    # An important function that pops-up varied error windows
    def show_error_window(self, message):
        self.Dialog = QtWidgets.QMainWindow()
        self.error_popup = Ui_ErrorWindow()
        self.error_popup.setup(self.Dialog)
        self.error_popup.textEdit.setText(message)
        self.Dialog.show()
    # The function for popping up a confirmation of success window
    
    def show_success_window(self):
        self.dialog_success = QtWidgets.QMainWindow()
        self.success_popup = Ui_ConfirmationWindow()
        self.success_popup.setup_confirmation_window(self.dialog_success)
        self.dialog_success.show()        
    
    # Add button function
    def add_to_table(self):
        self.tableWidget.insertRow(self.tableWidget.rowCount())
    
    # Remove button function
    def remove_from_table(self):
        row_index = self.tableWidget.currentRow()
        self.tableWidget.removeRow(row_index)
    
   #  Parts of the generate report function
    def generate_report(self):
        number_of_rows = self.tableWidget.rowCount()
        allowed_payment_periods = ['weekly', 'fortnightly', 'monthly', 'quarterly', 'yearly']
        
        # Create an empty dictionary to hold budget information
        budget_dictionary = {
            'Category': [],
            'Amount': [],
            'Frequency': [],
            }
        
        # First condition is if rows exist
        if number_of_rows > 0:
            # Test each cell for valid data
            error_flag = False
            duration_error_flag = False
            
            for row in range(number_of_rows):
                try:
                    # Extract each relevant value
                    current_category_text =[]
                    current_cost_text = []
                    current_period_text = []
                    current_category = self.tableWidget.item(row, 0)
                    current_category_text.append(current_category.text().lower())
                    current_cost = self.tableWidget.item(row, 1)
                    current_cost_text.append(float(current_cost.text()))
                    current_period = self.tableWidget.item(row, 2)
                    current_period_text.append(current_period.text().lower() in allowed_payment_periods)
                    
                except ValueError:
                    message = 'Make sure amount values are numbers throughout.'
                    self.show_error_window(message)
                    error_flag = True
                    
                except Exception as exception:
                    message = 'Unexpected Error: ' + str(exception)
                    self.show_error_window(message)
                    error_flag = True
         
            if False in current_period_text:
                duration_error_flag = True
            
            if duration_error_flag == False:
                # If rows exist attempt analysis
                if error_flag == False:
                    try:
                        current_cost_numerical = []
                        for row in range(number_of_rows):
                
                            # Use a try argument to test if the table is valid prior to analysis
                            # i.e. if amount of cost is a floatable number and if the period is in
                            # {weekly, fortnightly, monthly, quarterly, yearly}               
                            # Extract each relevant value
                            current_category = self.tableWidget.item(row, 0)
                            current_category_text = current_category.text().lower()
                            current_cost = self.tableWidget.item(row, 1)
                            current_cost_text = current_cost.text()
                            current_cost_numerical.append(float(current_cost.text()))
                            current_period = self.tableWidget.item(row, 2)
                            current_period_text = current_period.text().lower()
                            budget_dictionary['Category'].append(current_category_text)
                            budget_dictionary['Amount'].append(current_cost_text)
                            budget_dictionary['Frequency'].append(current_period_text)         
                        
                        # Order a little to test excel doc
                        d = {'weekly': 1, 'fortnightly': 1/2, 'monthly': 12/52, 'quarterly': 4/52, 'yearly': 1/52}
                        budget_table = pd.DataFrame(budget_dictionary)
                        duration_dictionary_adjusted = pd.Series(budget_dictionary['Frequency']).map(d)
                        adjusted_cost_numerical = round(pd.Series(current_cost_numerical)*duration_dictionary_adjusted, 2)
                        adjusted_budget_table = pd.DataFrame([budget_dictionary['Category'],
                                              budget_dictionary['Frequency'],
                                              adjusted_cost_numerical],
                                             ['Category', 'Frequency', 'Weekly Payment ($)'])
                        adjusted_budget_table = adjusted_budget_table.sort_values(by = ['Weekly Payment ($)'], axis = 1)
                        sum_total = sum(adjusted_cost_numerical)
                        sum_total_fortnightly = sum_total * 2
                        sum_total_monthly = round(sum_total * 52/12, 2)
                        total_costs = pd.DataFrame({'Weekly': [sum_total], 'Fortnightly': [sum_total_fortnightly], 'Monthly': [sum_total_monthly]})
                        transposed_budget_table = adjusted_budget_table.transpose() 
                        
                        # with pd.ExcelWriter('budgeting_report.xlsx', engine='xlsxwriter') as writer:
                        #     # total_costs.to_excel(writer, sheet_name = 'Total_Expenditure')
                        #     # transposed_budget_table.to_excel(writer, sheet_name = 'Costs_Breakdown')
            
                        #     # # Let us now plot a figure
                            
                        #     # # Point to the sheet 'Costs_Breakdown', where the chart will be added
                        #     # working_book = writer.book 
                        #     # relevant_sheet = working_book['Costs_Breakdown'] 
                        #     # # Grab the maximum row number in the sheet
                        #     # max_row = relevant_sheet.max_row
                        #     # # Refer to the data of close and close_200ma by the range of rorelevant_sheet and cols on the sheet
                        #     # categories = Reference(relevant_sheet, min_col=1, min_row=1, max_col=1, max_row=max_row)
                        #     # values_weekly = Reference(relevant_sheet, min_col=3, min_row=1, max_col=3, max_row=max_row)
                        #     # # Create a bar chart
                        #     # chart = relevant_sheet.add_chart({'type': 'bar'})
                        #     # # Add data of close and close_ma to the chart
                        #     # chart.add_data(categories, titles_from_data=True)
                        #     # chart.add_data(values_weekly, titles_from_data=True)
                        #     # # Set the dates as the x axis and format it
                        #     # #chart.x_axis.number_format = '${0:,.2f}'
                        #     # chart.x_axis.title = 'Weekly Cost ($)'
                        #     # chart.y_axis.title = 'Category'
                        #     # # Add the chart to the cell of F4 on the sheet relevant_sheet
                        #     # relevant_sheet.add_chart(chart, 'F4')
                        #     writer.save()
                        
                        # Once dictionary has been created construct the actual analysis and the library to check for on app startup                                       
                        report_generator = ReportGeneration(budget_dictionary, current_cost_numerical)
                        doc = report_generator.create_report()
                        excel_doc = report_generator.create_excel_report()
                        
                        # Generate a report from the returned doc
                        # doc.generate_pdf('budget_report', clean_tex=False, compiler = 'PDFLaTeX')
                        # report_generator.create_excel_report()
                        # writer = pd.ExcelWriter('budgeting_report.xlsx', engine='xlsxwriter')
                        
                        # # Add  DataFrames
                        # total_costs.to_excel(writer, sheet_name = 'Total_Expenditure')
                        # transposed_budget_table.to_excel(writer, sheet_name = 'Costs_Breakdown')
                        # # Point to the sheet 'Costs_Breakdown', where the chart will be added
                        # working_book = writer.book 
                        # relevant_sheet = working_book['Costs_Breakdown'] 
                        # # Grab the maximum row number in the sheet
                        # max_row = relevant_sheet.max_row
                        # # Refer to the data of close and close_200ma by the range of rorelevant_sheet and cols on the sheet
                        # categories = Reference(relevant_sheet, min_col=1, min_row=1, max_col=1, max_row=max_row)
                        # values_weekly = Reference(relevant_sheet, min_col=3, min_row=1, max_col=3, max_row=max_row)
                        # # Create a bar chart
                        # chart = relevant_sheet.add_chart({'type': 'bar'})
                        # # Add data of close and close_ma to the chart
                        # chart.add_data(categories, titles_from_data=True)
                        # chart.add_data(values_weekly, titles_from_data=True)
                        # # Set the dates as the x axis and format it
                        # chart.x_axis.number_format = '${0:,.2f}'
                        # chart.x_axis.title = 'Weekly Cost ($)'
                        # chart.y_axis.title = 'Category'
                        # # Add the chart to the cell of F12 on the sheet relevant_sheet
                        # relevant_sheet.add_chart(chart, 'F4')
                        # writer.save()
                        

                            
                        # Show the success window following report generation
                        self.show_success_window()
                        with open('budget_text_doc.txt', 'w') as bud:
                            bud.write(json.dumps(budget_dictionary))
                    
                    except:
                        self.show_success_window()
                        with open('budget_text_doc.txt', 'w') as bud:
                            bud.write(json.dumps(budget_dictionary))
                    
            elif duration_error_flag == True:
                # In this case one of the periods is not allowed
                message_prelude = 'Make sure that payment duration is in the set:\n\n\t'
                message_center = str(allowed_payment_periods).title() + '\n\n'
                message_end = 'Or alter allowed list in python script.'
                message = message_prelude + message_center + message_end
                self.show_error_window(message)            
        
        else:
            message = 'Please enter some values for analysis.'
            self.show_error_window(message)

# General form of app GUI generation
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    BudgetOverview = QtWidgets.QMainWindow()
    ui = Ui_BudgetOverview()
    ui.setupUi(BudgetOverview)
    BudgetOverview.show()
    sys.exit(app.exec_())
