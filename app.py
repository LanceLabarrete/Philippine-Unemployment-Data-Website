from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import geopandas as gpd
import plotly.express as px
import pandas as pd
from pathlib import Path
import numpy as np

dataset_folder = Path('dataset/')
unemployment_df = pd.read_excel(dataset_folder / "Data101 Unemployment Rate.xlsx")
unemployment_df.set_index('Region', inplace=True)
unemployment_df = unemployment_df.T.reset_index() 
regions = []

regions = unemployment_df.iloc[:, 0]
regions.tolist()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="#")),
    ],
    brand="UNEMPLOYMENT RATE IN THE PHILIPPINES",
    brand_href="#",
    color="#0A0A0A",
    dark=True,
    brand_style={"font-weight": "bold"}
)



app.layout = html.Div([
    navbar,
    html.Div([
        dbc.Row(children=[
            html.H1(children = "UNEMPLOYMENT DATA", style = {"font-weight": "bold"}),
            html.H6("In the Philippines, the unemployment rate measures the number of people actively looking for a job as a percentage of the labour force."),
            html.P("Choose the region to be displayed on the map and the bar graph."),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': region, 'value': region} for region in unemployment_df.columns[1:]],
                value=unemployment_df.columns[1]  # Default to the first region
            ),
            
            ]), 
        dcc.Graph(id='region-plot')
    ], style={
        'width': '48%',
        'display': 'inline-block',
        'vertical-align': 'top',
        'padding': '10px'
    }),
    
    html.Div([
        dbc.Col(children=[
            html.P("Choose the region to be displayed on the map and the bar graph"),
            # dcc.Dropdown(options=amenity_options, value=amenity_options[0]['value'], id="choropleth-select") 
        ], width=6)  
    ], style={
        'width': '48%',
        'display': 'inline-block',
        'vertical-align': 'top',
        'padding': '10px'
    })
])

@app.callback(
    Output('region-plot', 'figure'),
    Input('region-dropdown', 'value')
)


def update_plot(selected_region):
    # Filter data based on selected region
    filtered_df = unemployment_df[['index', selected_region]]
    filtered_df.columns = ['Date', 'Value']
    
    # Create a Plotly Express bar plot
    fig = px.bar(
        filtered_df,
        x='Date',
        y='Value',
        title=f'Unemployment Data for {selected_region}',
        labels={'Date': 'Date', 'Value': 'Value'}
    )

    
    # Format the x-axis to show Month-Year
    fig.update_xaxes(
        tickformat='%b-%Y',
        title='Date'
    )
    
    return fig

if __name__ == "__main__":
    app.run(debug=True)