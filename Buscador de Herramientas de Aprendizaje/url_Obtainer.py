import json
import urllib.request, urllib.parse

import query
class urlObtainer():
    def __init__(self, confiable, *args, **kwargs):
        self.listaConfiable = confiable

    def urlGetter(self, queryString):
        urlList = []
        cache = urlCache(queryString)
        for dominio in self.listaConfiable:
            listCache = cache.returnCache(dominio)
            if(listCache[0]):
                urlList.append(listCache[1])
            else:
                query = urllib.parse.urlencode({'q': queryString+" :"+dominio})
                url = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyDDKM1YteR8id4T1GwOQlTcm_agVGAwQUQ&cx=006325309441217833254:vcjnhphmc4i&' + query
                try:
                    search_response = urllib.request.urlopen(url)
                    search_result = search_response.read().decode("utf8")
                    results = json.loads(search_result)
                    data = results['items']
                    #print(data)
                    resultado = data[0]['link']
                    if(dominio in resultado):
                        urlList.append(resultado)
                        cache.insertCache(dominio, resultado)
                    print(resultado)

                except TypeError:
                    print("Error al buscar, por favor intente más tarde (?)")
                except KeyError:
                    print("No se encontraron resultados")


        return urlList

'''
Uso de la clase

Para instanciarla
urlObtain = urlObtainer(['hyperphysics','wikipedia'])


Para usar su método
urlObtain.urlGetter('Campo Electrico')
'''

class urlCache():
    def __init__(self, queryString):
        self.string = queryString.lower()
        self.urlDic = {}
        db = query.query()
        db.conectar()
        rows = db.select('StringBusqueda, Dominio, URL','WHERE StringBusqueda = \''+self.string+'\'', tabla ='Cache')
        if(len(rows) != 0):
            for row in rows:
                a, b , c = row
                self.urlDic[b] = c

    def returnCache(self, Dominio):
        if(Dominio in self.urlDic):
            return [True, self.urlDic[Dominio]]
        else:
            return [False, None]

    def insertCache(self, Dominio, Url):
        db = query.query()
        db.conectar()
        db.insert(tabla = 'Cache', stringBusqueda = self.string, dominio = Dominio, url = Url)
        print("inserté en el caché")
