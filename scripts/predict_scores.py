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
    
    non_na_rating_class, na_rating_class = utils.remove_missing_values(fuel_df)
    non_na_rating_class.rename(columns={'co2_rating': 'original_co2r'}, inplace=True)
    na_rating_class.rename(columns={'co2_rating': 'original_co2r'}, inplace=True)

    # Load model
    best_dtc = joblib.load('./models/hard_voting_classifier_co2_fuel.pkl')

    predictions = []
    for item in [non_na_rating_class, na_rating_class]:
        # Preprocess the original data (fuel_df)
        X_fuel = item[utils.var_list].copy()
        target = item['original_co2r'].copy()

        # Predict missing "co2_rating" values
        X_fuel['predicted_co2_rating'] = best_dtc.predict(X_fuel)

        # Merge the predicted values with the original data
        fuel_df_pred = pd.concat([X_fuel, target], axis=1)

        # Append to list
        predictions.append(fuel_df_pred)

    # Concatenate the two dataframes
    fuel_df_pred = pd.concat(predictions, axis=0)

    # Save the data
    fuel_df_pred.to_csv('./data/clean-data/predicted_co2_rating.csv', index=False)