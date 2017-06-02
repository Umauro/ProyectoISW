
import json
import urllib.request, urllib.parse

class urlObtainer():
    def __init__(self, confiable, *args, **kwargs):
        self.listaConfiable = confiable

    def urlGetter(self, queryString):
        for dominio in self.listaConfiable:
            query = urllib.parse.urlencode({'q': queryString+" :"+dominio})
            url = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyDDKM1YteR8id4T1GwOQlTcm_agVGAwQUQ&cx=006325309441217833254:vcjnhphmc4i&' + query
            try:
                search_response = urllib.request.urlopen(url)
                search_result = search_response.read().decode("utf8")
                results = json.loads(search_result)
                data = results['items']
                #print(data)
                resultado = data[0]['link']
                print(resultado)

            except TypeError:
                print("D:")

urlObtain = urlObtainer(['hyperphysics','wikipedia'])

urlObtain.urlGetter('Campo Electrico')
