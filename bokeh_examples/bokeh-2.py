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
player_stats = pd.read_csv('2017-18_playerBoxScore.csv', parse_dates=['gmDate'])
team_stats = pd.read_csv('2017-18_teamBoxScore.csv', parse_dates=['gmDate'])
standings = pd.read_csv('2017-18_standings.csv', parse_dates=['stDate'])
# Determine where the visualization will be rendered
# output_file("filename.html")  # Render to static HTML, or
# output_notebook()  # Render inline in a Jupyter Notebook


west_top_2 = (standings[(standings['teamAbbr'] == 'HOU') | (standings['teamAbbr'] == 'GS')] \
      .loc[:, ['stDate', 'teamAbbr', 'gameWon']]\
      .sort_values(['teamAbbr','stDate']))

# Set up the figure(s)
output_file('west-top-2-standings-race.html',
            title='Western Conference Top 2 Teams Wins Race')

# Isolate the data for the Rockets and Warriors
rockets_data = west_top_2[west_top_2['teamAbbr'] == 'HOU']
warriors_data = west_top_2[west_top_2['teamAbbr'] == 'GS']

print(type(rockets_data))
# Create a ColumnDataSource object for each team
rockets_cds = ColumnDataSource(rockets_data)
warriors_cds = ColumnDataSource(warriors_data)

# Create and configure the figure
fig = figure(x_axis_type='datetime',
             plot_height=300, plot_width=600,
             title='Western Conference Top 2 Teams Wins Race, 2017-18',
             x_axis_label='Date', y_axis_label='Wins',
             toolbar_location=None)

# Render the race as step lines
fig.step('stDate', 'gameWon',
         color='#CE1141', legend='Rockets',
         source=rockets_cds)
fig.step('stDate', 'gameWon',
         color='#006BB6', legend='Warriors',
         source=warriors_cds)

# Move the legend to the upper left corner
fig.legend.location = 'top_left'

# Show the plot
show(fig)

# See what I made, and save if I like it
