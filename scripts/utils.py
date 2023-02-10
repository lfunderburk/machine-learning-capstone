import pandas as pd
from pathlib import Path
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Var list
var_list = ['vehicleclass_','make_',
                    'model.1_','model_year',
                    'cylinders_','fuelconsumption_city(l/100km)',
                    'fuelconsumption_hwy(l/100km)',
                    'fuelconsumption_comb(l/100km)',
                    'fuelconsumption_comb(mpg)',
                    'co2emissions_(g/km)',
                    'number_of_gears']

# Set up parameters for the model - numerical and categorical
numeric_features =  ['model_year','cylinders_','fuelconsumption_city(l/100km)','fuelconsumption_hwy(l/100km)',
                    'fuelconsumption_comb(l/100km)','fuelconsumption_comb(mpg)','co2emissions_(g/km)','number_of_gears']
categorical_features = ['vehicleclass_']

# Set up numerical and categorical transformers
numeric_transformer = Pipeline(
                            steps=[("scaler", StandardScaler())]
                        )

categorical_transformer = OneHotEncoder(handle_unknown="ignore")

# Set up preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        #("cat", categorical_transformer, categorical_features),
    ]
)

def read_data(path):
    """
    This function reads data from csv files

    Parameters:
    ----------
        path: str
            path to data files

    Returns:
    -------
        fuel_df: pandas.DataFrame
            dataframe containing fuel cars data
        electric_df: pandas.DataFrame
            dataframe containing electric cars data
        hybrid_df: pandas.DataFrame
            dataframe containing hybrid cars data

    """
    
    # Fuel based cars
    file_name_2022_1995 = "1995_2022_vehicle_fuel_consumption.csv"
    
    # Electric cars
    pure_electric = "Battery-electric_vehicles_2012-2022_(2022-05-16).csv"
    hybric_vehicle = "Plug-in_hybrid_electric_vehicles_2012-2022_(2022-03-28).csv"

    # Read data files
    fuel_df = pd.read_csv(Path(path ,f'{file_name_2022_1995}'))
    electric_df = pd.read_csv(Path(path ,f'{pure_electric}'))
    hybrid_df = pd.read_csv(Path(path ,f'{hybric_vehicle}'))

    return fuel_df, electric_df, hybrid_df