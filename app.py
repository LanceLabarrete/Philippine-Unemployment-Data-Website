from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import geopandas as gpd
import pandas as pd
from pathlib import Path
dataset_folder = Path('dataset/')
unemployment_df = pd.read_excel(dataset_folder / "Data101 Unemployment Rate.xlsx")
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


app.layout = html.Div(children=[
    navbar, # and add them to the layout
    dbc.Container(children=[
        dbc.Col(children=[
            dbc.Row(children=[
            html.H2(children = "UNEMPLOYMENT DATA", style = {"font-weight": "bold"}),
            html.P("In the Philippines, the unemployment rate measures the number of people actively looking for a job as a percentage of the labour force."),
            html.P("Choose the region to be displayed on the map and the bar graph."),
            dcc.Dropdown(options=regions, value=regions[0], id="region-select")
            ]), 
        ], width=6),

        dbc.Col(children=[
            html.P("Choose the region to be displayed on the map and the bar graph"),
            # dcc.Dropdown(options=amenity_options, value=amenity_options[0]['value'], id="choropleth-select") 
        ], width=6)
        
    ])
])

def getBarChart(region):
    unemployment = unemployment_df[unemployment_df['Region'] == region]
    unemployment = unemployment.loc[unemployment['Region'] == region, 'Region'] = 'Unemployment Rate'

# bar_fig = px.bar(sorted_df, x=selected_value, y=sorted_df.index, # px.bar
#                         color_continuous_scale='teal')

if __name__ == "__main__":
    app.run(debug=True)