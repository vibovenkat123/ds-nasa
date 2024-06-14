import dash
from dash import dcc, html
import plotly.graph_objects as go

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Wind Speed and Direction Dashboard"),
    html.Label("Platform Name:"),
    dcc.Input(id='platform-name', type='text'),

    dcc.Graph(id='time-series-plot'),

    html.Label("Select Day:"),
    dcc.Dropdown(
        id='day-selector',
        options=[{'label': day, 'value': day} for day in days],
        value=days[0]
    ),

    dcc.Graph(id='polar-plot'),

    html.H2("Forecast for the Next 72 Hours"),
    dcc.Graph(id='forecast-plot')
])


@app.callback(
    [dash.dependencies.Output('time-series-plot', 'figure'),
     dash.dependencies.Output('polar-plot', 'figure'),
     dash.dependencies.Output('forecast-plot', 'figure')],
    [dash.dependencies.Input('platform-name', 'value'),
     dash.dependencies.Input('day-selector', 'value')]
)
def update_dashboard(platform_name, selected_day):
    # Fetch and process data for the given platform name
    # Update figures accordingly
    pass


if __name__ == '__main__':
    app.run_server(debug=True)
