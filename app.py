# Import relevant libraries
import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd




#data first chart==============
# Read the CSV file into a DataFrame
df = pd.read_csv("WBdata.csv")

# Filter electricity from coal
ElecFromCoal = df[df['Series Name'] == 'Electricity production from renewable sources, excluding hydroelectric (% of total)']

# List of top 50 economies (based on World Bank or relevant sources)
top_50_economies = [
    "United States", "China", "Japan", "Germany", "India", "United Kingdom", "France", "Italy",
    "Canada", "South Korea", "Russia", "Australia", "Brazil", "Spain", "Mexico", "Indonesia",
    "Netherlands", "Saudi Arabia", "Turkey", "Switzerland", "Taiwan", "Sweden", "Poland",
    "Belgium", "Thailand", "Argentina", "Nigeria", "Austria", "United Arab Emirates", "South Africa",
    "Israel", "Denmark", "Singapore", "Malaysia", "Hong Kong", "Philippines", "Norway", "Vietnam",
    "Bangladesh", "Ireland", "Czech Republic", "Pakistan", "Chile", "Finland", "Colombia", "Romania",
    "Portugal", "New Zealand", "Hungary", "Slovakia", "Greece"
]

# Filter data for top 50 economies
ElecFromCoal = ElecFromCoal[ElecFromCoal['Country Name'].isin(top_50_economies)]



# Reshape the data from wide to long format
long_format = ElecFromCoal.melt(
    id_vars=["Country Name"],
    value_vars=[col for col in ElecFromCoal.columns if "YR" in col],
    var_name="Year",
    value_name="Electricity Production (%)"
)

# Clean the "Year" column and filter valid numeric values

#long_format["Year"] = long_format["Year"].str.extract(r'(\d{4})')  # Extract year as numeric
long_format["Year"] = pd.to_numeric(long_format["Year"].str.extract(r'(\d{4})')[0], errors='coerce')  # Extract year as numeric

long_format["Electricity Production (%)"] = pd.to_numeric(long_format["Electricity Production (%)"], errors='coerce')

#filling the data
#long_format = long_format[long_format['Country Name'] == 'Australia']


# Forward fill missing values
long_format['Electricity Production (%)'] = long_format.groupby('Country Name')['Electricity Production (%)'].ffill()
long_format['Electricity Production (%)'] = long_format.groupby('Country Name')['Electricity Production (%)'].bfill()




#to modify the long format======================

# Drop rows with missing values
long_format = long_format.dropna()

# Filter countries with complete data from 1990 onwards
# Filter data to include only entries from 1990 onward
long_format = long_format[long_format["Year"] >= 1990]
long_format = long_format[long_format["Year"] <= 2015]
long_format['Average'] = long_format.groupby('Country Name')['Electricity Production (%)'].transform('mean')




#data preparation fourth chart=======================================
# Read the CSV file into a DataFrame
iea = pd.read_csv("MES_0924.csv", skiprows=8,encoding='Windows-1252')

# List of top 50 economies (based on World Bank or relevant sources)
#g20_countries = [
#    "Argentina", "Australia", "Brazil", "Canada", "China", "France", "Germany", 
#    "India", "Indonesia", "Italy", "Japan", "Mexico", "Russia", "Saudi Arabia", 
#    "South Africa", "South Korea", "Turkey", "United Kingdom", "United States"
#]

# Filter data for top 50 economies
#iea2 = iea[iea['Country'].isin(g20_countries)]
iea2 = iea
#change to date format
# Convert the 'Time' column from string format to datetime
iea2['Time'] = pd.to_datetime(iea2['Time'], format='%B %Y')

#to select net electricity production
iea2 = iea2[iea2["Balance"] == 'Net Electricity Production']

#select only total electricity and renewable electricity
select1= [
         "Electricity", "Total Renewables (Hydro, Geo, Solar, Wind, Other)"
         ]
iea2 = iea2[iea2['Product'].isin(select1)]


#get the percentage
# Extract the year from 'Time'
iea2['Year'] = iea2['Time'].dt.year
iea2 = iea2[iea2['Year'] >= 2020]


# Filter the data for the two relevant products: 'Electricity' and 'Total Renewables'
filtered_data = iea2[iea2['Product'].isin(['Electricity', 'Total Renewables (Hydro, Geo, Solar, Wind, Other)'])]

