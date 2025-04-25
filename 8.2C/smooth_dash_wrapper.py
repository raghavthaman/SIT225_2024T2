from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

def create_smooth_dash_app(buffer, title="Live Sensor Data", refresh_interval=200):
    app = Dash(__name__)
    app.layout = html.Div([
        html.H3(f" {title}"),
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(id='interval', interval=refresh_interval, n_intervals=0)
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

    return app
