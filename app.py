import pandas as pd
from pathlib import Path
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

def generate_count_plot(attribute, vehicle_type, dataframe):
    """
    This function generates a histogram of an attribute for 
    vehicle dataframes
    """

    try:
        
        year_min = dataframe['model_year'].min() 
        year_max = dataframe['model_year'].max() 
        rename_attr = attribute.replace("_"," ").capitalize()
        fig = px.histogram(data_frame=dataframe,
                        x=attribute, labels={attribute:rename_attr},
                        title=f"Frequency of {rename_attr} ({year_min} - {year_max}), {vehicle_type} vehicle")
        fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
        fig.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
        )


        return fig
    except KeyError:
        print("Key not found. Make sure that 'vehicle_type' is in ['electric', 'hybrid', 'fuel-only']")
    except ValueError:
        print("Dimension is not valid. ")
        
# Set data read path
clean_data = "C:/Users/Laura GF/Documents/GitHub/machine-learning-capstone/data/clean-data/"

# Assign variables 
file_name_2022_1995 = "1995_2022_vehicle_fuel_consumption.csv"
pure_electric = "Battery-electric_vehicles_2012-2022_(2022-05-16).csv"
hybric_vehicle = "Plug-in_hybrid_electric_vehicles_2012-2022_(2022-03-28).csv"

# Read data
master_df = pd.read_csv(Path(clean_data,f'{file_name_2022_1995}'))
electric_df = pd.read_csv(Path(clean_data,f'{pure_electric}'))
hybrid_df = pd.read_csv(Path(clean_data,f'{hybric_vehicle}'))

dataframe_dictionary = {"electric": electric_df,
                       "hybrid": hybrid_df,
                       "fuel-only": master_df}



# App section        
        

# Stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# Intialize app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, title="Fuel consumption of vehicles dashboard")
server = app.server

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

card_text_style = {
    'textAlign' : 'center',
    'color' : 'black',
    'backgroundColor': colors['background']
}

# ----------------------------------------------------------------------------------#
app.layout = html.Div(style=card_text_style, children=[
             # This div contains a header H1, a dropdown to select the kind of plot and the plot
            html.H1("Summary statistics - all makes and models", style={"color":"white"}),
            
            html.Div([
                html.Div([
                    html.H6("Select attribute", style={"color":"white"}),
                    dcc.Dropdown(
                        id='attribute',
                        options=[{'label': 'Vehicle make', 'value': 'make_'},
                                {'label': 'Vehicle class', 'value': 'vehicleclass_'},
                                {'label': 'Transmission', 'value': 'transmission_'},
                                {'label': 'Transmission type', 'value': 'transmission_type'},
                                {'label': 'Number of gears', 'value': 'number_of_gears'},
                                {'label':"CO2 Emissions", 'value': 'co2emissions_(g/km)'} ],
                        value= 'make_',
                        style={'backgroundColor':"white"}),
                ], className="four columns"),

            ], className="row"),
            html.Div([
                    html.Div([
                            dcc.Graph(id='graph-dist_fuel')
                        ], className="four columns"),
                    html.Div([
                        dcc.Graph(id='graph-dist_electric')
                    ], className="four columns"),

                    html.Div([
                        dcc.Graph(id='graph-dist_hybrid')
                    ], className="four columns"),
                ], className="row"),
            
            html.H1("Summary statistics - by make and models", style={"color":"white"}),
            html.Div([
                html.Div([
                    html.H6("Select type of vehicle", style={"color":"white"}),
                    dcc.Dropdown(
                        id='vehicle-type',
                        options=[{'label': 'Electric vehicle', 'value': 'electric'},
                                {'label': 'Hybrid vehicle', 'value': 'hybrid'},
                                {'label': 'Fuel-only vehicle', 'value': 'fuel-only'}],
                        value= 'fuel-only'),
                ], className="four columns")
            ], className="row")

        
])

@app.callback(
    Output('graph-dist_electric', 'figure'),
    [Input('attribute', 'value')])
def update_frequency_chart(attribute):
    vehicle_type = "electric"
    dataframe = dataframe_dictionary[vehicle_type]
    fig0 = generate_count_plot(attribute, vehicle_type, dataframe)
    return fig0

@app.callback(
    Output('graph-dist_hybrid', 'figure'),
    [Input('attribute', 'value')])
def update_frequency_chart(attribute):
    vehicle_type = "hybrid"
    dataframe = dataframe_dictionary[vehicle_type]
    fig0 = generate_count_plot(attribute, vehicle_type, dataframe)
    return fig0

@app.callback(
    Output('graph-dist_fuel', 'figure'),
    [Input('attribute', 'value')])
def update_frequency_chart(attribute):
    vehicle_type = "fuel-only"
    dataframe = dataframe_dictionary[vehicle_type]
    fig0 = generate_count_plot(attribute, vehicle_type, dataframe)
    return fig0

if __name__ == '__main__':  
    
    app.run_server(debug=True) 