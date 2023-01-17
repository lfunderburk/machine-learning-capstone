import pandas as pd
import sys, os
from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split

if __name__=="__main__":

    sys.path.append(os.path.abspath(os.path.join('.','./data/', './clean-data/')))
    paths = sys.path
    clean_path = [item for item in paths if "machine-learning-capstone\\data\\clean-data" in item]
    clean_data = clean_path[0]

    # Assign variables 
    file_name_2022_1995 = "1995_2022_vehicle_fuel_consumption.csv"
    pure_electric = "Battery-electric_vehicles_2012-2022_(2022-05-16).csv"
    hybric_vehicle = "Plug-in_hybrid_electric_vehicles_2012-2022_(2022-03-28).csv"

    # Read data files
    master_df = pd.read_csv(Path(clean_data + "clean-data",f'{file_name_2022_1995}'))
    electric_df = pd.read_csv(Path(clean_data + "clean-data",f'{pure_electric}'))
    hybrid_df = pd.read_csv(Path(clean_data + "clean-data",f'{hybric_vehicle}'))

    # Set up data pipeline - goal is to predict co2_rating 
    non_na_rating = master_df[~master_df['co2_rating'].isna()]
    
    # Set X and Y variables 
    # Response variable
    Y = non_na_rating[['co2_rating']]

    # Dependent variables
    X = non_na_rating[['vehicleclass_','make_','model.1_','model_year','cylinders_','fuelconsumption_city(l/100km)','fuelconsumption_hwy(l/100km)',
                        'fuelconsumption_comb(l/100km)','fuelconsumption_comb(mpg)','co2emissions_(g/km)','number_of_gears']]

    # Set up parameters for the model - numerical and categorical
    numeric_features =  ['model_year','cylinders_','fuelconsumption_city(l/100km)','fuelconsumption_hwy(l/100km)',
                     'fuelconsumption_comb(l/100km)','fuelconsumption_comb(mpg)','co2emissions_(g/km)','number_of_gears']
    categorical_features = ['vehicleclass_','make_','model.1_']

    # Set up numerical and categorical transformers
    numeric_transformer = Pipeline(
                                steps=[("scaler", StandardScaler())]
                            )

    categorical_transformer = OneHotEncoder(handle_unknown="ignore")

    # Set up preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)


    
