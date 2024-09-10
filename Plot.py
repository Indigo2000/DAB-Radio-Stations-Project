from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import Calculations
import config
# import main
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import difflib
import tkinter as tk
from functools import partial
import numpy as np
from matplotlib.figure import Figure
import GUI


# Extracts a dataFrame when passed CurrentState data from json_string for the given multiplex
def create_df(data_in, multiplex_in):
    multiplex = []
    # Cycle through each item writing it to a list
    for item in data_in[Calculations.make_correlation_data_string(multiplex_in)]:
        # Write all the data to a list
        multiplex.append(item)
    # Convert the list to a DataFrame and send it back
    multiplex_df = pd.DataFrame(multiplex)
    return multiplex_df


# Gets the data together for producing the heatmap for two multiplexes
def get_data_for_correlation(mult1_in, mult2_in):

    # Get all the data from json_string
    data = json.loads(config.json_string)

    # Create DataFrames for the two multiplexes given
    config.mult1_df = create_df(data, mult1_in)
    config.mult2_df = create_df(data, mult2_in)

    # Assemble lists of Serv Labels for each multiplex
    multiplex_dict1 = []
    multiplex_dict2 = []

    # List for multiplex 1 - we only need first entry as they all have the same service labels
    multiplex_dict1.append(config.mult1_df.iloc[0]['Serv Label1 '])
    multiplex_dict1.append(config.mult1_df.iloc[0]['Serv Label2 '])
    multiplex_dict1.append(config.mult1_df.iloc[0]['Serv Label3 '])
    multiplex_dict1.append(config.mult1_df.iloc[0]['Serv Label4 '])
    multiplex_dict1.append(config.mult1_df.iloc[0]['Serv Label10 '])

    # List for multiplex 2
    multiplex_dict2.append(config.mult2_df.iloc[0]['Serv Label1 '])
    multiplex_dict2.append(config.mult2_df.iloc[0]['Serv Label2 '])
    multiplex_dict2.append(config.mult2_df.iloc[0]['Serv Label3 '])
    multiplex_dict2.append(config.mult2_df.iloc[0]['Serv Label4 '])
    multiplex_dict2.append(config.mult2_df.iloc[0]['Serv Label10 '])

    # Returns a sequence match (a ratio) for how closely the text of the service labels match
    def apply_sm(c1, c2):
        send_list = []
        for item in c2:
            send_list.append(difflib.SequenceMatcher(isjunk=None, a=c1, b=item).ratio())
        return send_list

    # Gather ratios for the service level matches for the pair of multiplexes
    column1 = apply_sm(c1=config.mult1_df.iloc[0]['Serv Label1 '], c2=multiplex_dict2)
    column2 = apply_sm(c1=config.mult1_df.iloc[0]['Serv Label2 '], c2=multiplex_dict2)
    column3 = apply_sm(c1=config.mult1_df.iloc[0]['Serv Label3 '], c2=multiplex_dict2)
    column4 = apply_sm(c1=config.mult1_df.iloc[0]['Serv Label4 '], c2=multiplex_dict2)
    column5 = apply_sm(c1=config.mult1_df.iloc[0]['Serv Label10 '], c2=multiplex_dict2)

    # Convert the columns to a DataFrame and add labels
    combined_list = [column1, column2, column3, column4, column5]
    config.mult1_vs_mult2_df = pd.DataFrame(combined_list, index=['SL1', 'SL2', 'SL3', 'SL4', 'SL10'],
                                            columns=['SL1', 'SL2', 'SL3', 'SL4', 'SL10'])


