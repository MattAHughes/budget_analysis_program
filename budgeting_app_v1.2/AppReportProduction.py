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
    Plot, Figure, Matrix, Alignat, Table, VerticalSpace, HorizontalSpace
import matplotlib.pyplot as plt
from pylatex.utils import italic
import os
from pdflatex import PDFLaTeX

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
                                              self.adjusted_cost_numerical],
                                             ['Category', 'Frequency', 'Weekly Payment ($)'])
        self.adjusted_budget_table = self.adjusted_budget_table.sort_values(by = ['Weekly Payment ($)'], axis = 1)
        sum_total = sum(self.adjusted_cost_numerical)
        self.yearly_total_post_tax = round(52 * sum_total, 2)
        self.yearly_total_optimal = round(self.yearly_total_post_tax + 0.3*self.yearly_total_post_tax, 2)
        self.yearly_total_pre_tax = round(self.yearly_total_optimal + 3572 + (self.yearly_total_optimal - 37000)*0.325, 2)
        self.transposed_budget_table = self.adjusted_budget_table.transpose() 
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
        
        # Now create a tex document markup for the report
        geometry_options = {"tmargin": "1cm", "lmargin": "5cm"}
        doc = Document(geometry_options = geometry_options)
                        
        with doc.create(Section('Budget Overview')):
            doc.append('The total weekly cost based on your budget is:')
            with doc.create(Alignat(numbering=False, escape=False)):
                doc.append(Math(data=[sum_total]))
                
            doc.append('\nWith a total yearly, post-tax, cost of:')
            with doc.create(Alignat(numbering=False, escape=False)):
                doc.append(Math(data=[self.yearly_total_post_tax]))
                
            doc.append('\nAnd a 30% leeway total of:')
            with doc.create(Alignat(numbering=False, escape=False)):
                doc.append(Math(data=[self.yearly_total_optimal]))
                            
            doc.append('\nmaking for an approximate yearly pre-tax total of:')
            with doc.create(Alignat(numbering=False, escape=False)):
                doc.append(Math(data=[self.yearly_total_pre_tax]))
                                  
            doc.append('\nWith a breakdown of:\n')
            doc.append(VerticalSpace("10mm"))
            doc.append(HorizontalSpace("30mm"))
            with doc.create(Tabular('cccc')) as table:
                table.add_hline()
                table.add_row([self.transposed_budget_table.index.name] + list(self.transposed_budget_table.columns))
                table.add_hline()
            for row in self.transposed_budget_table.index:
                table.add_row([row] + list(self.transposed_budget_table.loc[row,:]))
                table.add_hline()
            doc.append(HorizontalSpace("10mm"))
            doc.append(VerticalSpace("10mm"))
            doc.append('\nAnd a plot of:\n')
            with doc.create(Figure(position = 'htbp')) as plot_fig:
                plot_fig.add_plot(dpi = 300, bbox_inches = 'tight')

        return doc
   