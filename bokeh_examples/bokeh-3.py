import numpy as np

# Bokeh libraries
from bokeh.io import curdoc
from bokeh.layouts import column, layout
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput
from bokeh.plotting import figure, show
# from bokeh.sampledata.movies_data import movie_path
# My word count data
day_num = np.linspace(1, 10, 10)
daily_words = [450, 628, 488, 210, 287, 791, 508, 639, 397, 943]
cumulative_words = np.cumsum(daily_words)

# Output the visualization directly in the notebook
# output_notebook()

# Create a figure with a datetime type x-axis
fig = figure(title='My Tutorial Progress',
             plot_height=400, plot_width=700,
             x_axis_label='Day Number', y_axis_label='Words Written',
             x_minor_ticks=2, y_range=(0, 6000),
             toolbar_location=None)

genre = Select(title="Genre", value="All",
               options=['Oi', 'Tchau'])

controls = [ genre]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())


# The daily words will be represented as vertical bars (columns)
fig.vbar(x=day_num, bottom=0, top=daily_words,
         color='blue', width=0.75,
         legend='Daily')

# The cumulative sum will be a trend line
fig.line(x=day_num, y=cumulative_words,
         color='gray', line_width=1,
         legend='Cumulative')

# Put the legend in the upper left corner
fig.legend.location = 'top_left'

# Let's check it out
# show(fig)
inputs = column(*controls, width=320, height=1000)
inputs.sizing_mode = "fixed"
l = layout(inputs, sizing_mode="scale_both")

# update()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "Movies"
