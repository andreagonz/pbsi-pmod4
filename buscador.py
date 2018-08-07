#!/usr/bin/python3
# -*- coding: utf-8 -*-

from urllib.parse import urljoin, parse_qs, urlparse
from aux import email_regex, printError
from navegacion import hacer_peticion
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import urllib
import json
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
        """
        Busca correos electrónicos en titulo y descripcion, crea un objeto
        Resultado con los hallazgos y los agrega al diccionario resultados.
        """
        emails = re.findall(email_regex, titulo)
        emails += re.findall(email_regex, descripcion)
        if len(emails) > 0:
            descripcion = "Correos electrónicos: %s" % ', '.join(emails)
            resultados[link] = Resultado(link, titulo, descripcion)

    def get_url(self, dicc, query):
        """
        Usando el diccionario de términos dicc, y la búsqueda query, regresa el url
        de una consulta.
        dicc contiene las llaves ip, filetype, site, exclude, include, inurl y mail.
        """
        return ""

    def obten_resultados(self, url, resultados, iteracion, proxy,
                         user_agent, intervalo, obten_emails, verboso=False):
        """
        Obtiene los resultados de la búsqueda con la url proporcionada, de acuerdo al
        número de iteración en el que se está, para hacer la petición hace uso de proxy,
        user_agent e intervalo.
        Si obten_emails es verdadero, se indica que se obtengan los correos de los
        resultados de la busqúeda.
        Guarda los objetos Resultado en el diccionario resultados (llave url, valor Resultado)
        resultados es un diccionario con urls como llave, y objetos Resultado como valor.
        Regresa el total de resultados nuevos encontrados
        Regresa -1 si se descubre que la ip ha sido bloqueada        
        """
        return 0
    
    def busqueda(self, dicc, query, proxy, user_agent, num_res=50,
                 no_params=False, intervalo=0, verboso=False):
        """
        Efectúa una búsqueda usando el diccionario de términos dicc y la búsqueda query.
        Toma num_res como un límite de resultados aproximado, para cada petición se utiliza
        proxy, user_agent e intervalo.
        Si no_params es verdadero, se ignoran los parámetros GET.
        Regresa una lista de objetos Resultado.
        Regresa None si la ip ha sido bloqueada.
        """
        if verboso:
            print("Fecha: %s" % datetime.now().strftime('%d-%b-%Y %H:%M:%S'))
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

    def banned(self, url):
        """
        Regresa True syss la url indica que se ha bloqueado a la IP.
        """
        return url.startswith('https://www.google.com/sorry/index')
    
    def get_url(self, dicc, query):
        url = "https://www.google.com/search?q="
        for k, v in dicc.items():
            if k == 'mail':
                url += '"@%s" ' % v
            elif k == 'exclude':
                url += '-%s ' % v
            elif k == 'include':
                url += '+%s ' % v
            elif k == 'exact_word':
                url += '"%s" ' % v
            else:
                url += "%s:%s " % (k, v)
        return '%s%s' % (url, query)

    def obten_resultados(self, url, resultados, iteracion, proxy,
                         user_agent, intervalo, obten_emails, verboso=False):
        url_p = '%s&start=%d' % (url, iteracion * 10)
        req = hacer_peticion(url_p, proxy, user_agent, intervalo)
        if verboso:
            print("URL de búsqueda: %s" % req.url)
        soup = BeautifulSoup(req.text, 'lxml')
        if self.banned(req.url):
            if verboso:
                print('IP bloqueada\n')
            return -1
        results = soup.findAll('div', { "class" : "g" })
        total = 0
        for result in results:
            if result.find('img'):
                continue
            r = result.find('h3', {'class' : 'r'})
            titulo = r.text if r else ''
            s = result.find('div', {'class': 's'})
            descripcion = s.find('span', {'class': 'st'}).text if s else ''
            link = r.find('a').get('href', '') if r else ''
            if link.startswith('/url?'):
                link = urljoin('https://google.com/', link)
            if not resultados.get(link, None):
                total += 1
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
            elif k == 'exact_word':
                url += '"%s" ' % v
            else:
                url += "%s:%s " % (k, v)
        return '%s%s' % (url, query)

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
            h2 = result.find('h2')
            titulo = h2.text if h2 else ''
            a = h2.find('a') if h2 else None
            link = a.get('href', '') if a else ''
            if not resultados.get(link, None):
                total += 1
                p = result.find('p')
                descripcion = p.text if p else ''
                if obten_emails:
                    self.get_emails(link, titulo, descripcion, resultados)
                else:
                    resultados[link] = Resultado(link, titulo, descripcion)
        return total
                
