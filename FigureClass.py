# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 09:31:01 2023

@author: Jack Morse

Class with methods to aid consistent plotting with easy formatting.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import warnings
import os

class Figure:
    def __init__(self, figsize=(10, 6), tag = "", title = "", x_label = "X", y_label = "Y", xlim = None, ylim = None, axis_font_size = 20, title_font_size = 26, **kwargs):
        self.figsize = figsize
        self.title_font_size = title_font_size
        self.axis_font_size = axis_font_size
        self.tag = tag
        self.figure, self.ax = plt.subplots(figsize=self.figsize, **kwargs)
        self.ax.set_title(title, fontsize=self.title_font_size)
        self.ax.set_xlabel(x_label, fontsize=self.axis_font_size)
        self.ax.set_ylabel(y_label, fontsize=self.axis_font_size)
        self.ax.tick_params(axis='both', which='major', labelsize=self.axis_font_size)
        if xlim is not None: 
            try:
                self.ax.set_xlim(xlim)
            except:
                warnings.warn("Unable to set custom x limits")
        if ylim is not None:
            try:
                self.ax.set_ylim(ylim)
            except:
                warnings.warn("Unable to set custom y limits")
                
        
    def StandAloneFigure(self, x_data = [], y_data = [], xlabel = "X", ylabel = "Y", title = "", legend=False, **kwargs):  
        fig, ax = plt.subplots()
        ax.plot(x_data, y_data, **kwargs)

    def load_csv_data(self, file_path, x_data_name = "", y_data_name = ""):
        if (os.path.isfile(file_path) == False):
            warnings.warn("Not a valid file name", UserWarning)
            return [[], []]
        
        data = pd.read_csv(file_path)
        
        if ((x_data_name in data.columns) == False):
            warnings.warn(f"x_data_name '{x_data_name}' is not a valid column name")
            return [[], []]
        if ((y_data_name in data.columns) == False):
            warnings.warn(f"y_data_name '{y_data_name}' is not a valid column name")
            return [[], []]
        return [data[x_data_name], data[y_data_name]]
    
    def add_plot(self, x_data, y_data, label = None, linewidth = 1, color = 'k', **kwargs):
        self.ax.plot(x_data, y_data, label = label, linewidth = linewidth, color=color, **kwargs)
        
    def show(self):
        plt.show()
        
    def save_figure(self, savename = "", loc = "", ext = 'eps', dpi = 1000):
        if (savename == ""):
            savename = self.tag
        
        if ~(savename.endswith(f'.{ext}')):
            savename += f'.{ext}'
        
        if loc != "":
            if (os.path.isfile(loc) == False):
                savename = os.path.join(loc, savename)                
            else:
                print(f"loc argument '{loc}' is not a valid file name")
        try:
            self.ax.figure.savefig(savename, format=ext, dpi=dpi)
        except Exception as e:
            print(f"Error: Unable to save\nException: {str(e)}")
                
        
    def show_legend(self, loc = 'best', fontsize=None):
        if fontsize is None:
            fontsize =self.axis_font_size           
        self.ax.legend(loc = loc, fontsize=fontsize)
        
    def add_line_of_best_fit(self, x_data, y_data, density = 100, display_equation = False, display_equation_position = None, return_coefficients = False, fontsize = None, **kwargs):
        x = np.linspace(min(x_data), max(x_data), density)
        coefficients = np.polyfit(x_data, y_data, 1)
        line_of_best_fit = np.polyval(coefficients, x)
       
        equation_text = 'y = '
        display_round_to = 1
        for i in range(len(coefficients)):
            if i == len(coefficients) - 1:
                equation_text += str(round(coefficients[i], display_round_to))
            elif i == (len(coefficients) - 2):
                equation_text += str(round(coefficients[i], display_round_to)) + "x + "
            else:
                equation_text += str(round(coefficients[i], display_round_to)) + f"$x^{i} + $"
        if ((display_equation == True) & (display_equation_position is not None)):
            if fontsize == None:
                fontsize = self.axis_font_size
            self.ax.text(display_equation_position[0], display_equation_position[1], equation_text, fontsize = fontsize)    
        elif ((display_equation == True) & (display_equation_position is None)):
            print("Add Line Of Best Fit Message: Please add a position for the equation to be displayed.")
        self.ax.plot(x, line_of_best_fit, label=equation_text, **kwargs)
        if return_coefficients == True:
            return coefficients
    
    def add_errorbars(self, x_data, y_data, y_err = None, x_err = None, fmt = 'none', capsize = 1.5, color = 'k', linewidth = 0.8,  **kwargs):
        # Error in the form y_err = [lower, upper]
        self.ax.errorbar(x_data, y_data, yerr = y_err, x_err = x_err, fmt = fmt, capsize = capsize, color = color, linewidth = linewidth, **kwargs)
        
    def normalise_data(self, y_data):
        return (y_data - min(y_data))/ max(y_data - min(y_data)); 
    
    def restrict_domain(self, x_data, y_data, x_min, x_max):
        idx = np.where((x_min < x_data) & (x_data < x_max))[0]
        return [x_data[idx], y_data[idx]]
    
    def add_polynomial_of_best_fit(self, x_data, y_data, order, density = 100, display_equation = False, display_equation_position = None, return_coefficients = False, fontsize = None, **kwargs):
        x = np.linspace(min(x_data), max(x_data), density)
        coefficients = np.polyfit(x_data, y_data, order)
        polynomial_of_best_fit = np.polyval(coefficients, x)
       
        equation_text = 'y = '
        display_round_to = 1
        for i in range(len(coefficients)):
            if i == len(coefficients) - 1:
                equation_text += str(round(coefficients[i], display_round_to))
            elif i == (len(coefficients) - 2):
                equation_text += str(round(coefficients[i], display_round_to)) + "x + "
            else:
                equation_text += str(round(coefficients[i], display_round_to)) + f"$x^{i} + $"
        if ((display_equation == True) & (display_equation_position is not None)):
            if fontsize == None:
                fontsize = self.axis_font_size
            self.ax.text(display_equation_position[0], display_equation_position[1], equation_text, fontsize = fontsize)    
        elif ((display_equation == True) & (display_equation_position is None)):
            print("Add Polynomial Of Best Fit Message: Please add a position for the equation to be displayed.")
        self.ax.plot(x, polynomial_of_best_fit, label=equation_text, **kwargs)
        if return_coefficients == True:
            return coefficients
    
    
    
    