# Group by 'Country' and 'Year' and sum the 'Value' for each product
aggregated_data = filtered_data.groupby(['Country', 'Year', 'Product'])['Value'].sum().reset_index()

# Pivot the table to create separate columns for 'Electricity' and 'Total Renewables'
pivoted_data = aggregated_data.pivot_table(index=['Country', 'Year'], columns='Product', values='Value', aggfunc='sum')

# If you want to combine the sum of 'Electricity' and 'Total Renewables' into a single column, you can do:
pivoted_data['Renewables_Percentage'] = (pivoted_data['Total Renewables (Hydro, Geo, Solar, Wind, Other)'] /pivoted_data['Electricity'] ) * 100 

pivoted_data_reset = pivoted_data.reset_index()
# Example: Subset the DataFrame to a few columns
iea3= pivoted_data_reset[['Country', 'Year', 'Renewables_Percentage']]
iea3_cleaned = iea3.drop_duplicates()



#extract year
country_specific_values = iea3_cleaned[iea3_cleaned['Year'] == 2024][['Country', 'Renewables_Percentage']]

# Merge this data back into the original dataframe based on the 'Country'
iea3_cleaned = pd.merge(iea3, country_specific_values, on='Country', how='left', suffixes=('', '_average'))


iea3_cleaned["average"]=iea3_cleaned["Renewables_Percentage_average"]



#end of data preparation fourth chart====================================



#==============================================DATA PREP END






#===============================================second chart========
# Read the CSV file into a DataFrame
df2 = pd.read_csv("WBdata.csv")

# List of top 50 economies (based on World Bank or relevant sources)
g20_countries = [
    "Argentina", "Australia", "Brazil", "Canada", "China", "France", "Germany", 
    "India", "Indonesia", "Italy", "Japan", "Mexico", "Russia", "Saudi Arabia", 
    "South Africa", "South Korea", "Turkey", "United Kingdom", "United States"
]

# Filter data for top 50 economies
df2 = df2[df2['Country Name'].isin(g20_countries)]


#select series
series_select = [
'Electricity production from coal sources (% of total)',
 'Electricity production from hydroelectric sources (% of total)',
 'Electricity production from natural gas sources (% of total)',
 'Electricity production from nuclear sources (% of total)',
 'Electricity production from oil sources (% of total)',
 ]

df2 = df2[df2['Series Name'].isin(series_select)]




#change to long format======================================
# Reshape the data from wide to long format
# Melt the DataFrame to long format
df_long2 = pd.melt(df2, 
                  id_vars=["Country Name", "Country Code", "Series Name", "Series Code"], 
                  value_vars=[col for col in df2.columns if "YR" in col],
                  var_name="Year", 
                  value_name="Value")

df_long2["Year"] = pd.to_numeric(df_long2["Year"].str.extract(r'(\d{4})')[0], errors='coerce')  # Extract year as numeric
df_long2["Value"] = pd.to_numeric(df_long2["Value"], errors='coerce')


df_long2 = df_long2[df_long2["Year"] == 2015]




# Create the Treemap (assuming df_long2 is your DataFrame)
# Create a horizontal bar plot
fig2 = px.bar(df_long2, 
              x='Value', 
              y='Country Name', 
              color='Series Name',  # Color by energy source
              title="Non-Renewable Electricity Sources in G20 Countries (2015)",
              orientation='h',  # Make the bars horizontal
              color_discrete_sequence=px.colors.qualitative.Set3,  # Color palette
              category_orders={'Country Name': df_long2['Country Name'].unique()}  # Order by country names
              )

# Update layout: Add text size for labels and titles, and adjust the margins
# Update layout: Adjust text size for labels, titles, and margins
fig2.update_layout(
    font=dict(size=10),  # Font size for titles and axis labels
    #margin={"t": 100, "l": 80, "r": 40, "b": 100},  # Adjust margins: increase bottom margin (b) for space
    legend=dict(
        title="Energy Source",  # Title for the legend
        orientation="h",  # Horizontal legend
        yanchor="bottom",
        y=-0.5,# Anchor the legend at the bottom
        xanchor="left",
        font=dict(size=6),  # Font size for legend items
    ),
    barmode='stack',  # Stack the bars for each country
)




