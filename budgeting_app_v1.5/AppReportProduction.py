# -*- coding: utf-8 -*-
"""
Created on Wed May 12 14:51:24 2021

@author: Baska

This is the report development functionality of the budgeting app.
"""
import pandas as pd
import numpy as np
import json
from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat, Table, VerticalSpace, HorizontalSpace, frames, Center
import matplotlib.pyplot as plt
from pylatex.utils import italic
import os
from pdflatex import PDFLaTeX
from jinja2 import Environment, FileSystemLoader
import pdfkit


class ReportGeneration:
    def __init__(self, budget_dictionary, current_cost_numerical):
        self.budget_dictionary = budget_dictionary
        self.current_cost_numerical = current_cost_numerical
        
    def create_report(self):
        
        # Once dictionary has been created construct the actual analysis and the library to check for on app startup                                       
        self.d = {'weekly': 1, 'fortnightly': 1/2, 'monthly': 12/52, 'quarterly': 4/52, 'yearly': 1/52}
        # Create a table
        self.budget_table = pd.DataFrame(self.budget_dictionary)
        self.duration_dictionary_adjusted = pd.Series(self.budget_dictionary['Frequency']).map(self.d)
        self.adjusted_cost_numerical = round(pd.Series(self.current_cost_numerical)*self.duration_dictionary_adjusted, 2)
        self.adjusted_budget_table = pd.DataFrame([self.budget_dictionary['Category'],
                                              self.budget_dictionary['Frequency'],
                                              self.adjusted_cost_numerical,
                                              self.adjusted_cost_numerical * 2],
                                             ['Category', 'Frequency', 'Weekly Payment ($)', 'Fortnightly Payment($)'])
        self.adjusted_budget_table = self.adjusted_budget_table.sort_values(by = ['Weekly Payment ($)'], axis = 1)
        # weekly, fortnightly, and monthly total costs
        sum_total = sum(self.adjusted_cost_numerical)
        sum_total_fortnightly = sum_total * 2
        sum_total_monthly = round(sum_total * 52/12, 2)
        
        self.yearly_total_post_tax = round(52 * sum_total, 2)
        # self.yearly_total_optimal = round(self.yearly_total_post_tax + 0.3*self.yearly_total_post_tax, 2)
        self.yearly_total_pre_tax = round(self.yearly_total_post_tax + 3572 + (self.yearly_total_post_tax - 37000)*0.325, 2)
        self.transposed_budget_table = self.adjusted_budget_table.transpose() 
        # self.transposed_budget_table['Fortnightly Payment ($)'] = self.transposed_budget_table['Weekly Payment($)'] * 2
        self.total_costs = pd.DataFrame({'Weekly': [sum_total], 'Fortnightly': [sum_total_fortnightly], 'Monthly': [sum_total_monthly]})

        y =  self.adjusted_budget_table.loc['Category']
        y = [item.title() for item in y]
        x =  self.adjusted_budget_table.loc['Weekly Payment ($)'] 
                        
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
        plt.savefig('budget_breakdown.png', bbox_inches = "tight", dpi = 400)
        
        # Now create a html report from the data
      
        # 2. Create a template Environment
        env = Environment(loader=FileSystemLoader('templates'))
        loader=FileSystemLoader('templates')
        # 3. Load the template from the Environment
        template = env.get_template('template_structure.html')
        self.data_yearly_total_post_tax = pd.DataFrame([self.yearly_total_post_tax], columns = ['Yearly Total ($)'])
        self.data_yearly_total_pre_tax = pd.DataFrame([self.yearly_total_pre_tax], columns = ['Yearly Total ($)'])
        
        # 4. Render the template with variables
        html = template.render(page_title_text='Budget Overview',
                               title_text = 'Budget Overview',
                               text_string_1 ='The total costs based on your budget are:',
                               text_string_2 ='With a total yearly, post-tax, cost of:',
                               text_string_3 ='Making for an approximate yearly pre-tax total of:',
                               text_string_4 ='With a breakdown of:',
                               prices_text='And a plot of:',
                               stats_text='Historical prices summary statistics',
                               yearly_total_post_tax = self.data_yearly_total_post_tax,
                               total_costs = self.total_costs,
                               yearly_total_pre_tax= self.data_yearly_total_pre_tax,
                               transposed_budget_table = self.transposed_budget_table)
        
        # 5. Write the template to an HTML file
        with open('html_report_budget.html', 'w') as f:
            f.write(html)
        
        
        # path_wkhtmltopdf = r'./pdf_creation_dependancy//wkhtmltox-0.12.4_msvc2015-win64//bin//wkhtmltopdf.exe'
        # config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        # pdfkit.from_file('html_report_budget.html', 'budget_report.pdf', configuration = config)
      
        # # plt.save('budget_breakdown.png')
        # # Now create a tex document markup for the report
        # geometry_options = {"tmargin": "1cm", "lmargin": "5cm"}
        # doc = Document(geometry_options = geometry_options)     
               
        # with doc.create(Section('Budget Overview')):
        #     doc.append('The total costs based on your budget is:\n\n')
        #     # with doc.create(Alignat(numbering=False, escape=False)):
        #     #     doc.append(Math(data=[sum_total]))
        #     doc.append(VerticalSpace("10mm"))
        #     doc.append(HorizontalSpace("30mm"))
        #     with doc.create(Tabular('ccc', row_height=(1.5))) as table:
        #         table.add_hline()
        #         table.add_row('Weekly', 'Fortnightly', 'Monthly')
        #         table.add_hline()
        #         table.add_row(sum_total, sum_total_fortnightly, sum_total_monthly)
        #         table.add_hline()
                
        #     doc.append('\nWith a total yearly, post-tax, cost of:\n')
        #     # with doc.create(Alignat(numbering=False, escape=False)):
        #     #     doc.append(Math(data=[self.yearly_total_post_tax]))
        #     with doc.create(Center()) as centered_1:
        #         with centered_1.create(Tabular('|c|')) as table:
        #             table.add_hline()
        #             table.add_row(Math(data = [self.yearly_total_post_tax]))
        #             table.add_hline()
        #     # doc.append('\nAnd a 30% leeway total of:')
        #     # with doc.create(Alignat(numbering=False, escape=False)):
        #     #     doc.append(Math(data=[self.yearly_total_optimal]))
                            
        #     doc.append('\n\nMaking for an approximate yearly pre-tax total of:\n')
        #     # with doc.create(Alignat(numbering=False, escape=False)):
        #     #     doc.append(Math(data=[self.yearly_total_pre_tax]))
        #     with doc.create(Center()) as centered:
        #         with centered.create(Tabular('|c|')) as table:
        #             table.add_hline()
        #             table.add_row(Math(data = [self.yearly_total_pre_tax]))
        #             table.add_hline()
                                  
        #     doc.append('\n\nWith a breakdown of:\n\n')
        #     doc.append(VerticalSpace("10mm"))
        #     doc.append(HorizontalSpace("30mm"))
        #     with doc.create(Tabular('cccc')) as table:
        #         table.add_hline()
        #         table.add_row(list(self.transposed_budget_table.columns))
        #         table.add_hline()
        #     for row in self.transposed_budget_table.index:
        #         table.add_row( list(self.transposed_budget_table.loc[row,:]))
        #         table.add_hline()
        #     doc.append(HorizontalSpace("10mm"))
        #     doc.append(VerticalSpace("10mm"))
        #     doc.append('\nAnd a plot of:\n')
        #     with doc.create(Figure(position = 'htbp')) as plot_fig:
        #         plot_fig.add_plot(dpi = 300, bbox_inches = 'tight')

        # return doc

    def create_excel_report(self):
        #Create an excel document for the report
        with pd.ExcelWriter('budget_report.xlsx', engine='xlsxwriter') as writer:
            self.total_costs.to_excel(writer, sheet_name = 'Total_Expenditure')
            self.transposed_budget_table.to_excel(writer, sheet_name = 'Costs_Breakdown')
           
            # Let us now plot a figure
            
            # Point to the sheet 'Costs_Breakdown', where the chart will be added
            working_book = writer.book 
            worksheet = working_book.add_worksheet('Plotted Data')
            # working_book.add_sheet('Plotted_Costs_Breakdown')
            # relevant_sheet = writer['Costs_Breakdown']
            # # Grab the maximum row number in the sheet
            max_row =  self.transposed_budget_table.shape[0]
            # Refer to the data of close and close_200ma by the range of rorelevant_sheet and cols on the sheet
            categories = self.transposed_budget_table['Category']
            values_weekly = self.transposed_budget_table['Weekly Payment ($)']
            # Create a bar chart
            chart = working_book.add_chart({'type': 'bar'})
            # # # Add data of close and close_ma to the chart
            chart.add_series({
                'name':       'Breakdown',
                'categories': ['Costs_Breakdown', 1, 1, max_row , 1],
                'values':     ['Costs_Breakdown', 1, 3, max_row, 3],
                })
            # Add a chart title
            chart.set_title ({'name': 'Weekly Cost Breakdown'})
 
            # Add x-axis label
            chart.set_x_axis({'name': 'Weekly Cost ($)'})
             
            # Add y-axis label
            chart.set_y_axis({'name': 'Categories'})
             
            # Set an Excel chart style.
            chart.set_style(11)
            # # # Set the dates as the x axis and format it
            # # chart.x_axis.number_format = '${0:,.2f}'
            # # chart.x_axis.title = 'Weekly Cost ($)'
            # # chart.y_axis.title = 'Category'
            # # # Add the chart to the cell of F12 on the sheet relevant_sheet
            # # relevant_sheet.add_chart(chart, 'F4')
            worksheet.insert_chart('B2', chart)
            writer.save()
        # book = load_workbook('budget_report.xlsx')  
        # writer = pd.ExcelWriter('budget_report.xlsx', engine='openpyxl')
        # writer.book = book
        # relevant_sheet = book.sheetnames['Costs_Breakdown']
        # writer.save()
        # writer = pd.ExcelWriter('budgeting_report.xlsx', engine='openpyxl')
        
        # # Add  DataFrames
        # self.total_costs.to_excel(writer, sheet_name = 'Total_Expenditure')
        # self.transposed_budget_table.to_excel(writer, sheet_name = 'Costs_Breakdown')
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
        
        
            