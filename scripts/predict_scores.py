import pandas as pd
import sys, os
import joblib
import utils

def predict_co2_rating(df, list_of_vars, model):
    # Preprocess the original data (fuel_df)
    X_fuel = df[list_of_vars].copy()
    target = df['original_co2r'].copy()

    # Get remaining columns from df
    remaining_cols = [col for col in df.columns if col not in list_of_vars and col != 'original_co2r']
    remaining_df = df[remaining_cols].copy()

    # Predict missing "co2_rating" values
    X_fuel['predicted_co2_rating'] = model.predict(X_fuel)

    # Merge the predicted values with the original data
    fuel_df_pred = pd.concat([X_fuel, target, remaining_df], axis=1)

    return fuel_df_pred

    

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
    
    # Use model to make predictions
    non_na_pred = predict_co2_rating(non_na_rating_class, utils.var_list, best_dtc)
    na_pred = predict_co2_rating(na_rating_class, utils.var_list, best_dtc)

    # Merge the predicted values with the original data
    fuel_df_pred = pd.concat([non_na_pred, na_pred], axis=0)
    
    # Save the data
    fuel_df_pred.to_csv('./data/clean-data/predicted_co2_rating.csv', index=False)

