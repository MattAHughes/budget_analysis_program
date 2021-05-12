"""
Author - Matthew Hughes
Date - 11/5/2021
Functionality - Creates a GUI for budget setup and analysis
                Generates a library and report from the info
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from AppErrorWindow import *
from AppReportConfirmation import *
import json
import pandas as pd
import numpy as np
from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat, Table, VerticalSpace, HorizontalSpace
import matplotlib.pyplot as plt
from pylatex.utils import italic
import os
from pdflatex import PDFLaTeX

class Ui_BudgetOverview(object):
    
    def setupUi(self, BudgetOverview):
        BudgetOverview.setObjectName("BudgetOverview")
        BudgetOverview.resize(800, 538)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("main_app_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        BudgetOverview.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(BudgetOverview)
        self.centralwidget.setObjectName("centralwidget")
        
        # Add button functionality
        self.add_item_push_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_item_push_button.setGeometry(QtCore.QRect(10, 420, 241, 71))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.add_item_push_button.setFont(font)
        self.add_item_push_button.setObjectName("add_item_push_button")
        self.remove_item_push_button = QtWidgets.QPushButton(self.centralwidget)
        self.remove_item_push_button.setGeometry(QtCore.QRect(260, 420, 241, 71))
        self.add_item_push_button.clicked.connect(self.add_to_table)
        font = QtGui.QFont()
        font.setPointSize(18)
        
        # Add remove button functionality
        self.remove_item_push_button.setFont(font)
        self.remove_item_push_button.setObjectName("remove_item_push_button")
        self.generate_report_push_button = QtWidgets.QPushButton(self.centralwidget)
        self.generate_report_push_button.setGeometry(QtCore.QRect(530, 410, 251, 91))
        self.remove_item_push_button.clicked.connect(self.remove_from_table)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        
        # Add generate report button functionality
        self.generate_report_push_button.setFont(font)
        self.generate_report_push_button.setObjectName("generate_report_push_button")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 30, 761, 371))
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
                        
                        # Once dictionary has been created construct the actual analysis and the library to check for on app startup                                       
                        d = {'weekly': 1, 'fortnightly': 1/2, 'monthly': 12/52, 'quarterly': 4/52, 'yearly': 1/52}
                        # Create a table
                        budget_table = pd.DataFrame(budget_dictionary)
                        duration_dictionary_adjusted = pd.Series(budget_dictionary['Frequency']).map(d)
                        adjusted_cost_numerical = round(pd.Series(current_cost_numerical)*duration_dictionary_adjusted, 2)
                        adjusted_budget_table = pd.DataFrame([budget_dictionary['Category'],
                                                              budget_dictionary['Frequency'],
                                                              adjusted_cost_numerical],
                                                             ['Category', 'Frequency', 'Weekly Payment ($)'])
                        sum_total = sum(adjusted_cost_numerical)
                        yearly_total_post_tax = round(52 * sum_total, 2)
                        yearly_total_optimal = round(yearly_total_post_tax + 0.3*yearly_total_post_tax, 2)
                        transposed_budget_table = adjusted_budget_table.transpose() 
                        y =  adjusted_budget_table.loc['Category'] 
                        x =  adjusted_budget_table.loc['Weekly Payment ($)'] 
                        
                        # set the style of the axes and the text color
                        plt.rcParams['axes.edgecolor']='#333F4B'
                        plt.rcParams['axes.linewidth']=0.8
                        plt.rcParams['xtick.color']='#333F4B'
                        plt.rcParams['ytick.color']='#333F4B'
                        plt.rcParams['text.color']='#333F4B'
                        # we first need a numeric placeholder for the y axis
                        my_range=list(range(1, len(y) + 1))

                        fig, ax = plt.subplots(figsize=(5,3.5))
                        #create for each expense type an horizontal line that starts at x = 0 with the length 
                        # represented by the specific expense percentage value.
                        plt.hlines(y = my_range, xmin = 0, xmax = x, color='#007ACC', alpha=0.2, linewidth=5)
                        
                        # create for each expense type a dot at the level of the expense percentage value
                        plt.plot(x, my_range, "o", markersize=5, color='#007ACC', alpha=0.6)
                        
                        # set labels
                        ax.set_xlabel('Amount per Week ($)', fontsize=15, fontweight='black', color = '#333F4B')
                        ax.set_ylabel('Category', fontsize=15, fontweight='black', color = '#333F4B')
                        
                        # set axis
                        ax.tick_params(axis='both', which='major', labelsize=12)
                        plt.yticks(my_range, y)
                        
                        # change the style of the axis spines
                        ax.spines['top'].set_visible(False)
                        ax.spines['right'].set_visible(False)
                        
                        ax.spines['left'].set_bounds((1, len(my_range)))
                        
                        ax.spines['left'].set_position(('outward', 8))
                        ax.spines['bottom'].set_position(('outward', 5))        
                        
                        # Now create a tex document markup for the report
                        geometry_options = {"tmargin": "1cm", "lmargin": "5cm"}
                        doc = Document(geometry_options=geometry_options)
                        
                        with doc.create(Section('Budget Overview')):
                            doc.append('The total weekly cost based on your budget is:')
                            with doc.create(Alignat(numbering=False, escape=False)):
                                doc.append(Math(data=[sum_total]))
                
                            doc.append('\nWith a total yearly, post-tax, cost of:')
                            with doc.create(Alignat(numbering=False, escape=False)):
                                doc.append(Math(data=[yearly_total_post_tax]))
                
                            doc.append('\nAnd a 30% leeway total of:')
                            with doc.create(Alignat(numbering=False, escape=False)):
                                doc.append(Math(data=[yearly_total_optimal]))
                                
                            doc.append('\nWith a breakdown of:\n')
                            doc.append(VerticalSpace("10mm"))
                            doc.append(HorizontalSpace("30mm"))
                            with doc.create(Tabular('cccc')) as table:
                                table.add_hline()
                                table.add_row([transposed_budget_table.index.name] + list(transposed_budget_table.columns))
                                table.add_hline()
                            for row in transposed_budget_table.index:
                                table.add_row([row] + list( transposed_budget_table.loc[row,:]))
                                table.add_hline()
                            doc.append(HorizontalSpace("10mm"))
                            doc.append(VerticalSpace("10mm"))
                            doc.append('\nAnd a plot of:\n')
                            with doc.create(Figure(position='htbp')) as plot_fig:
                                plot_fig.add_plot(dpi=300, bbox_inches='tight')
                                
                        doc.generate_pdf('budget_report', clean_tex=False, compiler = 'PDFLaTeX')
                
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

