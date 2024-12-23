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


if __name__ == '__main__':
    app.run_server(debug=False)
