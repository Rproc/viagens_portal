from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.models import ColumnDataSource, CategoricalColorMapper, Div
from bokeh.layouts import gridplot, column
from bokeh.models.widgets import Tabs, Panel
from bokeh.models import ColumnDataSource, NumeralTickFormatter
from bokeh.models import HoverTool

import pandas as pd

player_stats = pd.read_csv('2017-18_playerBoxScore.csv', parse_dates=['gmDate'])
team_stats = pd.read_csv('2017-18_teamBoxScore.csv', parse_dates=['gmDate'])
standings = pd.read_csv('2017-18_standings.csv', parse_dates=['stDate'])


phi_gm_stats = (team_stats[(team_stats['teamAbbr'] == 'BOS') & 
                           (team_stats['seasTyp'] == 'Regular')]
                .loc[:, ['gmDate', 
                         'teamPTS', 
                         'teamTRB', 
                         'teamAST', 
                         'teamTO', 
                         'opptPTS',]]
                .sort_values('gmDate'))

# Add game number
phi_gm_stats['game_num'] = range(1, len(phi_gm_stats)+1)

# Derive a win_loss column
win_loss = []
for _, row in phi_gm_stats.iterrows():

    # If the 76ers score more points, it's a win
    if row['teamPTS'] > row['opptPTS']:
        win_loss.append('W')
    else:
        win_loss.append('L')

# Add the win_loss data to the DataFrame
phi_gm_stats['winLoss'] = win_loss

output_file('celtics-gm-linked-stats.html',
                title='Celtics Game Log')

# Store the data in a ColumnDataSource
gm_stats_cds = ColumnDataSource(phi_gm_stats)


win_loss_mapper = CategoricalColorMapper(factors = ['W', 'L'], \
                                         palette=['green', 'red'])


stat_names = {'Points': 'teamPTS',
              'Assists': 'teamAST',
              'Rebounds': 'teamTRB',
              'Turnovers': 'teamTO',}

# The figure for each stat will be held in this dict
stat_figs = {}

# For each stat in the dict
for stat_label, stat_col in stat_names.items():

    # Create a figure
    fig = figure(y_axis_label=stat_label, 
                 plot_height=200, plot_width=400,
                 x_range=(1, 10), tools=['xpan', 'reset', 'save'])

    # Configure vbar
    fig.vbar(x='game_num', top=stat_col, source=gm_stats_cds, width=0.9, 
             color=dict(field='winLoss', transform=win_loss_mapper))

    # Add the figure to stat_figs dict
    stat_figs[stat_label] = fig

grid = gridplot([[stat_figs['Points'], stat_figs['Assists']], \
                [stat_figs['Rebounds'], stat_figs['Turnovers']]])


stat_figs['Points'].x_range = \
    stat_figs['Assists'].x_range = \
    stat_figs['Rebounds'].x_range = \
    stat_figs['Turnovers'].x_range

html = """<h3>Boston Celtics Game Log</h3>
<b><i>2017-18 Regular Season</i>
<br>
</b><i>Wins in green, losses in red</i>
"""
sup_title = Div(text=html)

# Visualize
show(column(sup_title, grid))