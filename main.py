from getdata import getdata
import plotly.graph_objs as go
from parsedata import parse
import numpy as np
from datetime import datetime, date
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)
station = "KIKT"
month_options = []
records = []
min_day = date.today()
max_day= date.today()
app.layout = html.Div([
    html.H1('Wind speed and direction'),
    dcc.Input(
        id='station-input',
        type='text',
        placeholder='Enter station name...',
        value=station,
        style={'width': '50%'}
    ),
    dcc.Dropdown(
        id='month-dropdown',
        options=month_options,
        value=None,  # Initially select the latest month
        clearable=False
    ),
    dcc.Graph(id="nasa-chart"),
    dcc.DatePickerSingle(
        id='date-picker',
        min_date_allowed=min_day,
        max_date_allowed=max_day,
        initial_visible_month=date.today(),
        date=date.today()
    ),
    dcc.Graph(id="daily-chart"),
])


def fetch_data(stat):
    tx = getdata(stat)
    if tx is None:
        return None
    return parse(tx)
@app.callback(
    Output('date-picker', 'max_date_allowed'),
    Input('station-input', 'value')
)
def update_day2(se):
    global min_day
    global max_day
    global records
    if not se:
        return date.today()
    records = fetch_data(se)
    if records is None:
        return []

    min_day = records[-1].date
    max_day = records[0].date
    return max_day

@app.callback(
    Output('date-picker', 'min_date_allowed'),
    Input('station-input', 'value')
)
def update_day(se):
    global min_day
    global max_day
    global records
    if not se:
        return date.today()
    records = fetch_data(se)
    if records is None:
        return []

    min_day = records[-1].date
    max_day = records[0].date
    return min_day


@app.callback(
    Output('month-dropdown', 'options'),
    Input('station-input', 'value')
)
def update_month_options(selected_station):
    global records
    global month_options
    if not selected_station:
        return []

    # Fetch data for the selected station
    records = fetch_data(selected_station)
    if records is None:
        return []

    # Generate month options
    month_options = []
    sl = set()

    for record in records:
        label = record.date.replace(day=1).strftime('%B %Y')
        if label not in sl:
            month_options.append({'label': label, 'value': record.date})
            sl.add(label)

    month_options = sorted(month_options, key=lambda x: x['value'])
    return month_options


@app.callback(
    Output("nasa-chart", "figure"),
    [Input("month-dropdown", "value"),
     Input('station-input', 'value')])
def display(selected_month, selected_station):
    if not selected_month or not selected_station:
        return {
            'data': [],
            'layout': {
                'title': 'No data available',
            }
        }

    selected_month = datetime.fromisoformat(selected_month)

    # Fetch data for the selected station
    records = fetch_data(selected_station)
    if records is None:
        return {}

    # Filter data based on selected month
    filtered_records = [rec for rec in records if rec.date.month == selected_month.month]

    # Extract data for plotting
    dates = [rec.date for rec in filtered_records]
    wspeeds = [rec.wspeed for rec in filtered_records if rec.wspeed is not None and rec.wdir is not None]
    wdirs = [rec.wdir for rec in filtered_records if rec.wdir is not None and rec.wspeed is not None]

    # Create traces for wind speed and direction
    wspeed_trace = go.Scatter(x=dates, y=wspeeds, mode='lines', name='Wind Speed')
    wdir_trace = go.Scatter(x=dates, y=wdirs, mode='lines', name='Wind Direction', yaxis='y2')

    # Layout of the chart
    layout = go.Layout(
        xaxis=dict(title='Date'),
        yaxis=dict(title='Wind Speed (m/s)'),
        yaxis2=dict(title='Wind Direction (degrees)', overlaying='y', side='right')
    )

    # Construct the figure
    fig = go.Figure(data=[wspeed_trace, wdir_trace], layout=layout)
    return fig
@app.callback(
    Output("daily-chart", "figure"),
    [Input("date-picker", "date"),
     Input('station-input', 'value')])
def display(day, selected_station):
    if not day or not selected_station:
        return {
            'data': [],
            'layout': {
                'title': 'No data available',
            }
        }
    day = datetime.fromisoformat(day)
    # Fetch data for the selected station
    records = fetch_data(selected_station)
    if records is None:
        return {}

    # Filter data based on selected month
    filtered_records = [rec for rec in records if rec.date.date() == day.date() and rec.wdir is not None and rec.wspeed is not None]

    # Extract data for plotting
    wspeeds_og = [rec.wspeed for rec in filtered_records if rec.wspeed is not None and rec.wdir is not None]
    wdirs_og = [rec.wdir for rec in filtered_records if rec.wdir is not None and rec.wspeed is not None]
    y = 0
    x = 0
    for s in filtered_records:
        wdir = s.wdir * (np.pi/180)
        mag_y = s.wspeed * np.sin(wdir)
        mag_x = s.wspeed * np.cos(wdir)
        y += mag_y
        x += mag_x
    y /= len(filtered_records)
    x /= len(filtered_records)
    wdirs = np.arctan2(y, x) * (180/np.pi)
    wspeeds = np.sqrt(x**2 + y**2)
    # Create traces for wind speed and direction
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[wspeeds],
        theta=[wdirs],
        mode='markers',
        marker=dict(
            size=10,

        ),
        text=wspeeds,  # Text labels show wind speeds
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                dtick=1,
                range=[0, wspeeds + 1],  # Adjust range if necessary
            ),
            angularaxis=dict(
                tickmode='array',
                tickvals=[0, 90, 180, 270],  # Customize angular tick values as needed
                ticktext=['E', 'N', 'W', 'S'],  # Customize angular tick labels as needed
            )
        )
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