#=================================================================













#===========real data prep end===========================================================================

# Create the Dash app
app = dash.Dash(__name__)
server = app.server

#====================FUNGSI SUBSET=====================
def filter_data(min_threshold, max_threshold):
    return long_format[(long_format["Average"] > min_threshold) & (long_format["Average"] <= max_threshold)]

#======================================================FUNGSION SET END


app.layout = html.Div([
    # Header Section
    html.Div([
        # Title and Subtitle
        html.H1("Indonesia Energy and Electricity Dashboard Compare to Selected Economies", style={"textAlign": "center", "color": "#2A3F54"}),
        html.P("Snapshot of Indonesia Energy and Electricity Indicators", style={"textAlign": "center"}),

        # Text Indicators (8 Boxes in Grid Layout)
        html.Div([
            html.Div([
                html.H4("323,321 (GWh)", style={"color": "#2A3F54"}),
                html.P("Produksi Tenaga Listrik - 2023", style={"color": "#2A3F54"})
            ], className="indicator-box"),
            html.Div([
                html.H4("60,374.000 (Cub m mn)", style={"color": "#2A3F54"}),
                html.P("Produksi Gas Alam: OPEC: Produksi yang Dipasarkan - 2023", style={"color": "#2A3F54"})
            ], className="indicator-box"),
            html.Div([
                html.H4("21,463.000 (Cub m mn)", style={"color": "#2A3F54"}),
                html.P("Gas Alam: Ekspor - 2023", style={"color": "#2A3F54"})
            ], className="indicator-box"),
            html.Div([
                html.H4("55.833 (Barrel/Day th)", style={"color": "#2A3F54"}),
                html.P("Minyak Mentah: Ekspor -  2023", style={"color": "#2A3F54"})
            ], className="indicator-box"),
            html.Div([
                html.H4("332.750 (Barrel/Day th)", style={"color": "#2A3F54"}),
                html.P("Minyak Mentah: Impor -  2023", style={"color": "#2A3F54"})
            ], className="indicator-box"),
            html.Div([
                html.H4("1,603.769 (Barrel/Day th)", style={"color": "#2A3F54"}),
                html.P("Konsumsi Minyak - 2023", style={"color": "#2A3F54"})
            ], className="indicator-box"),
            html.Div([
                html.H4("775.182 (Tonne mn)", style={"color": "#2A3F54"}),
                html.P("Produksi Batubara - 2023", style={"color": "#2A3F54"})
            ], className="indicator-box"),
            html.Div([
                html.H4("61.558 (TOE mn)", style={"color": "#2A3F54"}),
                html.P("Konsumsi Batubara - 2018", style={"color": "#2A3F54"})
            ], className="indicator-box"),
        ], style={"display": "grid", "gridTemplateColumns": "repeat(4, 1fr)", "gap": "20px", "padding": "20px"}),
    ], style={"padding": "20px", "backgroundColor": "#F7F7F7"}),


html.Div(
    style={"display": "grid", "gridTemplateColumns": "repeat(5, 1fr)", "gap": "20px", "padding": "20px"},
    children=[
        html.Div(
            style={"backgroundColor": "lightgray", "borderRadius": "8px", "padding": "10px"},
            children=[
                html.H3("Crude Oil Price", style={"textAlign": "center"}),
                html.P("69.724 | Increase | 0,70% |"),
            ],
        ),
        html.Div(
            style={"backgroundColor": "lightgray", "borderRadius": "8px", "padding": "10px"},
            children=[
                html.H3("Brent Price", style={"textAlign": "center"}),
                # Replace with another chart or content
                html.P("73.109 | Increase | 0,66% |"),
            ],
        ),
        html.Div(
            style={"backgroundColor": "lightgray", "borderRadius": "8px", "padding": "10px"},
            children=[
                html.H3("Natural Gas Price", style={"textAlign": "center"}),
                # Replace with another chart or content
                html.P("3.6980 | Increase | 1.15% |"),
            ],
        ),
        
        html.Div(
            style={"backgroundColor": "lightgray", "borderRadius": "8px", "padding": "10px"},
            children=[
                html.H3("Gasoline Price", style={"textAlign": "center"}),
                # Replace with another chart or content
                html.P("1.9502 | Increase | 0,33% |"),
            ],
        ),
        
        html.Div(
            style={"backgroundColor": "lightgray", "borderRadius": "8px", "padding": "10px"},
            children=[
                html.H3("Coal   Price", style={"textAlign": "center"}),
                # Replace with another chart or content
                html.P("125.50 | Decrease | -1.41% |"),
            ],
        ),
        
        
    ],
),




    # Charts Section (Two Rows with Three Charts Each)
  # Charts Section (Two Rows with Three Charts Each)
    html.Div([
        #=============
        html.Div([
        #============================================================
        html.Div(
            children=[
                
            
                # Text element
                html.Div(
                    children="Average Renewable Energy Production of Total Electricity (1990 - 2015)",
                    style={"paddingRight": "10px", "textAlign": "right", "lineHeight": "40px","fontSize": "10px"}  # Adjust line height for better vertical alignment
                ),

                # Dropdown element
                dcc.Dropdown(
                    id="threshold-filter",
                    options=[
                        {"label": "0% - 5%", "value": "0-5"},
                        {"label": "6% - 10%", "value": "6-10"},
                        {"label": "11% - 15%", "value": "11-15"},
                        {"label": "16% - 25%", "value": "16-25"},
                        {"label": "26% - 100%", "value": "26-100"}
                    ],
                    value="0-5",
                    placeholder="Select Range",
                    style={
                        "width": "30%",  # Set a specific width for the dropdown
                        "height": "auto",  # Adjust height to match the text height
                        "margin": "auto",
                        "fontSize": "10px"
                        
                    }
                ),
            ],
            style={
                "display": "flex",              # Align elements horizontally
                "alignItems": "center",         # Vertically center items in the flex container
                "justifyContent": "flex-start", # Align items to the left
                "width": "80%",                 # Adjust the width of the flex container
                "margin": "auto",
            }
        ),

        # Placeholder for the graph
        dcc.Graph(id="line-chart"),
        
        #============================================================
        ], style={"flex": "1", "padding": "10px"}),
        #===========================================================
        
       
           html.Div([
            
            html.Div(
                children="Average Renewable Energy Production of Total Electricity (1990 - 2015)",
                style={"paddingRight": "10px", "textAlign": "right", "lineHeight": "40px","fontSize": "10px","color": "white"}  # Adjust line height for better vertical alignment
            ),    
               
           dcc.Graph(figure=fig2),   
           ], style={"flex": "1", "padding": "10px"}),
       ], style={"display": "flex", "flexDirection": "row", "gap": "20px"}),

   
   #=============================new object row 
    
    
    
    
  #====================================================  
    
], style={"fontFamily": "Arial, sans-serif"})



