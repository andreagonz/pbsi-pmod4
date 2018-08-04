from navegacion import hacer_peticion
from bs4 import BeautifulSoup
import urllib

class FabricaBuscador():

    def get_buscador(self, nombre):
        if nombre == 'google':
            return BuscadorGoogle()
        if nombre == 'bing':
            return BuscadorBing()
        if nombre == 'duckduckgo':
            return BuscadorDuckduckgo()
        if nombre == 'pastebin':
            return BuscadorPastebin()
        if nombre == 'boardreader':
            return BuscadorBoardreader()
        if nombre == 'zone-h':
            return BuscadorZoneH()
        return None
        
class Resultado():

    def __init__(self, url, titulo, texto):
        self.url = url
        self.titulo = titulo
        self.texto = texto

class Buscador():

    def busqueda(self, dicc, query, max_res=50, no_params=False):
        return []
            
class BuscadorGoogle(Buscador):

    def busqueda(self, dicc, query, max_res=50, no_params=False):
        return []

class BuscadorBing(Buscador):

    def busqueda(self, dicc, query, max_res=50, no_params=False):
        url = "http://www.bing.com/search?q=%s" % (query)
        req = hacer_peticion(url)
        soup = BeautifulSoup(req.text, 'lxml')
        [s.extract() for s in soup('span')]
        unwantedTags = ['a', 'strong', 'cite']
        for tag in unwantedTags:
            for match in soup.findAll(tag):
                match.replaceWithChildren()
        results = soup.findAll('li', { "class" : "b_algo" })
        resultados = []
        for result in results:
            titulo = str(result.find('h2'))
            url = type(result.find('h2').find('a'))
            descripcion = str(result.find('p'))
            resultados.append(Resultado(url, titulo, descripcion))
        return resultados

class BuscadorDuckduckgo(Buscador):

    def busqueda(self, dicc, query, max_res=50, no_params=False):        
        return []

class BuscadorPastebin(Buscador):

    def busqueda(self, dicc, query, max_res=50, no_params=False):
        return []
    
class BuscadorBoardreader(Buscador):

    def busqueda(self, dicc, query, max_res=50, no_params=False):
        return []
    
class BuscadorZoneH(Buscador):

    def busqueda(self, dicc, query, max_res=50, no_params=False):
        return []
