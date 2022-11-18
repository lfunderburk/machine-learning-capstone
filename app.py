import pandas as pd
from pathlib import Path
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

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

all_makes = list(set(master_df['make_'].unique()).union(set(electric_df['make_'].unique())).union(set(hybrid_df['make_'].unique())))

# App section        
        

# Stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



# Intialize app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, title="Fuel consumption of vehicles dashboard")
server = app.server

colors = {
    'background': '#003f5c',
    'text': 'white'
}

card_text_style = {
    'textAlign' : 'left',
    'color' : 'black',
    'backgroundColor': colors['background']
}

header_style = {'textAlign' : 'center','color':"white"}

header_menu_style = {'textAlign' : 'left','color':"white"}

# ----------------------------------------------------------------------------------#
text_card = dbc.Card(
    dbc.CardBody(
        [
            html.H3("Vehicle fuel consumption dashboard", className="card-title",style=header_style),
            html.H6("Fuel-only, hybrid and electric vehicles", className="card-subtitle", style=header_style),
            html.P(
                "This dashboard's goal is to uncover trends in fuel consumption for various vehicles \
                whose fuel consumption ratings and CO2 emissions were established through 5-cycle fuel consumption testing.",
                className="card-text",style=header_style,
            ),
            dbc.CardLink(
                "Learn about fuel consumption testing", 
            href="https://www.nrcan.gc.ca/energy-efficiency/transportation-alternative-fuels/fuel-consumption-guide/understanding-fuel-consumption-ratings/fuel-consumption-testing/21008",
            style={'textAlign' : 'center'}),
            html.P(""),
            dbc.CardLink("Data source",
                href="https://open.canada.ca/data/en/dataset/98f1a129-f628-4ce4-b24d-6f16bf24dd64"
                )
            
        ]
    ),style={'backgroundColor': '#111111'}
)

menu_card = dbc.Card(
    dbc.CardBody(
        [
           html.Div([
                html.Div(
                        html.H4("Summary statistics - all makes and models", style=header_menu_style),
                        className="four columns"
                ),

                html.Div([
                    html.P("Select attribute", style=header_menu_style),
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
        ]
    ), style={'backgroundColor': colors['background']}
)

plots_card = dbc.Card(
    dbc.CardBody(
        [ 
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
        ]
    ), style={'backgroundColor': colors['background']}
)



cards = dbc.Container([ 
    dbc.Row(
    [   
        dbc.Col(text_card, width='auto'),
        dbc.Col(menu_card, width='auto'),
        dbc.Col(plots_card, width='auto'),
    ]
)
], fluid=True,style={'backgroundColor': "black"})




app.layout = html.Div(
    children=[cards],
    style={'backgroundColor': "black"}
)


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