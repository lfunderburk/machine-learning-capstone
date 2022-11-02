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

Then open jupyter via

```
jupyter lab
```
## Download data

This script uses Scrapy to scrape data from a website. Sample execution for this page

https://www.goodcarbadcar.net/2019-canada-vehicle-sales-figures-by-model/#monthlysales/

```
cd scripts/scrape_car_sales/scrape_car_sales/

scrapy crawl car-sales -o 2019_canada_vehicle_sales.json
```


