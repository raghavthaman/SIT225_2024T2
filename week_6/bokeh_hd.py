import pandas as pd
import numpy as np
from bokeh.plotting import figure, curdoc
from bokeh.models import (ColumnDataSource, Select, Slider, Button, 
                         DataTable, TableColumn, Div, DatetimeTickFormatter)
from bokeh.layouts import column, row
from bokeh.palettes import Category10
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

# Configuration
CSV_FILE = 'gyroscope_data.csv'

# Load initial data
def load_data(file_path=CSV_FILE):
    try:
        data = pd.read_csv(file_path)
        if 'timestamp' not in data.columns:
            data['timestamp'] = pd.to_datetime(data.index, unit='s')
        else:
            data['timestamp'] = pd.to_datetime(data['timestamp'])
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame(columns=['timestamp', 'x', 'y', 'z'])  # Return empty DataFrame in case of error

# Initialize data
data = load_data()
source = ColumnDataSource(data=data)
source_summary = ColumnDataSource(data=dict())

# Create plot
plot = figure(title="Gyroscope Data Dashboard", 
              x_axis_type='datetime',
              x_axis_label='Timestamp', 
              y_axis_label='Angular Velocity (rad/s)',
              sizing_mode='stretch_width',
              tools="pan,box_zoom,wheel_zoom,reset,save",
              toolbar_location="above")

# Configure datetime formatting
plot.xaxis.formatter = DatetimeTickFormatter(
    hours="%H:%M:%S",
    minutes="%H:%M:%S",
    seconds="%H:%M:%S"
)

# Define renderers
renderers = {'x': [], 'y': [], 'z': []}
colors = Category10[3]

# Create widgets
graph_select = Select(title="Graph Type:", value="Line", 
                      options=["Line", "Scatter", "Distribution", "Bar", "Box", "Violin", "Heatmap"])
variable_select = Select(title="Display Variable:", value="All", options=["All", "X", "Y", "Z"])
sample_slider = Slider(title="Samples to Show:", start=10, end=len(data), value=min(100, len(data)), step=10)
prev_button = Button(label="◄ Previous", width=100, button_type="primary")
next_button = Button(label="Next ►", width=100, button_type="primary")
auto_update = Button(label="Auto Update: OFF", button_type="default", width=150)
status_div = Div(text=f"<p>Loaded {len(data)} samples from {CSV_FILE}</p>", width=400)

# Create data table
columns = [
    TableColumn(field="timestamp", title="Timestamp"),
    TableColumn(field="x", title="X-axis"),
    TableColumn(field="y", title="Y-axis"),
    TableColumn(field="z", title="Z-axis")
]
data_table = DataTable(source=source, columns=columns, width=800, height=300)

# Create summary table
summary_columns = [
    TableColumn(field="stat", title="Statistic"),
    TableColumn(field="x", title="X-axis"),
    TableColumn(field="y", title="Y-axis"),
    TableColumn(field="z", title="Z-axis")
]
summary_table = DataTable(source=source_summary, columns=summary_columns, width=800, height=150)

