import random

from bokeh.driving import linear
from bokeh.layouts import column
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, curdoc

# Create ColumnDataSource that will be used by the plot
source = ColumnDataSource({"time": [], "value": [], "average": []})

# Create a callback function
@linear(m=1, b=0)
def update(step):
    new_value = random.random()
    new_data = {"time": [step], "value": [new_value]}

    recent_values = list(source.data["value"]) + [new_value]
    if len(recent_values) >= 3:
        recent_values = recent_values[-3:]
    avg_val = sum(recent_values) / len(recent_values)
    new_data["average"] = [avg_val]
    
    # Update the ColumnDataSource with the new values
    source.stream(new_data, rollover=200)

plot = figure(sizing_mode="stretch_both", tools="", toolbar_location=None)
plot.line('time', 'value', source=source, color="blue", legend_label="Value")
plot.line('time', 'average', source=source, color='red', legend_label="MA(3)")

plot.xaxis.axis_label_text_font_size = "20pt"
plot.yaxis.axis_label_text_font_size = "20pt"
plot.xaxis.major_label_text_font_size = "16pt"
plot.yaxis.major_label_text_font_size = "16pt"

curdoc().add_periodic_callback(update, 2000)

layout = column(plot, sizing_mode="stretch_both", margin=20)
curdoc().add_root(layout)
