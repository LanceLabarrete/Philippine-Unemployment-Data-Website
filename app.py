from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import geopandas as gpd
import plotly.express as px
import pandas as pd
from pathlib import Path
import numpy as np
from datetime import datetime
import traceback

dataset_folder = Path('dataset/')
unemployment_df = pd.read_csv(dataset_folder / "Data101 Unemployment Rate.csv")
# unemployment_df['index'] = pd.to_datetime(unemployment_df['index'])

map = gpd.read_file(dataset_folder / "PH_Adm1_Regions.shp.shp")
regions = []

unemployment_df.set_index('Region', inplace=True)
unemployment_df = unemployment_df.T.reset_index() 
unemployment_df2 = pd.read_csv(dataset_folder / "Data101 Unemployment Rate.csv")

# unemployment_df2['index'] = pd.to_datetime(unemployment_df2['index'])

merged_gdf = map.merge(unemployment_df2, left_on='adm1_en', right_on='Region', how='left')
merged_gdf = merged_gdf.to_crs(epsg=4326)
regions = unemployment_df.iloc[:, 0]
regions.tolist()

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
unemployment_df_avg = unemployment_df2.set_index('Region').mean(axis=1).reset_index()
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
unemployment_df_avg['Group'] = np.where(unemployment_df_avg['Region'].isin(luzon_regions), 'Luzon', np.where(unemployment_df_avg['Region'].isin(visayas_regions), 'Visayas', 'Mindanao'))

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

px.set_mapbox_access_token(open(".mapbox_token").read())

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
        dbc.Row(children = [
            dbc.Col(children = [dcc.Loading(id="map-loading2", children=dcc.Graph(id='region-plot')),
            # html.H1("Correlation Graph", style={"font-weight": "bold"}),
            # html.P("This graph shows the correlation between average unemployment rates and output per region."),
              ]),
            dbc.Col(children=[dcc.Graph(id='correlation-plot')])
             
        ])
        
    ], style={
        'width': '68%',
        'display': 'inline-block',
        'vertical-align': 'top',
        'padding': '10px'
    }),
    
    html.Div([
        dbc.Col(children=[
            html.P("Choose the quarter to be displayed on the map and the bar graph"),
            dcc.Dropdown(
                id='date-dropdown',
                options=[{'label': str(col), 'value': str(col)} for col in unemployment_df2.columns if col != 'Region'],
                value=unemployment_df2.columns[1]
            ),
            dcc.Loading(id="map-loading", children=dcc.Graph(id='map-graph', style={'height': '500px', 'width': '100%'}))
        ])  

    ], style={
        'width': '28%',
        'display': 'inline-block',
        'vertical-align': 'top',
        'padding': '10px'
    })
])

@app.callback(
    Output('region-plot', 'figure'),
    Output('correlation-plot', 'figure'),
    Output('map-graph', 'figure'),
    Input('region-dropdown', 'value'),
    Input('date-dropdown', 'value')
)


def update_plots(selected_region, selected_date):
    
    try:
        # Update region plot
        filtered_df = unemployment_df[['index', selected_region]]
        filtered_df.columns = ['Date', 'Value']
        
        fig_region = px.line(
            filtered_df,
            x='Date',
            y='Value',
            title=f'Unemployment Rate for {selected_region}',
            labels={'Date': 'Date', 'Value': 'Unemployment Rate'}
        )
        
        fig_region.update_xaxes(
            tickformat='%b-%Y',
            title='Date'
        )
       
        fig_corr = px.scatter(
        unemployment_df_avg,
        x='Average_Unemployment_Rate',
        y='Output',
        color='Group',
        title='Correlation Graph',
        labels={'Average_Unemployment_Rate': 'Average Unemployment Rate (%)', 'Output': 'Output'}
        )


        fig_map = update_map(selected_date)
    
        return fig_region, fig_corr, fig_map
    except Exception as e:
        print(f"An error occurred: {e}")
        print(traceback.format_exc())
        raise


# @app.callback(
#     Output('map-graph', 'figure'),
#     Input('date-dropdown', 'value')
# )
def update_map(selected_column):
    selected_date = str(selected_column)
    fig = px.choropleth_mapbox(
        merged_gdf,
        geojson=merged_gdf.geometry,
        locations=merged_gdf.index,
        color=selected_column,
        hover_name='adm1_en',
        mapbox_style="carto-positron",
        zoom=3,
        center={"lat": merged_gdf.geometry.centroid.y.mean(), "lon": merged_gdf.geometry.centroid.x.mean()},
        opacity=0.5
    )
    print('////////////////////////////////////////////////////////////////////')
        
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


    
if __name__ == "__main__":
    app.run(debug=True)
