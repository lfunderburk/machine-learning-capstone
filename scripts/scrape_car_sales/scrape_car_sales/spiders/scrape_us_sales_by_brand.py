import scrapy

class CarSalesSpider(scrapy.Spider):
    name="sales-brand"
    start_urls = ["https://www.goodcarbadcar.net/acura-us-sales-figures/",
                  "https://www.goodcarbadcar.net/audi-us-sales-figures/",]

    def parse(self, response):
        header = response.xpath('//*[@id="table_1"]/thead/tr/th/text()').getall()
        rows = response.xpath('//*[@id="table_1"]/tbody/tr/td/text()').getall()

        yield {
            'col_names': header,
            'data': rows
        }

        

        

