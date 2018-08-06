#!/usr/bin/python3
# -*- coding: utf-8 -*-

from navegacion import hacer_peticion
from bs4 import BeautifulSoup
import urllib
import re

email_regex = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

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

def myip(p, u, i):
    """
    Devuelve la IP pública con la que se está realizando el request
    """
    print(hacer_peticion('http://ip.42.pl/raw', p, u, i).text)

class Buscador():
        
    def busqueda(self, dicc, query, proxy, user_agent, num_res=50, no_params=False, intervalo=0):
        return []
            
class BuscadorGoogle(Buscador):

    def __init__(self):
        self.nombre = "Google"

    def busqueda(self, dicc, query, proxy, user_agent, num_res=50, no_params=False, intervalo=0):
        return []

class BuscadorBing(Buscador):

    def __init__(self):
        self.nombre = "Bing"

    def banned(self, html):
        return False
    
    def busqueda(self, dicc, query, proxy, user_agent, num_res=50, no_params=False, intervalo=0):
        # myip(proxy, user_agent, intervalo)
        url = "http://www.bing.com/search?q="
        for k, v in dicc.items():
            if k == 'mail':
                url += '"@%s" ' % v
            elif k == 'exclude':
                url += '-%s ' % v
            elif k == 'include':
                url += '+%s ' % v
            elif k == 'inurl':
                url += "instreamset:url:%s " % v
            else:
                url += "%s:%s " % (k, v)
        url += '"%s"' % query
        resultados = {}
        first = 1
        while len(resultados) < num_res:
            res_nuevo = False
            url_p = '%s&first=%d' % (url, first)
            req = hacer_peticion(url_p, proxy, user_agent, intervalo)
            # print(req.url)
            soup = BeautifulSoup(req.text, 'lxml')
            [s.extract() for s in soup('span')]
            for match in soup.findAll('strong'):
                match.replaceWithChildren()
            results = soup.findAll('li', { "class" : "b_algo" })
            for result in results:
                if self.banned(result):
                    return None
                titulo = result.find('h2').text
                link = result.find('h2').find('a')['href']
                if not resultados.get(link, None):
                    res_nuevo = True
                descripcion = result.find('p').text
                if dicc.get('mail', None):
                    emails = re.findall(email_regex, titulo)
                    emails += re.findall(email_regex, descripcion)
                    if len(emails) > 0:
                        descripcion = "Correos electrónicos: %s" % ', '.join(emails)
                        resultados[link] = Resultado(link, titulo, descripcion)
                else:
                    resultados[link] = Resultado(link, titulo, descripcion)
            if not res_nuevo:
                break
            first += 10
        if no_params:
            tmp = {}
            for k, v in resultados.items():
                v.url = k.split('?', maxsplit=1)[0]
                tmp[v.url] = v
            return [v for k, v in tmp.items()]
        return [v for k, v in resultados.items()]

class BuscadorDuckduckgo(Buscador):

    def __init__(self):
        self.nombre = "DuckDuckGo"

    def busqueda(self, dicc, query, proxy, user_agent, num_res=50, no_params=False, intervalo=0):        
        return []

class BuscadorPastebin(Buscador):

    def __init__(self):
        self.nombre = "Pastebin"

    def busqueda(self, dicc, query, proxy, user_agent, num_res=50, no_params=False, intervalo=0):
        return []
    
class BuscadorBoardreader(Buscador):

    def __init__(self):
        self.nombre = "BoardReader"

    def busqueda(self, dicc, query, proxy, user_agent, num_res=50, no_params=False, intervalo=0):
        return []
