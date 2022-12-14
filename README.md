# Machine Learning Capstone 
Repository for capstone project done as part of University of California San Diego [Machine Learning Engineering Bootcamp](https://career-bootcamp.extension.ucsd.edu/programs/machine-learning-engineering/)

### Project author: Laura G. Funderburk
## Setting up

Clone this repository.

## Create a virtual environment

Execute the following

```
cd machine-learning-capstone/
conda env create -f environment.yml
```

If something fails during pip command installation, execute

```
conda activate ml-project-env
pip install -r requirements
```

You can use the environment on a Jupyter notebook via the command

```
python -m ipykernel install --user --name ml-project-env --display-name "Python MP Capstone"
```

## Using the data pipeline

This script uses Scrapy to scrape data from the following website: https://www.goodcarbadcar.net/

```
cd scripts/scrape_car_sales/scrape_car_sales/

scrapy crawl car-sales2019 -o "file:///path_to_repo\machine-learning-capstone/data/raw-data/2019_canada_vehicle_sales.json" -t json
scrapy crawl car-sales2020 -o "file:///path_to_repo\machine-learning-capstone/data/raw-data/2020_canada_vehicle_sales.json" -t json
scrapy crawl car-sales2021 -o "file:///path_to_repo\machine-learning-capstone/data/raw-data/2021_canada_vehicle_sales.json" -t json
```

Then from the root directory, i.e. from machine-learning-capstone\

```
ploomber build
```

If everything goes well, you should see

```
Loading pipeline...
Executing: 100%|████████████████████████████████████| 18/18 [00:15<00:00,  1.14cell/s]
Building task 'data_extraction': 100%|██████████████████| 1/1 [00:15<00:00, 15.84s/it]
name             Ran?      Elapsed (s)    Percentage
---------------  ------  -------------  ------------
data_extraction  True          15.8406           100
```
