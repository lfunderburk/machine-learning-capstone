import pytest
from scripts.data_extraction import extract_raw_data

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



