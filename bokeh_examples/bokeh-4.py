from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.models import ColumnDataSource, CDSView, GroupFilter
from bokeh.layouts import column, gridplot

import pandas as pd

player_stats = pd.read_csv('2017-18_playerBoxScore.csv', parse_dates=['gmDate'])
team_stats = pd.read_csv('2017-18_teamBoxScore.csv', parse_dates=['gmDate'])
standings = pd.read_csv('2017-18_standings.csv', parse_dates=['stDate'])
# Output to file
# output_file('east-top-2-standings-race.html', 
#             title='Eastern Conference Top 2 Teams Wins Race')

output_file('east-west-top-2-standings-race.html', 
            title='Conference Top 2 Teams Wins Race')

# Create a ColumnDataSource
standings_cds = ColumnDataSource(standings)

# Create views for each team
celtics_view = CDSView(source=standings_cds,
                      filters=[GroupFilter(column_name='teamAbbr', 
                                           group='BOS')])
raptors_view = CDSView(source=standings_cds,
                      filters=[GroupFilter(column_name='teamAbbr', 
                                           group='TOR')])

# Create and configure the figure
east_fig = figure(x_axis_type='datetime',
           plot_height=300, plot_width=600,
           title='Eastern Conference Top 2 Teams Wins Race, 2017-18',
           x_axis_label='Date', y_axis_label='Wins',
           toolbar_location=None)

# Render the race as step lines
east_fig.step('stDate', 'gameWon', 
              color='#007A33', legend='Celtics',
              source=standings_cds, view=celtics_view)
east_fig.step('stDate', 'gameWon', 
              color='#CE1141', legend='Raptors',
              source=standings_cds, view=raptors_view)

# Move the legend to the upper left corner
east_fig.legend.location = 'top_left'

west_top_2 = (standings[(standings['teamAbbr'] == 'HOU') | (standings['teamAbbr'] == 'GS')] \
      .loc[:, ['stDate', 'teamAbbr', 'gameWon']]\
      .sort_values(['teamAbbr','stDate']))

# Set up the figure(s)
# output_file('west-top-2-standings-race.html', 
#             title='Western Conference Top 2 Teams Wins Race')

# Isolate the data for the Rockets and Warriors
rockets_data = west_top_2[west_top_2['teamAbbr'] == 'HOU']
warriors_data = west_top_2[west_top_2['teamAbbr'] == 'GS']

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

east_fig.plot_width = fig.plot_width = 300

east_fig.title.text = 'Eastern Conference'
fig.title.text = 'Western Conference'

east_west_gridplot = gridplot([[fig, east_fig]], 
                              toolbar_location='right')

# show(column(fig, east_fig))
show(east_west_gridplot)


# Show the plot
# show(fig)
# Show the plot
# show(east_fig)