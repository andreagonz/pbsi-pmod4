#!/usr/bin/python3
# -*- coding: utf-8 -*-

from navegacion import hacer_peticion
from bs4 import BeautifulSoup
from aux import email_regex, printError
import urllib
import re

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
    print("IP pública: %s" % hacer_peticion('http://ip.42.pl/raw', p, u, i).text)

class Buscador():

    def get_emails(self, link, titulo, descripcion, resultados):
        emails = re.findall(email_regex, titulo)
        emails += re.findall(email_regex, descripcion)
        if len(emails) > 0:
            descripcion = "Correos electrónicos: %s" % ', '.join(emails)
            resultados[link] = Resultado(link, titulo, descripcion)

    def get_url(self, dicc, query):
        return ""

    def obten_resultados(self, url, resultados, iteracion, proxy,
                         user_agent, intervalo, obten_emails, verboso=False):
        return 0
    
    def busqueda(self, dicc, query, proxy, user_agent, num_res=50,
                 no_params=False, intervalo=0, verboso=False):
        if verboso:
            myip(proxy, user_agent, intervalo)
            print("Expansión: %s %s" % (dicc, query))
        url = self.get_url(dicc, query)
        resultados = {}
        iteracion = 0
        while len(resultados) < num_res:
            nuevos = self.obten_resultados(url, resultados, iteracion, proxy, user_agent,
                                           intervalo, not dicc.get('mail', None) is None, verboso)
            if nuevos == 0:
                break
            elif nuevos < 0:
                return None
            iteracion += 1
        if no_params:
            tmp = {}
            for k, v in resultados.items():
                v.url = k.split('?', maxsplit=1)[0]
                tmp[v.url] = v
            return [v for k, v in tmp.items()]
        return [v for k, v in resultados.items()]
            
class BuscadorGoogle(Buscador):

    def __init__(self):
        self.nombre = "Google"

    def banned(self, html):
        return False
    
    def get_url(self, dicc, query):
        url = "https://www.google.com/search?q="
        for k, v in dicc.items():
            if k == 'mail':
                url += '"@%s" ' % v
            elif k == 'exclude':
                url += '-%s ' % v
            elif k == 'include':
                url += '+%s ' % v
            else:
                url += "%s:%s " % (k, v)
        return '%s"%s"' % (url, query)

    def obten_resultados(self, url, resultados, iteracion, proxy,
                         user_agent, intervalo, obten_emails, verboso=False):
        url_p = '%s&start=%d' % (url, iteracion * 10)
        req = hacer_peticion(url_p, proxy, user_agent, intervalo)
        if verboso:
            print("URL de búsqueda: %s" % req.url)
        soup = BeautifulSoup(req.text, 'lxml')
        if self.banned(soup.text):
            return -1
        print(soup)
        [s.extract() for s in soup('span')]
        for match in soup.findAll('strong'):
            match.replaceWithChildren()
        results = soup.findAll('li', { "class" : "b_algo" })
        total = 0
        for result in results:
            titulo = result.find('h2').text
            link = result.find('h2').find('a')['href']
            if not resultados.get(link, None):
                total += 1
                descripcion = result.find('p').text
                if obten_emails:
                    self.get_emails(link, titulo, descripcion, resultados)
                else:
                    resultados[link] = Resultado(link, titulo, descripcion)
        return total

class BuscadorBing(Buscador):

    def __init__(self):
        self.nombre = "Bing"

    def banned(self, html):
        return False

    def get_url(self, dicc, query):
        url = "https://www.bing.com/search?q="
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
        return '%s%s' % (url, '"%s"' % query if query else '')

    def obten_resultados(self, url, resultados, iteracion, proxy,
                         user_agent, intervalo, obten_emails, verboso=False):
        url_p = '%s&first=%d' % (url, iteracion * 10 + 1)
        req = hacer_peticion(url_p, proxy, user_agent, intervalo)
        if verboso:
            print("URL de búsqueda: %s" % req.url)
        soup = BeautifulSoup(req.text, 'lxml')
        if self.banned(soup.text):
            return -1
        [s.extract() for s in soup('span')]
        for match in soup.findAll('strong'):
            match.replaceWithChildren()
        results = soup.findAll('li', { "class" : "b_algo" })
        total = 0
        for result in results:
            titulo = result.find('h2').text
            link = result.find('h2').find('a')['href']
            if not resultados.get(link, None):
                total += 1
                descripcion = result.find('p').text
                if obten_emails:
                    self.get_emails(link, titulo, descripcion, resultados)
                else:
                    resultados[link] = Resultado(link, titulo, descripcion)
        return total
                
class BuscadorDuckduckgo(Buscador):

    def __init__(self):
        self.nombre = "DuckDuckGo"

class BuscadorPastebin(Buscador):

    def __init__(self):
        self.nombre = "Pastebin"
    
class BuscadorBoardreader(Buscador):

    def __init__(self):
        self.nombre = "BoardReader"
