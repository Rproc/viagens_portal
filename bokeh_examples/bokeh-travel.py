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
viagens = pd.read_excel('data/dadosbrutos2.xlsx')

celtics_gm_stats_2 = (team_stats[(team_stats['teamAbbr'] == 'BOS') & 
                             (team_stats['seasTyp'] == 'Regular')]
                  .loc[:, ['gmDate',
                           'team2P%',
                           'team3P%',
                           'teamPTS',
                           'opptPTS']]
                  .sort_values('gmDate'))

# Add game number
celtics_gm_stats_2['game_num'] = range(1, len(celtics_gm_stats_2) + 1)

# Derive a win_loss column
win_loss = []
for _, row in celtics_gm_stats_2.iterrows():

    # If the 76ers score more points, it's a win
    if row['teamPTS'] > row['opptPTS']:
        win_loss.append('W')
    else:
        win_loss.append('L')

# Add the win_loss data to the DataFrame
celtics_gm_stats_2['winLoss'] = win_loss

output_file('celtics-gm-linked-selections.html',
            title='Celtics Percentages vs. Win-Loss')

# Store the data in a ColumnDataSource
gm_stats_cds = ColumnDataSource(celtics_gm_stats_2)

# Create a CategoricalColorMapper that assigns specific colors to wins and losses
win_loss_mapper = CategoricalColorMapper(factors = ['W', 'L'], palette=['Green', 'Red'])

# Specify the tools
toolList = ['lasso_select', 'tap', 'reset', 'save']

# Create a figure relating the percentages
pctFig = figure(title='2PT FG % vs 3PT FG %, 2017-18 Regular Season',
                plot_height=400, plot_width=400, tools=toolList,
                x_axis_label='2PT FG%', y_axis_label='3PT FG%')

# Draw with circle markers
pctFig.circle(x='team2P%', y='team3P%', source=gm_stats_cds,
              size=12, color='black')

# Format the y-axis tick labels as percenages
pctFig.xaxis[0].formatter = NumeralTickFormatter(format='00.0%')
pctFig.yaxis[0].formatter = NumeralTickFormatter(format='00.0%')

# Create a figure relating the totals
totFig = figure(title='Team Points vs Opponent Points, 2017-18 Regular Season',
                plot_height=400, plot_width=400, tools=toolList,
                x_axis_label='Team Points', y_axis_label='Opponent Points')

# Draw with square markers
totFig.square(x='teamPTS', y='opptPTS', source=gm_stats_cds, size=10,
              color=dict(field='winLoss', transform=win_loss_mapper))

# Create layout
grid = gridplot([[pctFig, totFig]])

# Visualize
show(grid)
