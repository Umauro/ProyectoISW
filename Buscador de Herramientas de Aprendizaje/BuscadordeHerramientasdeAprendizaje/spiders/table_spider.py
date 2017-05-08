import scrapy


class tablaSpider(scrapy.Spider):
    name = "tablas"

    def start_requests(self):
        urls = [
            'https://es.wikipedia.org/wiki/Voltio',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for table in response.css('table.wikitable'):
            yield {
                'caption': table.css('caption').extract_first(),
                'tr': table.css('tr').extract(),
                'td': table.css('td').extract()
            }
        
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
