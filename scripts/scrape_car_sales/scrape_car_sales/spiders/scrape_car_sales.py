import scrapy

class CarSalesSpider(scrapy.Spider):
    name = "car-sales"

    start_urls = ['https://www.goodcarbadcar.net/2019-canada-vehicle-sales-figures-by-model/']
    
    def parse(self, response):
        table = response.xpath('//*[@id="table_3"]/tbody')
        rows = table.xpath('//tr[contains(@id,"table_3566")]')

        for row in rows:
            yield {
                'model' : row.xpath('td[1]//text()').get(),
                'jan': row.xpath('td[2]//text()').get(),
                'feb': row.xpath('td[3]//text()').get(),
                'mar': row.xpath('td[4]//text()').get(),
                'apr': row.xpath('td[5]//text()').get(),
                'may': row.xpath('td[6]//text()').get(),
                'jun': row.xpath('td[7]//text()').get(),
                'jul': row.xpath('td[8]//text()').get(),
                'aug': row.xpath('td[9]//text()').get(),
                'sep': row.xpath('td[10]//text()').get(),
                'oct': row.xpath('td[11]//text()').get(),
                'nov': row.xpath('td[12]//text()').get(),
                'dec': row.xpath('td[13]//text()').get()
            }