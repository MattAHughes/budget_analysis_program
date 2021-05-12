# -*- coding: utf-8 -*-
"""
Created on Wed May 12 14:51:24 2021

@author: Baska

This is the report development functionality of the budgeting app.
"""
import pandas as pd
import numpy as np
from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat, Table
import matplotlib.pyplot as plt
from pylatex.utils import italic
import os
from pdflatex import PDFLaTeX

class Report_Generation(object):
    def create_report(self, budget_dictionary, current_cost_numerical):
        
        d = {'weekly': 1, 'fortnightly': 1/2, 'monthly': 12/52, 'quarterly': 4/52, 'yearly': 1/52}
        # Create a table
        budget_table = pd.DataFrame(budget_dictionary)
        duration_dictionary_adjusted = pd.Series(budget_dictionary['Frequency']).map(d)
        adjusted_cost_numerical = round(pd.Series(current_cost_numerical)/duration_dictionary_adjusted, 2)
        adjusted_budget_table = pd.DataFrame([budget_dictionary['Category'],
                                              budget_dictionary['Frequency'],
                                              adjusted_cost_numerical],
                                             ['Category', 'Frequency', 'Weekly Payment ($)'])
        sum_total = sum(duration_dictionary_adjusted)
        yearly_total_post_tax = 52 * sum_total
        yearly_total_optimal = yearly_total_post_tax + 0.3*yearly_total_post_tax
        
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
        ax.set_ylabel('Category')

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
        if __name__ == '__main__':
            geometry_options = {"tmargin": "1cm", "lmargin": "10cm"}
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
                    
                doc.append('\nWith a breakdown of:')
                with doc.create(Tabular('ccc')) as table:
                    table.add_hline()
                    table.add_row([adjusted_budget_table.index.name] + list(adjusted_budget_table.columns))
                    table.add_hline()
                    for row in adjusted_budget_table.index:
                        table.add_row([row] + list(adjusted_budget_table.loc[row,:]))
                        table.add_hline()
                        
                doc.append('\nAnd a plot of:')
                with doc.create(Figure(position='htbp')) as plot_fig:
                    plot_fig.add_plot(width=NoEscape(r'1\linewidth'), dpi=300)
           
            doc.generate_pdf('budget_report', clean_tex=False, compiler = 'PDFLaTeX')
                