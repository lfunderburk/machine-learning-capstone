import pytest
from scripts.data_extraction import extract_raw_data, save_raw_data

def test_extract_raw_data():
    url = "https://www.fueleconomy.gov/feg/download.shtml"
    df = extract_raw_data(url)
    assert df.shape[0] > 0
    assert df.shape[1] > 0
    assert df.columns[0] == "Model"
