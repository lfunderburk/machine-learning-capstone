# import the necessary libraries
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
import pandas as pd

class FuelEconomySpider(Spider):
    name = "fuel_economy"
    start_urls = ["https://www.fueleconomy.gov/feg/download.shtml"]

    def parse(self, response):
        # extract the URLs of the .zip files from the HTML
        sel = Selector(response)
        zip_urls = sel.xpath('//li/a[contains(@href, ".zip")]/@href').extract()

        # download the .zip files and save them to a .csv file
        rows = []
        for zip_url in zip_urls:
            request = Request(zip_url, callback=self.save_zip)
            response = request.meta["zip_response"]
            rows.append({"zip_url": zip_url, "zip_data": response.body})
        df = pd.DataFrame(rows)
        df.to_csv("zip_files.csv", index=False)

    def save_zip(self, response):
        # save the .zip file to the request metadata
        request = response.request
        request.meta["zip_response"] = response
        return request