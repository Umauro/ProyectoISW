import scrapy


class imagenSpider(scrapy.Spider):
    name = "imagen"

    #def __init__(self, *args, **kwargs):
    #  super(imagenSpider, self).__init__(*args, **kwargs)
    #  print(kwargs)
    #  lista = kwargs['start_urls']
    #  print(lista)

    #  self.start_urls = lista

    start_urls = [
        'http://hyperphysics.phy-astr.gsu.edu/hbasees/electric/elefie.html'
    ]

    def parse(self, response):
        for url in response.css('img::attr(src)').extract():

            with open('Resultados/StringsLimpios.txt', 'a+') as archivo:
                print("Voy a escribir")
                archivo.write(response.urljoin(url)+'\n')
