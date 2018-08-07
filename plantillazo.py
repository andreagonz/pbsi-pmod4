#!/usr/bin/python3
# -*- coding: utf-8 -*-
#UNAM-CERT

"""
Se debe instalar TOR
Debian: apt-get install tor
Iniciarlo: service tor start o simplemente colocar el comado tor (Depende de como es que se haya instalado)
De igual forma se debe instalar socks
Debian: apt-get install python3-socks

Ademas instalar:

apt-get install python3-pip
pip3 install exrex
pip3 install BeautifulSoup4
pip3 install lxml

"""

import sys
import exrex
import optparse
from random import randint
from formato import formato
from buscador import FabricaBuscador
from aux import user_agents, proxies, printError

def addOptions():
    """
    Aquí se configuraron las banderas posibles para la ejecución del programa
    """
    parser = optparse.OptionParser()
    parser.add_option('-v', '--verbose', dest='verbose', default=None, action='store_true', help='Indica que se utilice el modo verboso.')
    parser.add_option('-n', '--num-res', dest='num_res', default='50', help='Numero de resultados por busqueda')
    parser.add_option('-b', '--buscadores', dest='buscadores', default='google', help='Se especifica el buscador a utilizar')
    parser.add_option('-N', '--no-params', dest='no_params', default=False, action='store_true', help='Excluye los parametros GET, haciendo unica cada busqueda')
    parser.add_option('-r', '--regex', dest='regex', default=False, action="store_true", help='Se pueden usar Expresiones Regulares')
    parser.add_option('-d', '--domains', dest='domains', default=False, action="store_true", help='Se usa para especificar el o los dominios de busqueda')
    parser.add_option('-U', '--user-agents', dest='user_agents', default=None, help='Archivo con agentes de usuario a utilizar, separados por un salto de linea')
    parser.add_option('-P', '--proxies', dest='proxies', default=None, help='Archivo con proxies a utilizar, separados por un salto de linea')
    parser.add_option('-F', '--formato', dest='formato', default='txt', help='Especifica el formato de salida')
    parser.add_option('-i', '--intervalo', dest='intervalo', default='0', help='Se especifica el intervalo de tiempo por busqueda')
    parser.add_option('-p', '--ip', dest='ip', default=None, help='Se especifica la(s) IP(s) de busqueda, separadas por una coma')
    parser.add_option('-m', '--mail', dest='mail', default=None, help='Busca correos electronicos en los dominios especificado, separados por una coma')
    parser.add_option('-f', '--filetype', dest='filetype', default=None, help='Se busca por los tipos de archivo especificados, separados por una coma')
    parser.add_option('-s', '--site', dest='site', default=None, help='Se busca por los sitios web especificados, separados por una coma')
    parser.add_option('-e', '--exclude', dest='exclude', default=None, help='Se excluyen los resultados que contengan esa palabra')
    parser.add_option('-I', '--include', dest='include', default=None, help='Se incluyen los resultados que contengan esa palabra')
    parser.add_option('-u', '--inurl', dest='inurl', default=None, help='Se busca las palabras dentro de la url, separadas por comas')
    return parser.parse_args()

def lee_proxies(p_lst):
    with open(p_lst) as f:
        for p in f.readlines():
            tmp = {}
            l = [x.strip().split('=') for x in p.split(',')]
            for x in l:
                if x[0] == 'http':
                    tmp['http'] = x[1]
                elif x[0] == 'https':
                    tmp['https'] = x[1]
            if len(tmp) > 0:
                proxies.append(tmp)

def lee_user_agents(ua):
    with open(ua) as f:
        for u in f.readlines():
            user_agents.append(u.strip())

def int_or_0(n):
    try:
        return int(n) if int(n) >= 0 else 0
    except:
        return 0

def agrega(lst, nom, op):
    if not op:
        return
    l = [x.strip() for x in op.split(',')]
    e = l.pop()
    for x in lst:
        x[nom] = e;
    while len(l) > 0:
        e = l.pop()
        for x in lst.copy():
            lst.append(dict(x))
            lst[-1][nom] = e
    
def expandir(queries, opts):
    """
    Regresa una lista de tuplas t, cada t tiene la forma (dicc, q), donde dicc es
    un diccionario de términos y q es una cadena de búsqueda.
    """
    lst = [{}]
    agrega(lst, 'ip', opts.ip)
    agrega(lst, 'filetype', opts.filetype)
    agrega(lst, 'site', opts.site)
    agrega(lst, 'exclude', opts.exclude)
    agrega(lst, 'include', opts.include)
    agrega(lst, 'inurl', opts.inurl)
    agrega(lst, 'mail', opts.mail)
    return [(d, q) for q in queries for d in lst if len(d) > 0 or len(q) > 0]

if __name__ == '__main__':
    try:
        opts, args = addOptions()
        if len(args) == 0 and not opts.mail and not opts.ip and \
           not opts.filetype and not opts.inurl and not opts.site:
            print("Uso: python3 %s {<busqueda> [opciones] | {f --filetype | s --site | h --help | "
                  "p --ip | u --inurl | m --mail} [opciones]" % sys.argv[0])
            sys.exit(1)
        if opts.proxies:
            lee_proxies(opts.proxies)
        if opts.user_agents:
            lee_user_agents(opts.user_agents)
        buscadores = []
        fabrica = FabricaBuscador()
        for x in opts.buscadores.split(','):
            buscadores.append(fabrica.get_buscador(x.strip()))
        q = [x.strip() for x in args[0].split('+')] if len(args) > 0 else [""]
        queries = [y for x in q for y in list(exrex.generate(x))] if opts.regex else q
        expansiones = expandir(queries, opts)
        if opts.verbose:
            print("Expansiones: %s\n" % str(expansiones))
        intervalo = int_or_0(opts.intervalo)
        num_res = int_or_0(opts.num_res)
        resultados = {}
        for d, q in expansiones:
            i = randint(0, len(proxies) - 1)
            proxy = proxies[i]
            for b in buscadores:
                user_agent = user_agents[randint(0, len(user_agents) - 1)]
                r = b.busqueda(d, q, proxy, user_agent, num_res,
                               opts.no_params, intervalo, opts.verbose)
                if not r:
                    for x in range(len(proxies)):
                        i = (i + 1) % len(proxies)
                        proxy = proxies[i]
                        r = b.busqueda(d, q, proxy, user_agent, num_res,
                                       opts.no_params, intervalo, opts.verbose)
                        if r: break
                r = r if r else []
                if not resultados.get(b.nombre, None):
                    resultados[b.nombre] = []
                for x in r:                    
                    resultados[b.nombre].append(x)
        formato(resultados, opts.formato, opts.domains)
    except Exception as e:
        printError(e)
