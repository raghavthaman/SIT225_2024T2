import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load gyroscope data from CSV
df = pd.read_csv('gyroscope_data.csv')

# Initialize Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Gyroscope Data Visualization"),
    
    # Dropdown for graph type
    dcc.Dropdown(
        id='graph-type',
        options=[
            {'label': 'Scatter Plot', 'value': 'scatter'},
            {'label': 'Line Chart', 'value': 'line'},
            {'label': 'Distribution Plot', 'value': 'histogram'},
            {'label': 'Bar Chart', 'value': 'bar'},
            {'label': 'Box Plot', 'value': 'box'},
            {'label': 'Violin Plot', 'value': 'violin'},
            {'label': 'Heatmap', 'value': 'heatmap'}
        ],
        value='scatter'  # Default value
    ),
    
    # Dropdown for variable selection
    dcc.Dropdown(
        id='variable-select',
        options=[
            {'label': 'X', 'value': 'x'},
            {'label': 'Y', 'value': 'y'},
            {'label': 'Z', 'value': 'z'},
            {'label': 'All', 'value': 'all'}
        ],
        value='all'  # Default value
    ),
    
    # Text box for sample selection
    dcc.Input(id='sample-size', type='number', value=100),
    
    # Navigation buttons
    html.Button('Previous', id='prev-button', n_clicks=0),
    html.Button('Next', id='next-button', n_clicks=0),
    
    # Graph
    dcc.Graph(id='gyroscope-graph'),
    
    # Summary table
    html.Div(id='summary-table')
])

# Callback to update graph and summary table
@app.callback(
    [Output('gyroscope-graph', 'figure'),
     Output('summary-table', 'children')],
    [Input('graph-type', 'value'),
     Input('variable-select', 'value'),
     Input('sample-size', 'value'),
     Input('prev-button', 'n_clicks'),
     Input('next-button', 'n_clicks')]
)
def update_graph(graph_type, variable, sample_size, prev_clicks, next_clicks):
    # Calculate start and end index for data slicing
    total_samples = len(df)
    start_idx = (prev_clicks - next_clicks) * sample_size
    end_idx = start_idx + sample_size
    
    # Ensure indices are within bounds
    start_idx = max(0, start_idx)
    end_idx = min(total_samples, end_idx)
    
    # Slice data
    sliced_df = df.iloc[start_idx:end_idx]
    
    # Select variables
    if variable == 'all':
        columns = ['x', 'y', 'z']
    else:
        columns = [variable]
    
    # Create graph based on selected type
    if graph_type == 'scatter':
        fig = px.scatter(sliced_df, x=sliced_df.index, y=columns, title='Scatter Plot of Gyroscope Data')
    elif graph_type == 'line':
        fig = px.line(sliced_df, x=sliced_df.index, y=columns, title='Line Chart of Gyroscope Data')
    elif graph_type == 'histogram':
        fig = px.histogram(sliced_df, x=columns, title='Distribution Plot of Gyroscope Data')
    elif graph_type == 'bar':
        fig = px.bar(sliced_df, x=sliced_df.index, y=columns, title='Bar Chart of Gyroscope Data')
    elif graph_type == 'box':
        fig = px.box(sliced_df, y=columns, title='Box Plot of Gyroscope Data')
    elif graph_type == 'violin':
        fig = px.violin(sliced_df, y=columns, title='Violin Plot of Gyroscope Data')
    elif graph_type == 'heatmap':
        # Heatmap requires a pivot table or correlation matrix
        corr_matrix = sliced_df[columns].corr()
        fig = px.imshow(corr_matrix, text_auto=True, title='Heatmap of Gyroscope Data')
    
    # Create summary table
    summary = sliced_df[columns].describe().reset_index()
    table = html.Table([
        html.Thead(html.Tr([html.Th(col) for col in summary.columns])),
        html.Tbody([
            html.Tr([html.Td(summary.iloc[i][col]) for col in summary.columns])
            for i in range(len(summary))
        ])
    ])
    
    return fig, table

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)