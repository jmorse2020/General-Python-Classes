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
    def __init__(self, rows=1, cols=1, figsize=(10, 6),  tag = "", title = "t", x_label = "X", y_label = "Y", axis_font_size = 20, title_font_size = 26, **kwargs):
        self.title_font_size = title_font_size
        self.axis_font_size = axis_font_size
        self.tag = tag
        self.fig, self.ax = plt.subplots(nrows=rows, ncols=cols, figsize = figsize, **kwargs)
        self.cols = cols
        self.rows = rows
        if rows == 1 and cols == 1:
            # self.ax = [[self.ax]]
            self._access_subplot(self, 0, 0).set_xlabel(x_label, fontsize=self.axis_font_size)
            self._access_subplot(self, 0, 0).set_ylabel(y_label, fontsize=self.axis_font_size)
           
            
        self.fig.suptitle(title, fontsize=self.title_font_size)
        for ax in np.array(self.ax).reshape(-1):
            ax.tick_params(axis='both', which='major', labelsize=self.axis_font_size)
   
    def xlabel(self, label, row = 0, col = 0):
        """
        Add x label to axis. For figures with multiple axes, select the axis at [row, col].

        Parameters
        -------
        label (string): x axis label
        row (int): row of axis
        col (int): column of axis
         

        Returns
        -------
        Adds x label to axis.
        """
        self._access_subplot(self, row, col).set_xlabel(xlabel=label, fontsize = self.axis_font_size)
    
    def ylabel(self, label, row = 0, col = 0):
        """
        Add y label to axis. For figures with multiple axes, select the axis at [row, col].

        Parameters
        -------
        label (string): y axis label
        row (int): row of axis
        col (int): column of axis
         

        Returns
        -------
        Adds y label to axis.
        """
        self._access_subplot(self, row, col).set_ylabel(label=label, fontsize = self.axis_font_size)
        
    def set_xlim(self, xlim, row = 0, col = 0):
        """
        Set x limit to axis. For figures with multiple axes, select the axis at [row, col].

        Parameters
        -------
        xlim (tuple): tuple of floats, e.g. (xmin, xmax)
        row (int): row of axis
        col (int): column of axis
         

        Returns
        -------
        Set the x axis limit.
        """
        if xlim is not None: 
            try:
                self._access_subplot(self, row,col).set_xlim(xlim)
            except:
                warnings.warn("Unable to set custom x limits")
        
    def set_ylim(self, ylim, row = 0, col = 0):
        """
        Set y limit to axis. For figures with multiple axes, select the axis at [row, col].

        Parameters
        -------
        ylim (tuple): tuple of floats, e.g. (ymin, ymax)
        row (int): row of axis
        col (int): column of axis
         

        Returns
        -------
        Set the y axis limit.
        """
        if ylim is not None:
            try:
                self._access_subplot(self, row, col).set_ylim(ylim)
            except:
                warnings.warn("Unable to set custom y limits")
        
    def load_csv_data(self, file_path, column_names = [], skiprows = 0, **kwargs):
        """
        Load data from a csv file with columns of data with headers 'column_names'.

        Parameters
        -------
        file_path (string): path to csv file
        column_names (string array): array containing the column names of all the columns to load, e.g. ["Header1", "Header2"]
        skiprows (int): number of rows in the csv file to skip
         

        Returns
        -------
        Array with each element containing the data in the corresponding column in column_names.
        """
        import os, warnings
        if (os.path.isfile(file_path) == False):
            warnings.warn("Not a valid file name", UserWarning)
            return [[], []]
        
        data = pd.read_csv(file_path, skiprows=skiprows, **kwargs)
        output= []
        for column in column_names:
            if ((column in data.columns) == False):
                warnings.warn(f"column '{column}' is not a valid column name")
            else:
                output.append(data[column])
        return output
    
    def add_plot(self, x_data, y_data, label = None, row = 0, col = 0,  linewidth = 1, color = 'k', **kwargs):
        """
        Add data to axis. For figures with multiple axes, select the axis at [row, col].

        Parameters
        -------
        x_data (array): x data to be plotted
        y_data (array): y data to be plotted
        label (string): label of the series, used for legends etc.
        row (int): row of axis
        col (int): column of axis
         

        Returns
        -------
        Adds data to axis.
        """
        self._access_subplot(self, row, col).plot(x_data, y_data, label = label, linewidth = linewidth, color=color, **kwargs)
        
    def show(self):
        plt.show()
        
    def save_figure(self, savename = "", loc = "", ext = 'eps', dpi = 1000):
        """
        Save a figure.

        Parameters
        -------
        savename (string): name of figure. Defaults to figure tag.
        loc (string): path to folder to save figure
        ext (string): file extension, e.g. 'eps', 'png', 'jpg'
         

        Returns
        -------
        Saves figure in desired format.
        """
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
            self.fig.savefig(savename, format=ext, dpi=dpi)
        except Exception as e:
            print(f"Error: Unable to save\nException: {str(e)}")
                
        
    def show_legend(self, loc = 'best', row=0, col=0, fontsize=None):
        """
        Show legend on axis. For figures with multiple axes, select the axis at [row, col].

        Parameters
        -------
        loc (string): location on axis, e.g. 'upper right', 'lower right'
        row (int): row of axis
        col (int): column of axis
         

        Returns
        -------
        Shows legend on axis
        """
        if fontsize is None:
            fontsize =self.axis_font_size           
        self._access_subplot(self, row, col).legend(loc = loc, fontsize=fontsize)
        
    def add_line_of_best_fit(self, x_data, y_data, row=0, col=0, density = 100, display_equation = False, display_equation_position = None, return_coefficients = False, fontsize = None, **kwargs):
        """
        Add line of best fit to data on axis. For figures with multiple axes, select the axis at [row, col].

        Parameters
        -------
        x_data (array): x data
        y_data (array): y data
        display_equation (bool): whether to display equation text. Requires position.
        display_equation_position (tuple): position on axis, e.g. (0.5, 0.5)
        return_coefficients (bool): returns coefficeints of the fit
        row (int): row of axis
        col (int): column of axis
         

        Returns
        -------
        Adds line of best fit to axis
        """
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
            self._access_subplot(self, row, col).text(display_equation_position[0], display_equation_position[1], equation_text, fontsize = fontsize)    
        elif ((display_equation == True) & (display_equation_position is None)):
            print("Add Line Of Best Fit Message: Please add a position for the equation to be displayed.")
        self._access_subplot(self, row, col).plot(x, line_of_best_fit, label=equation_text, **kwargs)
        if return_coefficients == True:
            return coefficients
    
    def add_errorbars(self, x_data, y_data, y_err = None, x_err = None, row=0, col=0, fmt = 'none', capsize = 1.5, color = 'k', linewidth = 0.8,  **kwargs):
        """
        Add error bars to data on axis. For figures with multiple axes, select the axis at [row, col].

        Parameters
        -------
        x_data (array): x data
        y_data (array): y data  
        y_err (array): y error data in the form [lower, upper]
        x_err (array): x error data in the form [lower, upper]
        row (int): row of axis
        col (int): column of axis
         

        Returns
        -------
        Adds error bars to data on axis
        """
        self._access_subplot(self, row, col).errorbar(x_data, y_data, yerr = y_err, x_err = x_err, fmt = fmt, capsize = capsize, color = color, linewidth = linewidth, **kwargs)
        
    def normalise_data(self, y_data):
        """
        Normalise y data.

        Parameters
        -------
        y_data (array): data to be normalised
         

        Returns
        -------
        Normalised y data
        """
        return (y_data - min(y_data))/ max(y_data - min(y_data)); 
    
    def restrict_domain(self, x_data, y_data, x_min, x_max):
        """
        Restricts data to a smaller domain.

        Parameters
        -------
        x_data (array): x data
        y_data (array): y data  
        x_min (float): minimum x value
        x_max (float): maximum x value
         

        Returns
        -------
        X and y data restricted to smaller domain.
        """
        idx = np.where((x_min < x_data) & (x_data < x_max))[0]
        return [x_data[idx], y_data[idx]]
    
    def add_polynomial_of_best_fit(self, x_data, y_data, order, row = 0, col = 0, density = 100, display_equation = False, display_equation_position = None, return_coefficients = False, fontsize = None, **kwargs):
        """
        Add polynomial of best fit to data on axis. For figures with multiple axes, select the axis at [row, col].

        Parameters
        -------
        x_data (array): x data
        y_data (array): y data
        order (int): order of fit
        display_equation (bool): whether to display equation text. Requires position.
        display_equation_position (tuple): position on axis, e.g. (0.5, 0.5)
        return_coefficients (bool): returns coefficeints of the fit
        row (int): row of axis
        col (int): column of axis
         

        Returns
        -------
        Adds polynomial of best fit to axis and coefficeints if selected
        """
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
            self._access_subplot(self, row, col).text(display_equation_position[0], display_equation_position[1], equation_text, fontsize = fontsize)    
        elif ((display_equation == True) & (display_equation_position is None)):
            print("Add Polynomial Of Best Fit Message: Please add a position for the equation to be displayed.")
        self._access_subplot(self, row, col).plot(x, polynomial_of_best_fit, label=equation_text, **kwargs)
        if return_coefficients == True:
            return coefficients
    
    def translate_y(self, y_data, translation):
        """
        Shifts data by a value.

        Parameters
        -------
        y_data (array): data to be translated
        translation (float): translation amount
         

        Returns
        -------
        Translated data
        """
        return y_data + translation
    
    @staticmethod
    def _access_subplot(self, row, col):
        if self.rows == 1 and self.cols == 1:
            return self.ax
        elif self.rows == 1:
            return self.ax[col]
        elif self.cols == 1:
            return self.ax[row]
        else:
            return self.ax[row][col]
        
    def subplot(self, row, col):
        if self.rows == 1 and self.cols == 1:
            return self.ax
        elif self.rows == 1:
            return self.ax[col]
        elif self.cols == 1:
            return self.ax[row]
        else:
            return self.ax[row][col]
    
    