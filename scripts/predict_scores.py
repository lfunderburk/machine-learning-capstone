import pandas as pd
import sys, os
import joblib
import utils


if __name__=="__main__":

    # Set up paths
    sys.path.append(os.path.abspath(os.path.join('.','./data/', './clean-data/')))
    sys.path.append(os.path.abspath(os.path.join('.','./models/')))

    # Load data
    fuel_df, electric_df, hybrid_df = utils.read_data("./data/clean-data/")

    # Load model
    best_dtc = joblib.load('./models/hard_voting_classifier.pkl')

    # Preprocess the original data (fuel_df)
    X_fuel = fuel_df[utils.var_list]

    X_fuel_preprocessed = utils.preprocessor.fit_transform(X_fuel)

    # Predict missing "co2_rating" values
    best_dtc.predict(X_fuel_preprocessed[fuel_df['co2_rating'].isnull()])

