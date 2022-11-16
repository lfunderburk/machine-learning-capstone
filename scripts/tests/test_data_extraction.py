from scripts.data_extraction import fuel_consumption_metadata_extraction
from scripts.data_extraction import read_and_clean_csv_file
from scripts.data_extraction import extract_raw_data
import sys, os
from pathlib import Path
import pandas as pd

# Paths exist
def test_data_folder_exists():
    sys.path.append(os.path.abspath(os.path.join('..',"./data")))
    paths = sys.path
    ml_path = [item for item in paths if "machine-learning-capstone\\data" in item]
    assert len(ml_path)==1

def test_raw_data_folder_exists():
    sys.path.append(os.path.abspath(os.path.join('..','./data/raw-data/')))
    paths = sys.path
    ml_path = [item for item in paths if "machine-learning-capstone\\data\\raw-data" in item]
    assert len(ml_path)==1

def test_clean_data_folder_exists():
    sys.path.append(os.path.abspath(os.path.join('..','./data/clean-data/')))
    paths = sys.path
    ml_path = [item for item in paths if "machine-learning-capstone\\data\\clean-data" in item]
    assert len(ml_path)==1

# Tests for fuel_consumption_metadata_extraction
def test_two_cols_fuel_consumption_metadata_extraction():
    df = fuel_consumption_metadata_extraction()
    assert df.shape[1] == 2

def test_row_non_empty_fuel_consumption_metadata_extraction():
    df = fuel_consumption_metadata_extraction()
    assert df.shape[0] > 0

def test_col_names_fuel_consumption_metadata_extraction(): 
    df = fuel_consumption_metadata_extraction()
    assert df.columns.tolist() == ['name', 'url']
    
def test_name_type_fuel_consumption_metadata_extraction():
    df = fuel_consumption_metadata_extraction()
    assert df['name'].dtype == object

def test_url_type_fuel_consumption_metadata_extraction():
    df = fuel_consumption_metadata_extraction()
    assert df['url'].dtype == object

def test_url_non_empty_fuel_consumption_metadata_extraction():
    df = fuel_consumption_metadata_extraction()
    assert df['url'].isnull().sum() == 0

def test_name_non_empty_fuel_consumption_metadata_extraction():
    df = fuel_consumption_metadata_extraction()
    assert df['name'].isnull().sum() == 0

# Tests for read_and_clean_csv_file
def test_clean_fuel_consumption():
    sys.path.append(os.path.abspath(os.path.join('..','./data/clean-data/')))
    paths = sys.path
    ml_path = [item for item in paths if "machine-learning-capstone\\data\\clean-data" in item] 
    folder_path = ml_path[0]
    final_df = pd.read_csv(Path(folder_path, "1995_2022_vehicle_fuel_consumption.csv"))
    test_cols= final_df.columns == ['model_year', 'make_', 'model.1_', 'vehicleclass_', 'enginesize_(l)',
                                    'cylinders_', 'transmission_', 'fuel_type',
                                    'fuelconsumption_city(l/100km)', 'fuelconsumption_hwy(l/100km)',
                                    'fuelconsumption_comb(l/100km)', 'fuelconsumption_comb(mpg)',
                                    'co2emissions_(g/km)', 'co2_rating', 'smog_rating', 'transmission_type',
                                    'number_of_gears', 'mapped_fuel_type', 'type_of_wheel_drive']
    assert all(test_cols)==True

# Tests for extract_raw_data
def test_200_response_extract_raw_data():
    url = 'https://www.nrcan.gc.ca/sites/nrcan/files/oee/files/csv/MY2022%20Fuel%20Consumption%20Ratings.csv'
    url_content = extract_raw_data(url)
    assert url_content.status_code == 200
    

def test_no_none_extract_raw_data():
    url = 'https://www.nrcan.gc.ca/sites/nrcan/files/oee/files/csv/MY2022%20Fuel%20Consumption%20Ratings.csv'
    url_content = extract_raw_data(url).content
    assert url_content is not None

def test_type_extract_raw_data():
    url = 'https://www.nrcan.gc.ca/sites/nrcan/files/oee/files/csv/MY2022%20Fuel%20Consumption%20Ratings.csv'
    url_content = extract_raw_data(url).content
    assert type(url_content) == bytes



