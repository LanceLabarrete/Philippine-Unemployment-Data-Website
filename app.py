from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from pathlib import Path
import numpy as np

# Load the data
dataset_folder = Path('dataset/')
unemployment_df = pd.read_excel(dataset_folder / "Data101 Unemployment Rate.xlsx")

# Classify regions
luzon_regions = [
    "National Capital Region (NCR)", "Cordillera Administrative Region (CAR)",
    "Region I (Ilocos Region)", "Region II (Cagayan Valley)",
    "Region III (Central Luzon)", "Region IV-A (CALABARZON)",
    "MIMAROPA Region", "Region V (Bicol Region)"
]

visayas_regions = [
    "Region VI (Western Visayas)", "Region VII (Central Visayas)", "Region VIII (Eastern Visayas)"
]

mindanao_regions = [
    "Region IX (Zamboanga Peninsula)", "Region X (Northern Mindanao)",
    "Region XI (Davao Region)", "Region XII (SOCCSKSARGEN)",
    "Region XIII (Caraga)", "Bangsamoro Autonomous Region in Muslim Mindanao (BARMM)"
]

# Calculate average unemployment rates
unemployment_df_avg = unemployment_df.set_index('Region').mean(axis=1).reset_index()
unemployment_df_avg.columns = ['Region', 'Average_Unemployment_Rate']

# Assign output values
output_values = {
    "National Capital Region (NCR)": 250,
    "Cordillera Administrative Region (CAR)": 50,
    "Region I (Ilocos Region)": 70,
    "Region II (Cagayan Valley)": 60,
    "Region III (Central Luzon)": 200,
    "Region IV-A (CALABARZON)": 220,
    "MIMAROPA Region": 30,
    "Region V (Bicol Region)": 40,
    "Region VI (Western Visayas)": 100,
    "Region VII (Central Visayas)": 120,
    "Region VIII (Eastern Visayas)": 90,
    "Region IX (Zamboanga Peninsula)": 40,
    "Region X (Northern Mindanao)": 80,
    "Region XI (Davao Region)": 110,
    "Region XII (SOCCSKSARGEN)": 70,
    "Region XIII (Caraga)": 40,
    "Bangsamoro Autonomous Region in Muslim Mindanao (BARMM)": 20
}

# Add output values to the dataframe
unemployment_df_avg['Output'] = unemployment_df_avg['Region'].map(output_values)

# Filter regions by Luzon, Visayas, and Mindanao
unemployment_df_avg['Group'] = np.where(unemployment_df_avg['Region'].isin(luzon_regions), 'Luzon', 
                                        np.where(unemployment_df_avg['Region'].isin(visayas_regions), 'Visayas', 'Mindanao'))

# Transpose the dataframe for the dropdown and bar plot
unemployment_df_t = unemployment_df.T.reset_index()
unemployment_df_t.columns = ['index'] + list(unemployment_df.index)

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
            html.H1(children="UNEMPLOYMENT DATA", style={"font-weight": "bold"}),
            html.H6("In the Philippines, the unemployment rate measures the number of people actively looking for a job as a percentage of the labour force."),
            html.P("Choose the region to be displayed on the map and the bar graph."),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': region, 'value': region} for region in unemployment_df_t.columns[1:]],
                value=unemployment_df_t.columns[1]  # Default to the first region
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
            html.H1("Correlation Graph", style={"font-weight": "bold"}),
            html.P("This graph shows the correlation between average unemployment rates and output per region."),
            dcc.Graph(id='correlation-plot')
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
    filtered_df = unemployment_df_t[['index', selected_region]]
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

@app.callback(
    Output('correlation-plot', 'figure'),
    Input('region-dropdown', 'value')
)
def update_correlation(selected_region):
    fig = px.scatter(
        unemployment_df_avg,
        x='Average_Unemployment_Rate',
        y='Output',
        color='Group',
        title='Correlation between Average Unemployment Rates and Output per Region',
        labels={'Average_Unemployment_Rate': 'Average Unemployment Rate (%)', 'Output': 'Output'}
    )
    return fig

if __name__ == "__main__":
    app.run(debug=True)