# Update function with fixed graph types
def update_data():
    global data, renderers, plot
    try:
        # Reload data if file has changed
        if os.path.exists(CSV_FILE):
            current_modified = os.path.getmtime(CSV_FILE)
            if not hasattr(update_data, 'last_modified') or current_modified > update_data.last_modified:
                new_data = load_data()
                if not new_data.empty:
                    data = new_data
                    sample_slider.end = len(data)
                    update_data.last_modified = current_modified
                    status_div.text = f"<p>Loaded {len(data)} samples from {CSV_FILE} (updated)</p>"

        # Get current display settings
        samples = sample_slider.value
        var = variable_select.value
        graph_type = graph_select.value
        
        # Update data source
        display_data = data.tail(samples)
        source.data = dict(
            timestamp=display_data['timestamp'],
            x=display_data['x'],
            y=display_data['y'],
            z=display_data['z']
        )
        
        # Update summary data
        summary = display_data[['x', 'y', 'z']].describe().reset_index()
        summary.columns = ['stat'] + list(summary.columns[1:])
        source_summary.data = summary

        # Clear previous renderers
        for axis in renderers:
            for r in renderers[axis]:
                plot.renderers.remove(r)
            renderers[axis] = []

        # Adjust plot axes based on graph type
        plot.xaxis.axis_label = "Timestamp" if graph_type in ["Line", "Scatter", "Bar"] else "Variable/Value"
        plot.yaxis.axis_label = "Angular Velocity (rad/s)" if graph_type in ["Line", "Scatter", "Bar"] else "Value/Count"

        # Plot based on graph type
        if graph_type == "Line":
            if var in ["All", "X"]:
                renderers['x'] = [plot.line('timestamp', 'x', source=source, color=colors[0], legend_label="X", line_width=2)]
            if var in ["All", "Y"]:
                renderers['y'] = [plot.line('timestamp', 'y', source=source, color=colors[1], legend_label="Y", line_width=2)]
            if var in ["All", "Z"]:
                renderers['z'] = [plot.line('timestamp', 'z', source=source, color=colors[2], legend_label="Z", line_width=2)]

        elif graph_type == "Scatter":
            if var in ["All", "X"]:
                renderers['x'] = [plot.scatter('timestamp', 'x', source=source, color=colors[0], legend_label="X", size=8)]
            if var in ["All", "Y"]:
                renderers['y'] = [plot.scatter('timestamp', 'y', source=source, color=colors[1], legend_label="Y", size=8)]
            if var in ["All", "Z"]:
                renderers['z'] = [plot.scatter('timestamp', 'z', source=source, color=colors[2], legend_label="Z", size=8)]

        elif graph_type == "Distribution":
            plot.x_range.start = None  # Reset range for non-datetime
            plot.x_range.end = None
            plot.xaxis.axis_label = "Value"
            plot.yaxis.axis_label = "Count"
            for axis in ['x', 'y', 'z']:
                if var in ["All", axis.upper()]:
                    hist, edges = np.histogram(display_data[axis], bins=20)
                    renderers[axis] = [plot.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], 
                                                fill_color=colors[['x', 'y', 'z'].index(axis)], 
                                                line_color="white", legend_label=axis.upper())]

        elif graph_type == "Bar":
            # Adjust bar width based on time range
            time_range = (display_data['timestamp'].max() - display_data['timestamp'].min()).total_seconds() * 1000
            bar_width = time_range / samples * 0.8 if samples > 0 else 0.9
            if var in ["All", "X"]:
                renderers['x'] = [plot.vbar(x='timestamp', top='x', source=source, width=bar_width, 
                                           fill_color=colors[0], legend_label="X")]
            if var in ["All", "Y"]:
                renderers['y'] = [plot.vbar(x='timestamp', top='y', source=source, width=bar_width, 
                                           fill_color=colors[1], legend_label="Y")]
            if var in ["All", "Z"]:
                renderers['z'] = [plot.vbar(x='timestamp', top='z', source=source, width=bar_width, 
                                           fill_color=colors[2], legend_label="Z")]

        elif graph_type == "Box":
            plot.xaxis.axis_label = "Variable"
            plot.yaxis.axis_label = "Value"
            plot.x_range.start = None  # Reset datetime range
            plot.x_range.end = None
            plot.xaxis[0].ticker = [0, 1, 2]  # Fixed positions for x, y, z
            plot.xaxis.major_label_overrides = {0: "X", 1: "Y", 2: "Z"}
            for i, axis in enumerate(['x', 'y', 'z']):
                if var in ["All", axis.upper()]:
                    q1, q2, q3 = display_data[axis].quantile([0.25, 0.5, 0.75])
                    iqr = q3 - q1
                    upper = min(q3 + 1.5 * iqr, display_data[axis].max())
                    lower = max(q1 - 1.5 * iqr, display_data[axis].min())
                    renderers[axis] = [
                        plot.vbar(x=[i], top=[q3], bottom=[q1], width=0.4, fill_color=colors[i], legend_label=axis.upper()),
                        plot.segment(x0=[i], y0=[lower], x1=[i], y1=[upper], color="black"),
                        plot.scatter(x=[i], y=[q2], size=10, color="black", legend_label=axis.upper() + " Median")
                    ]

        elif graph_type == "Violin":
            plot.xaxis.axis_label = "Variable"
            plot.yaxis.axis_label = "Density"
            plot.x_range.start = None
            plot.x_range.end = None
            plot.xaxis[0].ticker = [0, 1, 2]
            plot.xaxis.major_label_overrides = {0: "X", 1: "Y", 2: "Z"}
            for i, axis in enumerate(['x', 'y', 'z']):
                if var in ["All", axis.upper()]:
                    hist, edges = np.histogram(display_data[axis], bins=20, density=True)
                    hist = hist / hist.max() * 0.4  # Normalize and scale width
                    for h, left, right in zip(hist, edges[:-1], edges[1:]):
                        renderers[axis].append(plot.quad(top=right, bottom=left, left=i-h, right=i+h, 
                                                        fill_color=colors[i], alpha=0.5, legend_label=axis.upper()))

        elif graph_type == "Heatmap":
            plot.xaxis.axis_label = "Time Index"
            plot.yaxis.axis_label = "Variable"
            plot.x_range.start = None
            plot.y_range.start = None
            hm_data = display_data[['x', 'y', 'z']].values.T
            x_indices = np.arange(len(display_data))
            y_indices = [0, 1, 2]  # For x, y, z
            x_grid, y_grid = np.meshgrid(x_indices, y_indices)
            hm_source = ColumnDataSource(dict(
                x=x_grid.flatten(),
                y=y_grid.flatten(),
                values=hm_data.flatten()
            ))
            plot.grid.grid_line_color = None
            renderers['x'] = [plot.rect(x='x', y='y', width=1, height=1, source=hm_source, 
                                       fill_color={'field': 'values', 'transform': {'palette': "Viridis256"}},
                                       line_color=None)]

        plot.legend.location = "top_left"
        plot.legend.click_policy = "hide"
        plot.legend.background_fill_alpha = 0.5

    except Exception as e:
        status_div.text = f"<p style='color:red'>Error updating data: {str(e)}</p>"
        print(f"Update error: {e}")

