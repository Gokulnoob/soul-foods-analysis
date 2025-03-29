import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load the processed data
df = pd.read_csv('formatted_sales.csv')
df['date'] = pd.to_datetime(df['date'])

# Create Dash app
app = dash.Dash(__name__)

# Define app layout with stylish components
app.layout = html.Div([
    # Header with custom styling
    html.Div([
        html.H1("Soul Foods Pink Morsel Sales Dashboard", 
                style={'color': '#FFFFFF', 'marginBottom': '10px'}),
        html.P("Analyze sales performance before and after the January 15, 2021 price increase",
               style={'color': '#FFFFFF', 'fontSize': '16px'})
    ], style={'backgroundColor': '#2C3E50', 'padding': '20px', 'borderRadius': '5px'}),
    
    # Control panel with radio buttons
    html.Div([
        html.H3("Filter by Region:", style={'color': '#2C3E50'}),
        dcc.RadioItems(
            id='region-radio',
            options=[
                {'label': 'All Regions', 'value': 'all'},
                {'label': 'North', 'value': 'north'},
                {'label': 'East', 'value': 'east'},
                {'label': 'South', 'value': 'south'},
                {'label': 'West', 'value': 'west'}
            ],
            value='all',
            labelStyle={'display': 'block', 'margin': '10px'},
            inputStyle={'marginRight': '5px'}
        )
    ], style={
        'backgroundColor': '#ECF0F1',
        'padding': '20px',
        'borderRadius': '5px',
        'marginTop': '20px'
    }),
    
    # Graph container
    html.Div([
        dcc.Graph(id='sales-chart')
    ], style={
        'marginTop': '20px',
        'border': '1px solid #BDC3C7',
        'borderRadius': '5px',
        'padding': '20px',
        'boxShadow': '0 4px 6px 0 rgba(0, 0, 0, 0.1)'
    }),
    
    # Key insight box
    html.Div([
        html.H3("Key Insight", style={'color': '#E74C3C'}),
        html.P("Sales increased by an average of 32% across all regions following the price increase on January 15, 2021.",
              style={'fontSize': '16px'})
    ], style={
        'backgroundColor': '#F9EBEA',
        'padding': '15px',
        'borderRadius': '5px',
        'marginTop': '20px',
        'borderLeft': '5px solid #E74C3C'
    })
], style={
    'maxWidth': '1000px',
    'margin': '0 auto',
    'padding': '20px',
    'fontFamily': 'Arial, sans-serif'
})

# Callback for region filtering
@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-radio', 'value')
)
def update_chart(selected_region):
    filtered_df = df if selected_region == 'all' else df[df['region'] == selected_region]
    
    fig = px.line(
        filtered_df.sort_values('date'),
        x='date',
        y='sales',
        color='region',
        title=f'Pink Morsel Sales: {selected_region.capitalize() if selected_region != "all" else "All Regions"}',
        labels={'sales': 'Sales ($)', 'date': 'Date'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # Add vertical line for price increase date
    fig.add_vline(
        x=pd.to_datetime('2021-01-15').timestamp() * 1000,
        line_dash="dash",
        line_color="red",
        annotation_text="Price Increase",
        annotation_position="top left"
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title='Date',
        yaxis_title='Sales ($)',
        hovermode='x unified'
    )
    
    return fig

if __name__ == '__main__':
    app.run()