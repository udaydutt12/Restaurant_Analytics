from dash import Dash
from dash.dependencies import Input, Output
from datetime import datetime as dt
import dash_html_components as html
import dash_core_components as dcc
from create_db import getClient

db = getClient().restaurant_data
app = Dash(__name__)

store_codes = {
    'A': 'All Stores',
    'S': 'Saunders',
    'M': 'McPherson',
    'L': 'Loop 20',
    'D': 'Del Mar'
}

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Saunders', 'value': 'S'},
            {'label': 'McPherson', 'value': 'M'},
            {'label': 'Loop 20', 'value': 'L'},
            {'label': 'Del Mar', 'value': 'D'},
            {'label': 'All Stores', 'value': 'A'}
        ]
    ),
    dcc.DatePickerSingle(
        id = 'day-picker',
        min_date_allowed = dt(2017, 1, 1),
        max_date_allowed = dt(2020, 6, 10),
        initial_visible_month = dt(2020, 1, 1),
        date = dt(2020, 1, 1).date()
    ),
    dcc.Graph(
        id = 'hourly-breakdown'
    )
])

@app.callback(
    Output('hourly-breakdown', 'figure'),
    [Input('day-picker', 'date'),
     Input('dropdown', 'value')]
)
def output_figure(date, value):
    if value == None:
        return {}
    year, month, day = tuple(date.split('-'))
    collection = db[year]
    date = month + day + year
    x = list(range(24))
    y = []
    if value == 'A':
        query = {
            '_id': {'$regex': '^' + date}
        }
        for document in collection.find(query):
            for i in range(24):
                if len(y) == 24:
                    y[i] += document['HourlyBreakdown'][str(i)]['NetSales']
                else:
                    y.append(document['HourlyBreakdown'][str(i)]['NetSales'])
    else:
        document = collection.find_one({
            '_id': date + value
        })
        for i in range(24):
            y.append(document['HourlyBreakdown'][str(i)]['NetSales'])
    return {
        'data': [
            {'x': x, 'y': y, 'type': 'bar', 'name': store_codes[value]}
        ],
        'layout': {
            'title': 'Net Sales Hourly Breakdown'
        }
    }

if __name__ == '__main__':
    app.run_server(debug=True)

