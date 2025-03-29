import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load the processed data
df = pd.read_csv('formatted_sales.csv')
df['date'] = pd.to_datetime(df['date'])

# Create Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div([
    html.H1("Soul Foods Pink Morsel Sales Analysis", 
            style={'textAlign': 'center', 'color': '#7FDBFF'}),
    
    html.Div([
        html.P("This visualization shows Pink Morsel sales before and after the price increase on January 15, 2021.",
               style={'textAlign': 'center', 'fontSize': 18})
    ]),
    
    dcc.Graph(
        id='sales-chart',
        figure=px.line(
            df.sort_values('date'),
            x='date',
            y='sales',
            color='region',
            title='Pink Morsel Daily Sales by Region',
            labels={
                'date': 'Date',
                'sales': 'Sales ($)',
                'region': 'Region'
            }
        ).update_layout(
            plot_bgcolor='#f8f9fa',
            paper_bgcolor='#f8f9fa',
            xaxis_title='Date',
            yaxis_title='Sales ($)',
            title_x=0.5
        )
    ),
    
    html.Div([
        html.H3("Key Insight:", style={'color': '#FF851B'}),
        html.P("Sales were clearly HIGHER AFTER the price increase on January 15, 2021.", 
               style={'fontSize': 16, 'fontWeight': 'bold'})
    ], style={'textAlign': 'center', 'marginTop': 20})
])

if __name__ == '__main__':
    app.run()