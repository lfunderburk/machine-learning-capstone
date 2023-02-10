import pandas as pd
import sys, os
from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.metrics import confusion_matrix, \
                            classification_report, \
                            accuracy_score,\
                            balanced_accuracy_score,\
                            ConfusionMatrixDisplay
from sklearn.metrics import DetCurveDisplay, RocCurveDisplay
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
import joblib

def read_data(path):
    
    # Fuel based cars
    file_name_2022_1995 = "1995_2022_vehicle_fuel_consumption.csv"
    
    # Electric cars
    pure_electric = "Battery-electric_vehicles_2012-2022_(2022-05-16).csv"
    hybric_vehicle = "Plug-in_hybrid_electric_vehicles_2012-2022_(2022-03-28).csv"

    # Read data files
    master_df = pd.read_csv(Path(path ,f'{file_name_2022_1995}'))
    electric_df = pd.read_csv(Path(path ,f'{pure_electric}'))
    hybrid_df = pd.read_csv(Path(path ,f'{hybric_vehicle}'))

    # Set up data pipeline - goal is to predict co2_rating 
    non_na_rating = master_df[~master_df['co2_rating'].isna()]
    non_na_rating_class = non_na_rating.copy()
    non_na_rating_class['co2_rating'] = non_na_rating_class['co2_rating'].astype(int)

    # Drop smog_rating from non_na_rating
    non_na_rating_class.drop(columns=['smog_rating'], inplace=True)
    non_na_rating_class['number_of_gears'].fillna(0, inplace=True)

    return non_na_rating_class

def train_and_evaluate_model(X_train, y_train, X_test, y_test, model_pipeline, model_name):
    
    model_pipeline.fit(X_train, y_train.values.ravel())


    # Predict
    y_pred = model_pipeline.predict(X_test)
    
    # Obtain accuracy score
    acc = accuracy_score(y_test, y_pred)
    print('accuracy is',accuracy_score(y_pred,y_test))
    
    score_train = model_pipeline.score(X_train, y_train)
    score_test = model_pipeline.score(X_test, y_test)
    print('score for training set', score_train, 'score for testing set', score_test)
    balanced_accuracy = balanced_accuracy_score(y_test, y_pred)
    print("Balanced accuracy score", balanced_accuracy)
    
    report = classification_report(y_test, y_pred)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ConfusionMatrixDisplay.from_predictions(y_test, y_pred, ax=ax)
    _ = ax.set_title(
        f"Confusion Matrix for {model_name}"
    )
    
    plt.show()
    
    print(report, sep=',')
    
def classify_grid_search_cv_tuning(model, parameters, X_train, X_test, y_train, y_test, n_folds = 5, scoring='accuracy'):
    """
    This function tunes GridSearchCV model
    
    Parameters:
    ----------
        model
        parameters
        X_train
        X_test
        y_train
        y_test
        n_folds
        scoring
        
    Returns:
    --------
        best_model
        best_score
    """
    # Set up and fit model
    tune_model = GridSearchCV(model, param_grid=parameters, cv=n_folds, scoring=scoring)
    tune_model.fit(X_train, y_train.values.ravel())
    
    best_model = tune_model.best_estimator_
    best_score = tune_model.best_score_
    y_pred = best_model.predict(X_test)
    
    # Printing results
    print("Best parameters:", tune_model.best_params_)
    print("Cross-validated accuracy score on training data: {:0.4f}".format(tune_model.best_score_))
    print()

    print(classification_report(y_test, y_pred))
    
    return best_model, best_score

if __name__=="__main__":

    sys.path.append(os.path.abspath(os.path.join('.','./data/', './clean-data/')))
    sys.path.append(os.path.abspath(os.path.join('.','./models/')))
    paths = sys.path
    clean_path = [item for item in paths if "machine-learning-capstone\\data\\clean-data" in item]
    clean_data = clean_path[0]

    non_na_rating = read_data(clean_data)
    
    # Set X and Y variables 
    # Response variable
    Y = non_na_rating[['co2_rating']]

    # Dependent variables
    X = non_na_rating[['vehicleclass_','make_',
                        'model.1_','model_year',
                        'cylinders_','fuelconsumption_city(l/100km)',
                        'fuelconsumption_hwy(l/100km)',
                        'fuelconsumption_comb(l/100km)',
                        'fuelconsumption_comb(mpg)',
                        'co2emissions_(g/km)',
                        'number_of_gears']]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    
    
    # Set up pipeline
    # Set up parameters for the model - numerical and categorical
    numeric_features =  ['model_year','cylinders_','fuelconsumption_city(l/100km)','fuelconsumption_hwy(l/100km)',
                     'fuelconsumption_comb(l/100km)','fuelconsumption_comb(mpg)','co2emissions_(g/km)','number_of_gears']
    categorical_features = ['vehicleclass_']

    # Use smote to balance the data
    smote = SMOTE(random_state=42)
    X_train, y_train = smote.fit_resample(X_train[numeric_features], y_train)


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

    # Set up model pipeline
    clf1 = KNeighborsClassifier(3,)
    clf2 = SVC(gamma=2, C=1, random_state=42)
    clf3 = RandomForestClassifier(max_depth=100, n_estimators=10, max_features=1, random_state=42)

    classifiers = {"KNN": clf1, 
                   "SVM": clf2,
                   "RFC": clf3
                }

    eclf1 = VotingClassifier(estimators=[('knn', clf1), ('svm', clf2), ('dt', clf3)], voting='hard')
    model = Pipeline(
            steps=[("preprocessor", preprocessor), 
                    ("hard Voting", eclf1 )] #colsample  by tree, n estimators, max depth
                                                                        )
    train_and_evaluate_model(X_train, y_train, X_test, y_test, model,"Voting")

    params = {}
    best_dtc, dtc_score = classify_grid_search_cv_tuning(model, params, X_train, X_test, y_train, y_test, n_folds=10, scoring='balanced_accuracy')

    # Save model
    joblib.dump(best_dtc, './models/hard_voting_classifier.pkl')



