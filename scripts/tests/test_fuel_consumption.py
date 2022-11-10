from scripts.data_extraction import fuel_consumption_metadata_extraction
import tempfile 

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