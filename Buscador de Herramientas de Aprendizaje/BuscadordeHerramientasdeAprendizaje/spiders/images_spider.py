import scrapy


class imageSpider(scrapy.Spider):
    name = "imagenes"

    def start_requests(self):
        urls = [
            'https://es.wikipedia.org/wiki/Voltio',
            'http://hyperphysics.phy-astr.gsu.edu/hbase/electric/elefie.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        #wikipedia format
        for quote in response.css('div.thumbinner'):
            if("wikipedia" in response.url):
                yield {
                    'URL': 'https:'+ quote.css('img::attr(src)').extract_first(),
                    'source': response.url
                }
                with open('Resultado.txt', 'a') as archivo:
                    print("Voy a escribir")
                    archivo.write('https:'+ quote.css('img::attr(src)').extract_first()+'\n')

        #hyperphysics format
        for image in response.css('img::attr(src)').extract():
            if("hyperphysics" in response.url):
                yield{
                    'URL': response.urljoin(image),
                    'source': response.url
                }
                with open('Resultado.txt', 'a') as archivo:
                    print("Voy a escribir")
                    archivo.write(response.urljoin(image)+'\n')

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
