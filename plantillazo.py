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
import optparse
import navegacion as nav
from formato import formato
from buscador import FabricaBuscador

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
    parser.add_option('-u', '--user-agents', dest='user_agents', default=None, help='Port that the HTTP server is listening to.')
    parser.add_option('-p', '--proxies', dest='proxies', default=None, help='Port that the HTTP server is listening to.')
    parser.add_option('-f', '--formato', dest='formato', default='txt', help='Port that the HTTP server is listening to.')
    return parser.parse_args()

def myip():
    """
    Devuelve la IP pública con la que se está realizando el request
    """
    my_ip = urlopen('http://ip.42.pl/raw').read()
    print('La IP que se eśtá usando es: ', my_ip)

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
                nav.proxies.append(tmp)

def lee_user_agents(user_agents):
    with open(user_agents) as f:
        for u in f.readlines():
            nav.user_agents.append(u.strip())

def int_or_0(n):
    try:
        return int(n)
    except:
        return 0
    
if __name__ == '__main__':
    try:
        opts, args = addOptions()
        if len(args) == 0:
            print("Uso: python3 %s <busqueda> [parametros]" % sys.argv[0])
            sys.exit(1)
        query = args[0]
        if opts.proxies:
            lee_proxies(opts.proxies)
        if opts.user_agents:
            lee_user_agents(opts.user_agents)
        buscadores = []
        fabrica = FabricaBuscador()
        for x in opts.buscadores.split(','):
            buscadores.append(fabrica.get_buscador(x.strip()))
        resultados = []
        for b in buscadores:
            resultados += b.busqueda(query, int_or_0(opts.num_res), opts.no_params, opts.regex)
        print(formato(resultados, opts.formato, opts.domains))
        # print(nav.hacer_peticion("http://google.com").text)
    except Exception as e:
        printError('Ocurrio un error inesperado: %s' % str(e))
