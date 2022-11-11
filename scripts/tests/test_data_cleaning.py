import pytest
from scripts.data_extraction import read_and_clean_csv_file
from pathlib import Path

def test_two_cols_read_and_clean_csv_file():
    folder_path =  Path("C:/Users/Laura GF/Documents/GitHub/machine-learning-capstone/data/raw-data/") 
    csv_file_name = "2019-20_Fuel_Consumption_Ratings.csv"
    test_df  = read_and_clean_csv_file(folder_path, csv_file_name)