class BuscadorDuckduckgo(Buscador):

    def __init__(self):
        self.nombre = "DuckDuckGo"

    def banned(self, raw):
        return 'If this error persists, please let us know: error-lite@duckduckgo.com' in raw
    
    def get_url(self, dicc, query):
        url = "https://duckduckgo.com/html/"
        q = ""
        for k, v in dicc.items():
            if k == 'mail':
                q += '"@%s" ' % v
            elif k == 'exclude':
                q += '-%s ' % v
            elif k == 'include':
                q += '+%s ' % v
            elif k == 'exact_word':
                url += '"%s" ' % v
            else:
                q += "%s:%s " % (k, v)
        return url, ('%s%s' % (q, query)).strip()

    def obten_resultados(self, url, resultados, iteracion, proxy,
                         user_agent, intervalo, obten_emails, verboso=False):
        url_p, q = url
        data = {'q' : q, 'kl' : 'us-en'}
        if iteracion > 0:
            data['api'] = '/d.js'
            data['o'] = 'json'
            data['v'] = 'l'
            data['dc'] = 31 if iteracion == 1 else ((iteracion - 1) * 50) + 31
            data['s'] = 30 if iteracion == 1 else data['dc'] - 1
        req = hacer_peticion(url_p, proxy, user_agent, intervalo, True, data)
        if verboso:
            print("URL de búsqueda: %s" % req.url)
            print("Data: %s" % data)
        soup = BeautifulSoup(req.text, 'lxml')
        if self.banned(req.text):
            if verboso:
                print('IP bloqueada\n')
            return -1
        results = soup.findAll('div', { "class" : "result" })
        total = 0
        for result in results:
            r = result.find('h2', {'class' : 'result__title'})
            titulo = r.text.strip() if r else ''
            a = r.find('a', {'class', 'result__a'}) if r else None
            link = a.get('href', '') if a else ''
            s = result.find('a', {'class': 'result__snippet'})
            descripcion = s.text if s else ''
            if not resultados.get(link, None) and a:
                total += 1
                if obten_emails:
                    self.get_emails(link, titulo, descripcion, resultados)
                else:
                    resultados[link] = Resultado(link, titulo, descripcion)
        return total
    
class BuscadorPastebin(Buscador):

    def __init__(self):
        self.nombre = "Pastebin"

    def get_url(self, dicc, query):
        dicc['site'] = 'pastebin.com'
        return BuscadorGoogle().get_url(dicc, query)
    
    def obten_resultados(self, url, resultados, iteracion, proxy,
                         user_agent, intervalo, obten_emails, verboso=False):
        return BuscadorGoogle().obten_resultados(url, resultados, iteracion, proxy,
                         user_agent, intervalo, obten_emails, verboso)
    
class BuscadorBoardreader(Buscador):

    def __init__(self):
        self.nombre = "BoardReader"

    def banned(self, html):
        return False
    
    def get_url(self, dicc, query):
        url = "https://boardreader.com/return.php?query="
        for k, v in dicc.items():
            if k == 'mail':
                url += '"@%s" ' % v
            elif k == 'exclude':
                url += '-%s ' % v
            elif k == 'include':
                url += '%s ' % v
            elif k == 'exact_word':
                url += '"%s" ' % v
        url = '%s%s&language=English' % (url, '%s' % query if query else '')
        return url + "&domain=%s" % dicc['site'] if dicc.get('site', None) else url

    def obten_resultados(self, url, resultados, iteracion, proxy,
                         user_agent, intervalo, obten_emails, verboso=False):
        s = requests.Session()
        url_b = 'https://boardreader.com'
        req = hacer_peticion(url_b, proxy, user_agent, intervalo, sesion=s)
        if self.banned(req.text):
            return -1
        url_p = url + "&page=%d" % (iteracion + 1)
        req = hacer_peticion(url_p, proxy, user_agent, intervalo, sesion=s)
        if verboso:
            print("URL de búsqueda: %s" % req.url)
        data = json.loads(req.text)
        if not data.get('SearchResults', None):
            return 0        
        results = data['SearchResults']
        total = 0
        for result in results:
            titulo = result.get('Subject', '').replace('[Keyword]', '').replace('[/Keyword]', '')
            link = result.get('Url', '')
            if not resultados.get(link, None):
                total += 1
                descripcion = result.get('Text', '').replace('[Keyword]', '').replace('[/Keyword]', '').replace('\n', ' ')
                if obten_emails:
                    self.get_emails(link, titulo, descripcion, resultados)
                else:
                    resultados[link] = Resultado(link, titulo, descripcion)
        return total
