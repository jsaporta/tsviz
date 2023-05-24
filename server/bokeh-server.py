import json
import time

from confluent_kafka import Consumer
from bokeh.driving import linear
from bokeh.layouts import column
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, curdoc

time.sleep(0.5)

# Create Kafka Consumer
c = Consumer({
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
})

c.subscribe(['raw-data'])

# Create ColumnDataSource that will be used by the plot
source = ColumnDataSource({"time": [], "value": [], "average": []})

# Create a callback function
@linear(m=1, b=0)
def update(step):
    # Poll Kafka for new data
    msg = c.poll(1.0)

    if msg is None:
        return
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        return

    # Parse message and update data
    data = json.loads(msg.value())
    new_value = data['value']
    new_data = {"time": [step], "value": [new_value]}

    recent_values = list(source.data["value"]) + [new_value]
    if len(recent_values) >= 3:
        recent_values = recent_values[-3:]
    avg_val = sum(recent_values) / len(recent_values)
    new_data["average"] = [avg_val]

    # Update the ColumnDataSource with the new values
    source.stream(new_data, rollover=200)

# Create the plot
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
