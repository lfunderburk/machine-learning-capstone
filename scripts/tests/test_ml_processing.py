from scripts.machine_learning_pre_processing import remove_duplicate_rows
from pathlib import Path

def test_remove_duplicate_rows_fuel_consumption():
    folder_path =  Path("C:/Users/Laura GF/Documents/GitHub/machine-learning-capstone/data/clean-data/") 
    csv_file_name = "1995_2022_vehicle_fuel_consumption.csv"
    test_df = remove_duplicate_rows(folder_path, csv_file_name)
    assert test_df.duplicated().sum()==0
