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
    def __init__(self, figsize=(10, 6), tag = "", title = "", x_label = "X", y_label = "Y", xlim = None, ylim = None, **kwargs):
        self.figsize = figsize
        self.tag = tag
        self.figure, self.ax = plt.subplots(figsize=self.figsize, **kwargs)
        self.ax.set_title(title)
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
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

    def LoadData(self, file_path, x_data_name = "", y_data_name = ""):
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
        self.ax.plot(x_data, y_data, label = label, linewidth = linewidth, **kwargs)
        
    def show(self):
        plt.show()
        
    def save_figure(self, savename = "", loc = "", ext = 'eps', dpi = 1000):
        if (savename == ""):
            savename = self.tag
        
        if ~(savename.endswith(f'.{ext}')):
            savename += f'.{ext}'
            
        self.ax.figure.savefig(savename, format=ext, dpi=dpi)
        
    def show_legend(self, loc = 'best'):
        self.ax.legend(loc = loc)
        
    def add_line_of_best_fit(self, x_data, y_data, order=1, density = 100, **kwargs):
        x = np.linspace(min(x_data), max(x_data), density)
        coefficients = np.polyfit(x_data, y_data, order)
        m, b = coefficients
        line_of_best_fit = np.polyval(coefficients, x)
        self.ax.plot(x, line_of_best_fit, **kwargs)
    
    def add_errorbars(self, x_data, y_data, y_err = None, x_err = None, fmt = 'none', capsize = 1.5, color = 'k', linewidth = 0.8,  **kwargs):
        # Error in the form y_err = [lower, upper]
        self.ax.errorbar(x_data, y_data, yerr = y_err, x_err = x_err, fmt = fmt, capsize = capsize, color = color, linewidth = linewidth, **kwargs)
        
    
    
    
    