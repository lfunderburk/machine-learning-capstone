import pandas as pd
import bs4
import requests
import requests
import seaborn as sns
import numpy as np
import sys
from pathlib import Path
import json
import re
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

global model_dict
global transmission_dict
global fuel_dict
model_dict = {"4WD/4X4":"Four-wheel drive",
	      "AWD": "All-wheel drive",
	      "FFV": "Flexible-fuel vehicle",
	      "SWB": "Short wheelbase",
	      "LWB" : "Long wheelbase",
	      "EWB" : "Extended wheelbase",
	      "CNG" : "Compressed natural gas",
	      "NGV" : "Natural gas vehicle",
	      "#" : "High output engine that provides more power than the standard engine of the same size"
 }

transmission_dict = {"A": "automatic",
		     "AM": "automated manual",
		     "AS": "automatic with select Shift",
		     "AV": "continuously variable",
		     "M": "manual",
		     "1 – 10" : "Number of gears",
}

fuel_dict = {"X": "regular gasoline",
	     "Z": "premium gasoline",
 	     "D": "diesel",
	     "E": "ethanol (E85)",
	     "N": "natural gas",
	     "B": "electricity"
	
}

def fuel_consumption_metadata_extraction() -> pd.DataFrame:
    """Extract metadata from fuel consumption data"""
    try:
        # Extract data in JSON format from URL
        url_open_canada = "https://open.canada.ca/data/api/action/package_show?id=98f1a129-f628-4ce4-b24d-6f16bf24dd64"
        json_resp = requests.get(url_open_canada)
        # Check response is successful and application is of type JSON
        if json_resp.status_code == 200 and 'application/json' in json_resp.headers.get('Content-Type',''):
            # Format data and obtain entries in english
            open_canada_data = json_resp.json()
            data_entries = pd.json_normalize(open_canada_data['result'], record_path="resources")
            data_entries['language'] = data_entries['language'].apply(lambda col: col[0])
            data_entries_english = data_entries[data_entries['language']=='en']
            final_result = data_entries_english[['name','url']]
        else:
            print("Error - check the url is still valid \
                https://open.canada.ca/data/api/action/package_show?id=98f1a129-f628-4ce4-b24d-6f16bf24dd64")
            final_result = pd.DataFrame(columns=['name','url'])
            sys.exit(1)
        return final_result
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)


def extract_raw_data(url:str):
    """Extract raw data from a URL"""
    try:
        
        # Perform query
        csv_req = requests.get(url)
        # Parse content
        url_content = csv_req.content
        
        return url_content
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)

def save_raw_data(folder_path: str, url_content: str):
    """This function saves the raw data obtained using extract_raw_data() into a CSV file"""
    # Save content into file
    csv_file = open(Path(folder_path,file_name), 'wb')
    csv_file.write(url_content)
    csv_file.close()

def read_and_clean_csv_file(folder_path, csv_file_name):
    """This function reads a csv file and performs data cleaning"""
    # Read CSV file
    df = pd.read_csv(Path(folder_path,csv_file_name), sep=",", low_memory=False, encoding='cp1252')
    
    # Data cleaning
    sample_df_col = df.dropna(thresh=1 ,axis=1).dropna(thresh=1 ,axis=0)
    sample_df_col.columns = [item.lower() for item in sample_df_col.columns]
    sample_df_no_footer = sample_df_col.dropna(thresh=3 ,axis=0)
    
    # Remove Unnamed cols
    cols = sample_df_no_footer.columns
    cleaned_cols = [re.sub(r'unnamed: \d*', "fuel consumption", item) if "unnamed" in item else item for item in cols]


    # Clean row 1 on df
    str_item_cols = [str(item) for item in sample_df_no_footer.iloc[0:1,].values[0]]
    str_non_nan = ["" if item=='nan' else item for item in str_item_cols]

    # Form new columns
    new_cols = []
    for itema,itemb in zip(cleaned_cols, str_non_nan):
        new_cols.append(f'{itema}_{itemb}'.lower().replace("*","").replace(" ","").replace(r'#=highoutputengine',""))


    final_df = sample_df_no_footer.iloc[1:, ].copy()
    final_df.columns = new_cols

    return final_df
    


def convert_model_key_words(s, dictionary):
    """Add values from footnote"""

    group = "unspecified"
    for key in dictionary:
        if key in s:
            group = dictionary[key]
            break
    return group


if __name__=='__main__':
    # Variable initialization
    raw_data_path = Path("C:/Users/Laura GF/Documents/GitHub/machine-learning-capstone/data/raw-data/")
    
    clean_data_path = Path("C:/Users/Laura GF/Documents/GitHub/machine-learning-capstone/data/clean-data/")
    
    # Master dataframe initialization
    fuel_based_df = []
    electric_based_df = []

    # Fuel consumption metadata extraction urls
    data_entries_english = fuel_consumption_metadata_extraction()
    
    # Iterate over entries
    for item in data_entries_english.iterrows():
        name, url = item[1]["name"], item[1]["url"]
        
        # Form file name
        file_name = f'{name.replace(" ","_")}.csv'

        # Extract raw data
        item_based_url  = extract_raw_data(raw_data_path, url)

        # Save raw data into a csv file
        save_raw_data(raw_data_path,item_based_url)
        
        # Read and clean csv file
        final_df = read_and_clean_csv_file(raw_data_path, item[1]['name'].replace(" ","_")+".csv")