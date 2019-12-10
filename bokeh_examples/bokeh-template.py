"""Bokeh Visualization Template
This template is a general outline for turning your data into a
visualization using Bokeh.
"""
# Data handling
import pandas as pd  # noqa
import numpy as np  # noqa

# Bokeh libraries
from bokeh.io import output_file, output_notebook
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource  # noqa
from bokeh.layouts import row, column, gridplot  # noqa
from bokeh.models.widgets import Tabs, Panel  # noqa

# Prepare the data

# Determine where the visualization will be rendered
output_file("filename.html")  # Render to static HTML, or
# output_notebook()  # Render inline in a Jupyter Notebook

# Set up the figure(s)
fig = figure(background_fill_color='gray',
             background_fill_alpha=0.5,
             border_fill_color='blue',
             border_fill_alpha=0.25,
             plot_height=300,
             plot_width=500,
             h_symmetry=True,
             x_axis_label='X Label',
             x_axis_type='datetime',
             x_axis_location='above',
             x_range=('2018-01-01', '2018-06-30'),
             y_axis_label='Y Label',
             y_axis_type='linear',
             y_axis_location='left',
             y_range=(0, 100),
             title='Example Figure',
             title_location='right',
             toolbar_location='below',
             tools='save') # Instantiate a figure() object

# Connect to and draw the data

# Organize the layout

# Preview and save
show(fig)  # See what I made, and save if I like it 