# Creates a heatmap for the 2 multiplexes
def create_heatmap(self, mult1_in, mult2_in):
    screen_width = self.winfo_screenwidth()
    # the figure that will contain the plot
    fig = Figure(figsize=(9, 7), dpi=100)

    # adding the subplot
    plot1 = fig.add_subplot(111)

    # Assemble the data for the heatmap
    get_data_for_correlation(mult1_in, mult2_in)
    # Create heatmap for comparing data
    sns.heatmap(config.mult1_vs_mult2_df, vmin=0, vmax=1, annot=True, ax=plot1)
    # Set title
    title = mult1_in + ' v ' + mult2_in + ' Correlation Data'
    plot1.set_title(title)
    # Add Labels
    x_label = mult2_in + ' Service Labels (Block: ' + config.mult2_df.iloc[0]['Block']\
        + ', Freq.: ' + config.mult2_df.iloc[0]['Freq.'] + 'Hz)'
    y_label = mult1_in + ' Service Labels (Block: ' + config.mult1_df.iloc[0]['Block'] \
              + ', Freq.: ' + config.mult1_df.iloc[0]['Freq.'] + 'Hz)'
    plot1.update(dict(xlabel=x_label, ylabel=y_label))

    # Ensure axis labels aren't clipped
    fig.tight_layout()

    # creating the Tkinter canvas containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=self)
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().grid(row=1, column=1, rowspan=8, padx=screen_width / 100, sticky='ns')
# Creates a graphical representation of the service labels and site info for the 3 multiplexes given
def plot_scatter(self):
    screen_width = self.winfo_screenwidth()
    # the figure that will contain the plot
    fig = Figure(figsize=(9, 7), dpi=100)

    # adding the subplot
    plot = fig.add_subplot(111)

    # Get the data for each multiplex's site and stations (x and y axes) and add labels for the legend
    for item in config.desired_multiplexes:
        x = Calculations.get_site_data(item)
        y = Calculations.get_station_data(item)
        lab = Calculations.get_labels(item)

        # plotting the graph for each multiplex (new colour automatically assigned for each one)
        plot.scatter(x, y, label=lab)

    # Make x axis labels vertical
    for label in plot.get_xticklabels():
        label.set_rotation(90)

    # Display the legend
    plot.legend(bbox_to_anchor=(-0.15, 1), loc='lower left')

    # Add Labels
    plot.update(dict(xlabel='Sites', ylabel='Service Labels'))

    # Ensure axis labels aren't clipped
    fig.tight_layout()

    # creating the Tkinter canvas containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=self)
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().grid(row=1, column=1, rowspan=8, padx=screen_width/100, sticky='ns')


# Creates a blank area when no graph is available
def plot_blank(self):
    screen_width = self.winfo_screenwidth()
    # the figure that will contain the plot
    fig = Figure(figsize=(9, 7), dpi=100)

    # adding the subplot
#    plot = fig.add_subplot(111)

    fig.tight_layout()

    # creating the Tkinter canvas containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=self)
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().grid(row=1, column=1, rowspan=8, padx=screen_width/100, sticky='ns')


# Creates a graphical representation of the service labels and site info for the 3 multiplexes given
def plot_scatter(self):
    screen_width = self.winfo_screenwidth()
    # the figure that will contain the plot
    fig = Figure(figsize=(9, 7), dpi=100)

    # adding the subplot
    plot = fig.add_subplot(111)

    # Get the data for each multiplex's site and stations (x and y axes) and add labels for the legend
    for item in config.desired_multiplexes:
        x = Calculations.get_site_data(item)
        y = Calculations.get_station_data(item)
        lab = Calculations.get_labels(item)

        # plotting the graph for each multiplex (new colour automatically assigned for each one)
        plot.scatter(x, y, label=lab)

    # Make x axis labels vertical
    for label in plot.get_xticklabels():
        label.set_rotation(90)

    # Display the legend
    plot.legend(bbox_to_anchor=(-0.15, 1), loc='lower left')

    # Add Labels
    plot.update(dict(xlabel='Sites', ylabel='Service Labels'))

    # Ensure axis labels aren't clipped
    fig.tight_layout()

    # creating the Tkinter canvas containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=self)
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().grid(row=1, column=1, rowspan=8, padx=screen_width/100, sticky='ns')


# Create a heatmap for the first pair of multiplexes
def plot_heat_1(self):
    create_heatmap(self, config.desired_multiplexes[0], config.desired_multiplexes[1])


# Create a heatmap for the second pair of multiplexes
def plot_heat_2(self):
    create_heatmap(self, config.desired_multiplexes[0], config.desired_multiplexes[2])


# Create a heatmap for the third pair of multiplexes
def plot_heat_3(self):
    create_heatmap(self, config.desired_multiplexes[1], config.desired_multiplexes[2])