# Callback functions
def variable_change(attrname, old, new):
    update_data()

def sample_change(attrname, old, new):
    update_data()

def graph_change(attrname, old, new):
    update_data()

def prev_button_click():
    current = sample_slider.value
    if current > sample_slider.start:
        sample_slider.value = current - sample_slider.step

def next_button_click():
    current = sample_slider.value
    if current < sample_slider.end:
        sample_slider.value = current + sample_slider.step

def toggle_auto_update():
    if auto_update.label == "Auto Update: OFF":
        auto_update.label = "Auto Update: ON"
        auto_update.button_type = "success"
        curdoc().add_periodic_callback(update_data, 2000)
    else:
        auto_update.label = "Auto Update: OFF"
        auto_update.button_type = "default"
        curdoc().remove_periodic_callback(update_data)

# Set up callbacks
graph_select.on_change('value', graph_change)
variable_select.on_change('value', variable_change)
sample_slider.on_change('value', sample_change)
prev_button.on_click(prev_button_click)
next_button.on_click(next_button_click)
auto_update.on_click(toggle_auto_update)

# File watcher setup
class CSVHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(CSV_FILE):
            update_data()

if os.path.exists(CSV_FILE):
    observer = Observer()
    observer.schedule(CSVHandler(), path='.', recursive=False)
    observer.start()
    update_data.last_modified = os.path.getmtime(CSV_FILE)
else:
    status_div.text = f"<p style='color:red'>Warning: {CSV_FILE} not found</p>"

# Initial update
update_data()

# Create layout
header = Div(text="<h1 style='text-align:center'>Gyroscope Data Dashboard</h1>")
controls_top = row(graph_select, variable_select, sample_slider, status_div)
controls_bottom = row(prev_button, next_button, auto_update)
layout = column(
    header,
    controls_top,
    controls_bottom,
    plot,
    Div(text="<h3>Current Data</h3>"),
    data_table,
    Div(text="<h3>Statistics</h3>"),
    summary_table
)

# Add to document
curdoc().add_root(layout)
curdoc().title = "Gyroscope Dashboard"