# Import relevant libraries
import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

# Sample data for charts
data_bar = {
    "Country": ["Germany", "France", "Italy", "Spain", "Netherlands", "Belgium"],
    "Solar Consumption": [468, 302, 256, 198, 126, 98],
}
data_pie = {
    "Country": ["Germany", "France", "Italy", "Spain", "Poland", "Netherlands"],
    "GDP": [38.44, 20.0, 18.43, 12.0, 8.5, 6.8],
}
data_line = {
    "Year": [2000, 2005, 2010, 2015, 2020],
    "GDP": [5.0, 7.0, 9.0, 14.2, 16.7],
}

# Create DataFrames
df_bar = pd.DataFrame(data_bar)
df_pie = pd.DataFrame(data_pie)
df_line = pd.DataFrame(data_line)

# Create charts
fig_bar = px.bar(df_bar, x="Country", y="Solar Consumption", title="Solar Consumption by Country")
fig_pie = px.pie(df_pie, names="Country", values="GDP", title="GDP by Country")
fig_line = px.line(df_line, x="Year", y="GDP", title="GDP Over Time")
fig_bar2 = px.bar(df_bar, x="Country", y="Solar Consumption", title="Electricity Generation by Country")
fig_pie2 = px.pie(df_pie, names="Country", values="GDP", title="Carbon Emission by Country")
fig_line2 = px.line(df_line, x="Year", y="GDP", title="Energy Usage Over Time")

 # Load dataset
data = pd.read_csv('winequality-red.csv')


# Create the Dash app
app = dash.Dash(__name__)
server = app.server



# Layout for the app
app.layout = html.Div([
    # Header Section
    html.Div([
        # Title and Subtitle
        html.H1("World Energy Dashboard", style={"textAlign": "center", "color": "#2A3F54"}),
        html.P("An overview of energy consumption, GDP, and electricity generation.", style={"textAlign": "center"}),

        # Text Indicators (8 Boxes)
        html.Div([
            html.Div([
                html.H4("177", style={"color": "#2A3F54"}),
                html.P("No. of Countries", style={"color": "#2A3F54"})
            ], className="indicator-box"),
            html.Div([
                html.H4("113.82K", style={"color": "#2A3F54"}),
                html.P("Total Oil Consumed", style={"color": "#2A3F54"})
            ], className="indicator-box"),
            html.Div([
                html.H4("67.63K", style={"color": "#2A3F54"}),
                html.P("Total Carbon Consumed", style={"color": "#2A3F54"})
            ], className="indicator-box"),
            html.Div([
                html.H4("48.41K", style={"color": "#2A3F54"}),
                html.P("Total Electricity Generated", style={"color": "#2A3F54"})
            ], className="indicator-box"),
            html.Div([
                html.H4("5.0%", style={"color": "#2A3F54"}),
                html.P("Annual Growth Rate", style={"color": "#2A3F54"})
            ], className="indicator-box"),
            html.Div([
                html.H4("38.44T", style={"color": "#2A3F54"}),
                html.P("Global GDP", style={"color": "#2A3F54"})
            ], className="indicator-box"),
            html.Div([
                html.H4("12.4M", style={"color": "#2A3F54"}),
                html.P("Solar Units Produced", style={"color": "#2A3F54"})
            ], className="indicator-box"),
            html.Div([
                html.H4("25%", style={"color": "#2A3F54"}),
                html.P("Renewable Energy Usage", style={"color": "#2A3F54"})
            ], className="indicator-box"),
        ], className="indicators-row"),
    ], style={"padding": "20px", "backgroundColor": "#F7F7F7"}),

    # Charts Section (Two Rows with Three Charts Each)
    html.Div([
        html.Div([
            dcc.Graph(figure=fig_bar),
        ], className="chart-box"),
        html.Div([
            dcc.Graph(figure=fig_pie),
        ], className="chart-box"),
        html.Div([
            dcc.Graph(figure=fig_line),
        ], className="chart-box"),
    ], className="chart-row"),

    html.Div([
        html.Div([
            dcc.Graph(figure=fig_bar2),
        ], className="chart-box"),
        html.Div([
            dcc.Graph(figure=fig_pie2),
        ], className="chart-box"),
        html.Div([
            dcc.Graph(figure=fig_line2),
        ], className="chart-box"),
    ], className="chart-row"),
], style={"fontFamily": "Arial, sans-serif"})

# Add CSS for styling
app.index_string = """
<!DOCTYPE html>
<html>
<head>
    <title>World Energy Dashboard</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background-color: #F7F7F7;
        }
        .indicators-row {
            display: flex;
            justify-content: space-around;
            gap: 20px;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        .indicator-box {
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            width: 22%;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .chart-row {
            display: flex;
            justify-content: space-around;
            gap: 20px;
            margin: 20px 0;
        }
        .chart-box {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            width: 30%; /* Ensure three charts fit per row */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body>
    <div id="react-entry-point"></div>
</body>
</html>
"""


if __name__ == '__main__':
    app.run_server(debug=False)
