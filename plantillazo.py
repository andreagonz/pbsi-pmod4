#!/usr/bin/python3
# -*- coding: utf-8 -*-
#UNAM-CERT

"""
Se debe instalar TOR
Debian: apt-get install TOR
Iniciarlo: service tor start o simplemente colocar el comado tor (Depende de como es que se haya instalado)
De igual forma se debe instalar socks
Debian: apt-get install python-socks
"""

import sys
import exrex
import optparse
from random import randint
from formato import formato
from buscador import FabricaBuscador

user_agents = ['firefox', 'chrome']
proxies = [{'http':  'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}]
# proxies = [None]

def printError(msg, exit = False):
    """
    Imprime mensaje de Error y sale del programa
    """
    sys.stderr.write('Error:\t%s\n' % msg)
    if exit:
        sys.exit(1)

def addOptions():
    """
    Aquí se configuraron las banderas posibles para la ejecución del programa
    """
    parser = optparse.OptionParser()
    parser.add_option('-v', '--verbose', dest='verbose', default=None, action='store_true', help='If specified, prints detailed information during execution.')
    parser.add_option('-n', '--num-res', dest='num_res', default='50', help='Port that the HTTP server is listening to.')
    parser.add_option('-b', '--buscadores', dest='buscadores', default='google', help='Port that the HTTP server is listening to.')
    parser.add_option('-N', '--no-params', dest='no_params', default=False, action='store_true', help='If specified, prints detailed information during execution.')
    parser.add_option('-r', '--regex', dest='regex', default=False, action="store_true", help='Make request with TOR')
    parser.add_option('-d', '--domains', dest='domains', default=False, action="store_true", help='Make request with TOR')
    parser.add_option('-U', '--user-agents', dest='user_agents', default=None, help='Port that the HTTP server is listening to.')
    parser.add_option('-P', '--proxies', dest='proxies', default=None, help='Port that the HTTP server is listening to.')
    parser.add_option('-F', '--formato', dest='formato', default='txt', help='Port that the HTTP server is listening to.')
    parser.add_option('-i', '--intervalo', dest='intervalo', default='0', help='Port that the HTTP server is listening to.')
    parser.add_option('-p', '--ip', dest='ip', default=None, help='Port that the HTTP server is listening to.')
    parser.add_option('-m', '--mail', dest='mail', default=None, help='Port that the HTTP server is listening to.')
    parser.add_option('-f', '--filetype', dest='filetype', default=None, help='Port that the HTTP server is listening to.')
    parser.add_option('-s', '--site', dest='site', default=None, help='Port that the HTTP server is listening to.')
    parser.add_option('-e', '--exclude', dest='exclude', default=None, help='Port that the HTTP server is listening to.')
    parser.add_option('-I', '--include', dest='include', default=None, help='Port that the HTTP server is listening to.')
    parser.add_option('-u', '--inurl', dest='inurl', default=None, help='Port that the HTTP server is listening to.')
    return parser.parse_args()

def lee_proxies(proxies):
    with open(proxies) as f:
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

def lee_user_agents(user_agents):
    with open(user_agents) as f:
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
    
def expandir(queries, dicc):
    lst = [{}]
    agrega(lst, 'ip', opts.ip)
    agrega(lst, 'filetype', opts.filetype)
    agrega(lst, 'site', opts.site)
    agrega(lst, 'exclude', opts.exclude)
    agrega(lst, 'include', opts.include)
    agrega(lst, 'inurl', opts.inurl)
    return [(d, q) for q in queries for d in lst]
    
if __name__ == '__main__':
    try:
        opts, args = addOptions()
        if len(args) == 0:
            print("Uso: python3 %s <busqueda> [parametros]" % sys.argv[0])
            sys.exit(1)
        if opts.proxies:
            lee_proxies(opts.proxies)
        if opts.user_agents:
            lee_user_agents(opts.user_agents)
        buscadores = []
        fabrica = FabricaBuscador()
        for x in opts.buscadores.split(','):
            buscadores.append(fabrica.get_buscador(x.strip()))
        q = [x.strip() for x in args[0].split('+')]
        queries = [y for x in q for y in list(exrex.generate(x))] if opts.regex else q
        expansiones = expandir(queries, opts)
        intervalo = int_or_0(opts.intervalo)
        num_res = int_or_0(opts.num_res)
        resultados = {}
        for d, q in expansiones:
            proxy = proxies[randint(0, len(proxies) - 1)]
            for b in buscadores:
                user_agent = user_agents[randint(0, len(user_agents) - 1)]
                r = b.busqueda(d, q, proxy, user_agent, num_res, opts.no_params, intervalo)
                if not r:
                    for x in proxies:
                        if x != proxy:
                            r = b.busqueda(d, q, x, user_agent, num_res, opts.no_params, intervalo)
                        if r: break
                r = r if r else []
                if not resultados.get(b.nombre, None):
                    resultados[b.nombre] = []
                for x in r:                    
                    resultados[b.nombre].append(x)
        formato(resultados, opts.formato, opts.domains)
    except Exception as e:
        printError('Ocurrio un error inesperado: %s' % str(e))
