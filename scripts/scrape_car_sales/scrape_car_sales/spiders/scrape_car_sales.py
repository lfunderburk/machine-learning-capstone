import scrapy

class CarSalesSpider(scrapy.Spider):
    name = "car-sales"

    start_urls = ['https://www.goodcarbadcar.net/2019-canada-vehicle-sales-figures-by-model/#monthlysales/']
    
    def parse(self, response):
        table = response.xpath('//*[@id="table_3"]/tbody')
        rows = table.xpath('//tr')

        for row in rows:
            yield {
                'model' : row.xpath('td[1]//text()').extract_first(),
                'jan': row.xpath('td[2]//text()').extract_first(),
                'feb': row.xpath('td[3]//text()').extract_first(),
                'mar': row.xpath('td[4]//text()').extract_first(),
                'apr': row.xpath('td[5]//text()').extract_first(),
                'may': row.xpath('td[6]//text()').extract_first(),
                'jun': row.xpath('td[7]//text()').extract_first(),
                'jul': row.xpath('td[8]//text()').extract_first(),
                'aug': row.xpath('td[9]//text()').extract_first(),
                'sep': row.xpath('td[10]//text()').extract_first(),
                'oct': row.xpath('td[11]//text()').extract_first(),
                'nov': row.xpath('td[12]//text()').extract_first(),
                'dec': row.xpath('td[13]//text()').extract_first()
            }