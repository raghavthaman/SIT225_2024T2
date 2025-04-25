import threading
import time
from arduino_iot_cloud import ArduinoCloudClient
from smooth_dash_wrapper import create_smooth_dash_app
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# --- Arduino IoT Credentials ---
DEVICE_ID = "5e48c1f8-1778-4e32-8731-5300d17dcbc5"
SECRET_KEY = "AwZkk2oLmWoWWU@IsgOPburTc"

# --- Data Buffer ---
buffer = {"x": [], "y": [], "z": [], "timestamp": []}
BUFFER_SIZE = 200

# --- Live Vars ---
x, y, z = 0, 0, 0

# --- Arduino Callbacks ---
def on_x(client, value): global x; x = value
def on_y(client, value): global y; y = value
def on_z(client, value): global z; z = value

# --- Arduino Stream Thread ---
def start_arduino_stream():
    global x, y, z
    client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY, sync_mode=True)
    client.register("py_X", value=None, on_write=on_x)
    client.register("py_Y", value=None, on_write=on_y)
    client.register("py_Z", value=None, on_write=on_z)
    client.start()

    while True:
        client.update()
        timestamp = time.time()

        if x is not None and y is not None and z is not None:
            buffer['x'].append(x)
            buffer['y'].append(y)
            buffer['z'].append(z)
            buffer['timestamp'].append(timestamp)

            if len(buffer['x']) > BUFFER_SIZE:
                for k in buffer:
                    buffer[k] = buffer[k][-BUFFER_SIZE:]

            x, y, z = None, None, None

        time.sleep(0.05)  # ~20 Hz

# --- Dash App Layout & Callbacks ---
app = Dash(__name__)
app.layout = html.Div([
    html.H3("📱 Live Accelerometer Data (Smooth Plot)"),
    dcc.Graph(id='live-graph', animate=False),
    dcc.Interval(id='interval', interval=100, n_intervals=0)
])

@app.callback(
    Output('live-graph', 'figure'),
    Input('interval', 'n_intervals')
)
def update_graph(n):
    fig = go.Figure()
    if len(buffer['x']) < 2:
        return fig

    fig.add_trace(go.Scatter(y=buffer['x'], name='X', mode='lines', line_shape='spline'))
    fig.add_trace(go.Scatter(y=buffer['y'], name='Y', mode='lines', line_shape='spline'))
    fig.add_trace(go.Scatter(y=buffer['z'], name='Z', mode='lines', line_shape='spline'))

    fig.update_layout(
        title='Accelerometer X/Y/Z',
        xaxis_title='Sample Index',
        yaxis_title='Acceleration (g)',
        uirevision='true'
    )
    return fig

# --- Start Everything ---
if __name__ == '__main__':
    threading.Thread(target=start_arduino_stream, daemon=True).start()
    app.run_server(debug=True)
