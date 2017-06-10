import scrapy

class tablasSpider(scrapy.Spider):
    name = "tablasSpider"

    def __init__(self, *args, **kwargs):
      super(tablasSpider, self).__init__(*args, **kwargs)

      lista = kwargs['start_urls']
      print(lista)

      self.start_urls = lista

    #start_urls = [
    #    'http://hyperphysics.phy-astr.gsu.edu/hbasees/electric/elefie.html'
    #]

    def parse(self, response):
        limpio = ""
        ultimo=''
        URL = response.url
        for linea in response.css('table td').extract():
            deboEscribir = True
            if '<h1' in linea:
                limpio+='\n==='
                limpio+=("Fuente: "+str(URL))

            for caracter in linea:
                if caracter=='<':
                    deboEscribir = False
                elif caracter=='>':
                    deboEscribir = True

                if deboEscribir:
                    if caracter=='\r':
                        caracter='\n'
                    elif caracter=='>':
                        caracter=''

                    if (ultimo=='\n' and caracter=='\n') or (ultimo==' ' and caracter==' '):
                        caracter=''

                    limpio+=caracter
                    ultimo = caracter
        with open('Resultados/Materia.txt', 'a+') as archivo:
            print("=================================")
            print("Guardando las tablas encontradas.")
            print("=================================")
            archivo.write(limpio)
