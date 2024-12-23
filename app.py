# Import relevant libraries
import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

 # Load dataset
data = pd.read_csv('winequality-red.csv')


# Create the Dash app
app = dash.Dash(__name__)
server = app.server

# Define the layout
app.layout = html.Div([
    html.H1("Hello, World!", style={"textAlign": "center"}),
    html.P("This is a simple Dash app.", style={"textAlign": "center"})
])


if __name__ == '__main__':
    app.run_server(debug=False)