#app callback first chart=======================
@app.callback(
    dash.dependencies.Output("line-chart", "figure"),
    [dash.dependencies.Input("threshold-filter", "value")]
)
def update_chart(threshold_key):
    # Map string keys to numeric ranges
    range_mapping = {
        "0-5": (0, 5),
        "6-10": (6, 10),
        "11-15": (11, 15),
        "16-25": (16, 25),
        "26-100": (26, 100)
    }
    min_threshold, max_threshold = range_mapping[threshold_key]
    filtered_data = filter_data(min_threshold, max_threshold)
    fig = px.line(
        filtered_data,
        markers=True,
        #connectgaps=True,
        x="Year",
        y="Electricity Production (%)",
        color="Country Name",
        color_discrete_sequence=px.colors.qualitative.Set3,
        title=f"Average Renewable Energy Production of Total Electricity 1990 - 2015 {min_threshold}% - {max_threshold}%",
        labels={"Electricity Production (%)": "Electricity Production (%)", "Year": "Year"}
    )
    
    # Update font size for the axis labels, title, and legend
    fig.update_layout(
        title_font=dict(size=12),  # Title font size
        font=dict(size=14),  # Font size for axis labels and tick labels
        xaxis_title_font=dict(size=12),  # Font size for the X-axis title
        yaxis_title_font=dict(size=12),  # Font size for the Y-axis title
        legend_title_font=dict(size=12),  # Font size for legend title
        legend_font=dict(size=10),  # Font size for legend items
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=False)
